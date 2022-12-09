"""Script to generate linkml YAML from a SKOS vocabulary.

Part of the iSamples project.

Output is a linkml schema containing enums that represent SKOS concepts.
"""

import datetime
import sys
import textwrap
import click
import rdflib
from rdflib.namespace import SKOS, RDF, RDFS, OWL
import yaml

NS = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "obo": "http://purl.obolibrary.org/obo/",
    "geosciml": "http://resource.geosciml.org/classifier/cgi/lithology",
}


PFX = """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""

INDENT = "  "


def skosT(term):
    return rdflib.URIRef(f"{NS['skos']}{term}")


def rdfT(term):
    return rdflib.URIRef(f"{NS['rdf']}{term}")


def rdfsT(term):
    return rdflib.URIRef(f"{NS['rdfs']}{term}")


def listVocabularies(g):
    """List the vocabularies in the provided graph"""
    q = (
        PFX
        + """SELECT ?s
    WHERE {
        ?s rdf:type skos:ConceptScheme.
    }"""
    )
    qres = g.query(q)
    res = []
    for r in qres:
        res.append(r[0])
    return res


def getVocabRoot(g, v):
    """Get top concept of the specific vocabulary"""
    q = rdflib.plugins.sparql.prepareQuery(
        PFX
        + """SELECT ?s
    WHERE {
        ?s skos:topConceptOf ?vocabulary .
    }"""
    )
    qres = g.query(q, initBindings={"vocabulary": v})
    res = []
    for row in qres:
        res.append(row[0])
    return res


def getNarrower(g, v, r):
    q = rdflib.plugins.sparql.prepareQuery(
        PFX
        + """SELECT ?s
    WHERE {
        ?s skos:inScheme ?vocabulary .
        ?s skos:broader ?parent .
    }"""
    )
    qres = g.query(q, initBindings={"vocabulary": v, "parent": r})
    res = []
    for row in qres:
        res.append(row[0])
    return res


def getObjects(g, s, p):
    q = rdflib.plugins.sparql.prepareQuery(
        PFX
        + """SELECT ?o
    WHERE {
        ?subject ?predicate ?o .
    }"""
    )
    qres = g.query(q, initBindings={"subject": s, "predicate": p})
    res = []
    for row in qres:
        res.append(row[0])
    return res


def _labelToLink(label):
    if isinstance(label, list):
        label = label[0]
    label = label.split("/")[-1]
    label = label.lower().strip()
    label = label.replace(",", "")
    label = label.replace(" ", "-")
    return label


def termTree(g, v, r, depth=0):
    label = getObjects(g, r, skosT("prefLabel"))
    llabel = _labelToLink(r)
    res = [f"{'    '*depth}- [{label[0]}](#{llabel})"]
    for term in getNarrower(g, v, r):
        res += termTree(g, v, term, depth=depth + 1)
    return res


def termJsonTree(g, v, r, depth=0):
    label = getObjects(g, r, skosT("prefLabel"))[0]
    llabel = _labelToLink(r)
    obj = {
        "name": label,
        "target": llabel,
    }
    # res = [f"{'    '*depth}- [{label[0]}](#{llabel})"]
    children = []
    for term in getNarrower(g, v, r):
        children.append(termJsonTree(g, v, term, depth=depth + 1))
    obj["children"] = children
    return obj


def describeTerm(g, t, depth=0, level=1):
    res = []
    labels = getObjects(g, t, skosT("prefLabel"))
    hl = f"{'#'*(depth+1)} "
    if len(labels) < 1:
        res.append(f"{hl} `{t}`")
    else:
        res.append(f"{hl} {labels[0].strip()}")
        for label in labels[1:]:
            res.append(f"* `{label}`")
        res.append("")
    _target = t.split("/")[-1]
    res.append("[]{" + f"#{_labelToLink(_target)}" + "}")
    res.append("")
    res.append(f"Concept: [`{t.split('/')[-1]}`]({t})")
    broader = getObjects(g, t, skosT("broader"))
    if len(broader) > 0:
        res.append("")
        res.append("Child of:")
        for b in broader:
            bt = b.split("/")[-1]
            res.append(f" [`{bt}`](#{bt})")
    res.append("")
    # The textual description will be present in rdfs:comment or
    # skos:definition.
    comments = []
    for comment in getObjects(g, t, rdfsT("comment")):
        comments.append(comment)
    for comment in getObjects(g, t, skosT("definition")):
        comments.append(comment)
    for comment in comments:
        lines = textwrap.wrap(comment, width=70)
        res += lines
    seealsos = getObjects(g, t, rdfsT("seeAlso"))
    if len(seealsos) > 0:
        res.append("")
        res.append("See Also:")
        res.append("")
        for seealso in seealsos:
            res.append(f"* [{seealso.n3(g.namespace_manager)}]({seealso})")
    return res


def describeNarrowerTerms(g, v, r, depth=0, level=[]):
    res = []
    terms = getNarrower(g, v, r)
    for term in terms:
        res += describeTerm(g, term, depth=depth)
        res.append("")
        res += describeNarrowerTerms(g, v, term, depth=depth + 1)
    return res


def describeVocabulary(G, V):
    res = []
    level = [
        1,
    ]
    title = getObjects(G, V, skosT("prefLabel"))[0]
    res.append("---")
    res.append(
        "comment: | \n  WARNING: This file is generated. Any edits will be lost!"
    )
    res.append(f'title: "{title.strip()}"')
    res.append(
        f'date: "{datetime.datetime.now().replace(tzinfo=datetime.timezone.utc).isoformat()}"'
    )
    res.append("subtitle: |")
    for comment in getObjects(G, V, skosT("definition")) + getObjects(
        G, V, rdfsT("comment")
    ):
        res.append(f"  {comment.strip()}")
    res.append("execute:")
    res.append("  echo: false")
    res.append("---")
    res.append("")
    res.append("Namespace: ")
    res.append(f"[`{V}`]({V})")
    res.append("")
    res.append("**History**")
    res.append("")
    for history in getObjects(G, V, skosT("historyNote")):
        res.append(f"* {history}")
    res.append("")
    res.append("**Concepts**")
    res.append("")
    depth = 1
    roots = getVocabRoot(G, V)
    for root in roots:
        res += termTree(G, V, root, depth=0)
        res.append("")
    # res.append("```{ojs}")
    ##res.append("import {Tree} from '@d3/tree'")
    # res.append(TREE_CHART_SCRIPT)
    # res.append(f"vocab_terms=JSON.parse({json.dumps(json.dumps(termJsonTree(G, V, roots[0], depth=0)))});")
    # res.append(TREE_CHART_BLOCK)
    # res.append("```")
    for aroot in roots:
        res += describeTerm(G, aroot, depth=depth, level=level)
        res.append("")
        res += describeNarrowerTerms(G, V, aroot, depth=depth + 1, level=level)
        res.append("")
    return res


def vocab_to_dict(G, V) -> (str, dict):
    # name = str(getObjects(G, V, skosT("prefLabel"))[0])
    name = G.compute_qname(V)
    res = {}
    return name, res


class VocabHandler:
    PFX = """
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    """

    def __init__(
        self,
        G: rdflib.ConjunctiveGraph,
        schema_id: str,
        schema_name: str,
        default_prefix: str,
    ):
        self._version = 1  # TODO: set this
        self.schema_id = schema_id
        self.schema_name = schema_name
        self.default_prefix = default_prefix
        self._G = G

    def getObjects(self, s, p):
        q = rdflib.plugins.sparql.prepareQuery(
            self.PFX
            + """SELECT ?o
        WHERE {
            ?subject ?predicate ?o .
        }"""
        )
        qres = self._G.query(q, initBindings={"subject": s, "predicate": p})
        res = []
        for row in qres:
            res.append(row[0])
        return res

    def oneStrObject(self, s, p, default=""):
        objects = self.getObjects(s,p)
        if len(objects) < 1:
            return default
        return str(objects[0])

    def objectName(self, obj):
        pfx, uri, label = self._G.compute_qname(obj)
        if pfx == self.default_prefix:
            return label
        return f"{pfx}:{label}"

    def vocabs(self) -> list[rdflib.URIRef]:
        q = (
            self.PFX
            + """SELECT ?s
        WHERE {
            ?s rdf:type skos:ConceptScheme.
        }"""
        )
        qres = self._G.query(q)
        res = []
        for r in qres:
            res.append(r[0])
        return res

    def concepts(self, vocab) ->list[rdflib.URIRef]:
        q = rdflib.plugins.sparql.prepareQuery(
            PFX
            + """SELECT ?s
        WHERE {
            ?s skos:inScheme ?vocabulary .
            ?s rdf:type skos:Concept .
        }"""
        )
        qres = self._G.query(q, initBindings={"vocabulary": vocab})
        res = []
        for row in qres:
            res.append(row[0])
        return res

    def concept(self, c_uri) -> tuple[str, dict]:

        def addlist(p):
            res = []
            for m in self.getObjects(c_uri,p):
                res.append(str(m))
            return res

        cname = self.objectName(c_uri)
        e = {
            "label":self.oneStrObject(c_uri, RDFS.label).strip(),
            "description":self.oneStrObject(c_uri, SKOS.definition).strip(),
        }
        e["exact_mappings"] = addlist(SKOS.exactMatch)
        e["close_mappings"] = addlist(SKOS.closeMatch)
        e["notes"] = addlist(SKOS.note)
        e["notes"] += addlist(SKOS.historyNote)
        e["notes"] += addlist(SKOS.editorialNote)
        e["notes"] += addlist(SKOS.scopeNote)

        SKOS.
        return (cname, e)



    def asDict(self) -> dict:
        schemadoc = {
            "id": self.schema_id,
            "name": self.schema_name,
            "version": self._version,
            "prefixes": {},
            "default_prefix": self.default_prefix,
            "enums": {},
        }
        # Set the prefixes
        for ns in self._G.namespace_manager.namespaces():
            schemadoc["prefixes"][ns[0]] = str(ns[1])
        for vocab in self.vocabs():
            vname = self.objectName(vocab)
            vdoc = {"description": self.oneStrObject(vocab,SKOS.definition),
                    "permissible_values": {}
                    }
            for concept in self.concepts(vocab):
                c_name, c_doc = self.concept(concept)
                vdoc["permissible_values"][c_name] = c_doc
            schemadoc["enums"][vname] = vdoc

        return schemadoc


@click.command()
@click.argument("ttl")
@click.option(
    "-i",
    "--schema_id",
    default="http://resource.isamples.org/schema/0.2.1",
    help="Schema identifier",
)
@click.option("-n", "--schema_name", default="physicalSample", help="Schema name")
@click.option(
    "-d",
    "--default_prefix",
    default="isam:http://resource.isamples.org/schema/",
    help="Default prefix:namespace to use",
)
def main(ttl, schema_id, schema_name, default_prefix):
    """Load SKOS to a dictionary that can be dumped to YAML for linkml.

    TTL may be a local file or URL.

    Output to STDOUT.
    """
    # Load the source graph
    vgraph = rdflib.ConjunctiveGraph()
    vgraph.parse(ttl, format="text/turtle")

    dprefix, dname = default_prefix.split(":", 1)
    dprefix = dprefix.strip()
    dname = dname.strip()
    NS[dprefix] = dname
    # Bind the namespaces
    for k, v in NS.items():
        vgraph.bind(k, v)
    vhandler = VocabHandler(vgraph, schema_id, schema_name, dprefix)
    yaml.safe_dump(vhandler.asDict(), sys.stdout, sort_keys=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())

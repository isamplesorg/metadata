import sys
import logging
import textwrap
import click
import rdflib

NS = {
    "@vocab":"https://w3id.org/isample/vocabulary/",
    "rdf":"http://www.w3.org/1999/02/22-rdf-syntax-ns#", 
    "rdfs":"http://www.w3.org/2000/01/rdf-schema#",
    "owl":"http://www.w3.org/2002/07/owl#",
    "skos": "http://www.w3.org/2004/02/skos/core#",   
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
    '''List the vocabularies in the provided graph
    '''
    q = PFX + """SELECT ?s
    WHERE {
        ?s rdf:type skos:ConceptScheme.
    }"""
    qres = g.query(q)
    res = []
    for r in qres:
        res.append(r[0])
    return res

        
def getVocabRoot(g, v):
    """Get top concept of the specific vocabulary
    """    
    q = rdflib.plugins.sparql.prepareQuery(PFX + """SELECT ?s
    WHERE {
        ?s skos:topConceptOf ?vocabulary .
    }""")
    qres = g.query(q, initBindings={'vocabulary': v})
    res = []
    for row in qres:
        res.append(row[0])
    return res

def getNarrower(g, v, r):
    q = rdflib.plugins.sparql.prepareQuery(PFX + """SELECT ?s
    WHERE {
        ?s skos:inScheme ?vocabulary .
        ?s skos:broader ?parent .
    }""")
    qres = g.query(q, initBindings={'vocabulary': v, 'parent':r})
    res = []
    for row in qres:
        res.append(row[0])
    return res


def getObjects(g, s, p):
    q = rdflib.plugins.sparql.prepareQuery(PFX + """SELECT ?o
    WHERE {
        ?subject ?predicate ?o .
    }""")
    qres = g.query(q, initBindings={'subject':s, 'predicate':p})
    res = []
    for row in qres:
        res.append(row[0])
    return res


def termTree(g, v, r, depth=0):
    label = getObjects(g, r, skosT("prefLabel"))
    llabel = label[0].lower().strip()
    llabel = llabel.replace(" ","")
    res = [f"{'    '*depth}- [{label[0]}](#{llabel})"]
    for term in getNarrower(g, v, r):
        res += termTree(g, v, term, depth=depth+1)
    return res


def describeTerm(g, t, depth=0, level=1):
    res = []
    labels = getObjects(g, t, skosT('prefLabel'))
    hl = f"{'#'*(depth+1)} "
    if len(labels) < 1:
        res.append(f"{hl} `{t}`")
    else:
        res.append(f"{hl} {labels[0].strip()}")
        for label in labels[1:]:
            res.append(f"* `{label}`")
        res.append("")
    res.append(f"Concept: [`{t.split('/')[-1]}`]({t})")
    broader = getObjects(g, t, skosT('broader'))
    if len(broader) > 0:
        res.append("")
        res.append("Child of:")
        for b in broader:
            bt = b.split('/')[-1]
            res.append(f" [`{bt}`](#{bt})")
    res.append("")
    for comment in getObjects(g, t, rdfsT('comment')):
        lines = textwrap.wrap(
                    comment, 
                    width=70
                    )
        res += lines
    
    return res

def describeNarrowerTerms(g, v, r, depth=0, level=[]):
    res = []
    terms = getNarrower(g, v, r)
    for term in terms:
        res += describeTerm(g, term, depth=depth)
        res.append("")
        res += describeNarrowerTerms(g, v, term, depth=depth+1)
    return res

def describeVocabulary(G, V):
    res = []
    level = [1, ]
    title = getObjects(G, V, skosT("prefLabel"))[0]
    res.append(f"# {title}")
    res.append("")
    res.append(f"[`{V}`]({V})")
    res.append("")
    for comment in getObjects(G, V, rdfsT("comment")):
        res.append(comment)
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
    for aroot in roots:
        res += describeTerm(G, aroot, depth=depth, level=level)
        res.append("")
        res += describeNarrowerTerms(G, V, aroot, depth=depth+1, level=level)
        res.append("")
    return res

@click.command()
@click.argument("ttl")
def main(ttl):
    vgraph = rdflib.ConjunctiveGraph()
    vgraph.parse(ttl)
    vocabs = listVocabularies(vgraph)
    res = []
    for vocab in vocabs:
        res.append(describeVocabulary(vgraph, vocab))
    for doc in res:
        for line in doc:
            print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
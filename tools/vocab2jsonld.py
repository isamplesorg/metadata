'''Script to produce a JSON-LD serialization of an iSamples vocabulary.
'''
import sys
import logging
import click
import rdflib

NAMESPACES = {
    "@vocab":"https://w3id.org/isample/vocabulary/",
    "rdfs":"http://www.w3.org/2000/01/rdf-schema#",
    "owl":"http://www.w3.org/2002/07/owl#",
    "skos": "http://www.w3.org/2004/02/skos/core#",    
}


def ttl2jsonld(fn_src:str, namespaces:dict)->str:
    g = rdflib.ConjunctiveGraph()
    _base = "https://w3id.org/isample/vocabulary/"
    g.parse(fn_src)
    _context = namespaces
    _context["mat"] = "https://w3id.org/isample/vocabulary/material/0.9/"
    print(g.serialize(format="json-ld", base=_base, context=_context, use_native_types=True))


@click.command()
@click.argument("ttl")
def main(ttl):
    ttl2jsonld(ttl, NAMESPACES)
    return 0


if __name__ == "__main__":
    sys.exit(main())
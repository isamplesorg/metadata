[![NSF-2004562](https://img.shields.io/badge/NSF-ID=2004562-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=2004562)
[![NSF-2004815](https://img.shields.io/badge/NSF-ID=2004815-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=2004815)
[![NSF-2004839](https://img.shields.io/badge/NSF-ID=2004839-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=2004839)
[![NSF-2004642](https://img.shields.io/badge/NSF-ID=2004642-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=2004642)

# metadata

Defines the core metadata model for iSamples.

`src/schemas/isamples_core.yaml` defines the iSamples core model in LinkML. It references vocabularies contained in [`isamplesorg/vocabularies/vocabulary`](https://github.com/isamplesorg/vocabularies/tree/develop/vocabulary) which define terms for the Material Type, Sampled Feature, and Material Sample Object Type vocabularies.

Documentation is available at https://isamplesorg.github.io/metadata/

## Repository Structure

```
metadata/
├── src/
│   └── schemas/           # LinkML schema definitions
│       └── isamples_core.yaml
├── background/            # Diagrams and information about existing models
│   ├── DataCite/
│   ├── ESS-DIVE/
│   ├── GEOME-TDWG/
│   ├── GeoScience/
│   ├── ODM-CUAHSI/
│   └── OpenContext-Archae-anthro/
├── examples/              # Example metadata documents from different systems
│   ├── APItesting/
│   ├── GEOME/
│   ├── geoJSON/
│   ├── iSamples/
│   ├── OpenContext/
│   ├── script/
│   ├── SESAR/
│   └── smithonsonian/
├── vocabulary/            # Vocabulary-related files
├── tools/                 # Modified docgen tool and templates for Quarto
├── quarto/                # Quarto configuration files
├── build/                 # Build output (intermediate docs)
│   └── docs/              # Generated markdown documentation
├── tests/                 # Test files
└── notes/                 # Development notes
```

## Development

LinkML and associated tools require a Python environment (version 3.9 or newer) and uses [Poetry](https://python-poetry.org/) for dependency management. Poetry can be installed with `pip install poetry`.

To work on project contents and run artifact generators, first grab the source and switch to the develop branch:

```bash
git clone https://github.com/isamplesorg/metadata.git
cd metadata
git checkout develop
git pull
```

Setup a virtual environment using Poetry:

```bash
poetry shell
poetry install
```

(To exit poetry shell, use `exit`).

Artifacts are produced by running `make` or `make all`.

### Documentation Generation

Documentation is rendered with [Quarto](https://quarto.org/) rather than the default `mkdocs` or `Sphinx` (Quarto offers many additional features for including computed examples). To generate the documentation:

1. Install [Quarto >= 1.2](https://quarto.org/docs/get-started/)
2. Run `make`, `make all` or `make gen-docs`

This will generate markdown intermediate files in the `build/docs` folder, then invoke `quarto render` to generate HTML documentation.

Note that this project uses a modified version of the LinkML `docgen` tool and templates to render markdown for Quarto. The modified `docgen` and templates are located in the `tools/` folder.

## LinkML Schema Operations

### Convert YAML schema to JSON schema

```bash
gen-json-schema -t PhysicalSampleRecord --not-closed src/schemas/isamples_core.yaml > isamples_core.schema.json
```

The `-t PhysicalSampleRecord` option makes the "PhysicalSampleRecord" class the top-level class in the JSON schema.

### Generate JSON-LD context

```bash
gen-jsonld-context src/schemas/isamples_core.yaml > isamples_core.jsonld
```

After generating the JSON-LD context, the enumeration part may need manual modification. For each enumeration, use `@type` to declare the enumeration type.

<details>
  <summary>Example modified JSON-LD context</summary>

```json
{
   "@context": {
      "dct": "http://purl.org/dc/terms/",
      "isam": "http://resource.isamples.org/schema/",
      "mat": "http://resource.isamples.org/vocabulary/material/",
      "sf": "http://resource.isamples.org/vocabulary/sampledFeature/",
      "skos": "http://www.w3.org/2004/02/skos/core#",
      "spt": "http://resource.isamples.org/vocabulary/sampleobjecttype/",
      "xsd": "http://www.w3.org/2001/XMLSchema#",
      "@vocab": "http://resource.isamples.org/schema/",
      "hasContextCategory": {
         "@type": "contextcategory"
      },
      "hasMaterialCategory": {
         "@type": "materialtype"
      },
      "has_sample_object_type": {
         "@type": "specimencategory"
      },
      "id": "@id",
      "latitude": {
         "@type": "xsd:decimal"
      },
      "longitude": {
         "@type": "xsd:decimal"
      },
      "resultTime": {
         "@type": "xsd:date"
      }
   }
}
```
</details>

### Validate instance files

```bash
linkml-validate -s src/schemas/isamples_core.yaml instance.json
jsonschema -i instance.json isamples_core.schema.json
```

The first command validates an instance file against the YAML schema. The second command validates against the JSON schema.

## Docker

The iSamples Metadata Docker container is based on the Docker container from the LinkML project ([https://hub.docker.com/r/monarchinitiative/linkml/tags](https://hub.docker.com/r/monarchinitiative/linkml/tags)).

Build the image:

```bash
docker build -t isamples_linkml .
```

Run the container (opens a bash shell with the repository mounted at `/work`):

```bash
docker run -a stdin -a stdout -i -t -v `pwd`:/work isamples_linkml
```

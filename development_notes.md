# iSamples Schema Development Notes

1. All artifacts should be built from the source schema.
2. The source schema is `src/schemas/isamples_core.yaml`.
3. The source schema is defined using LinkML YAML.
4. Artifacts are generated using the linkml tools.
5. HTML documentation is built with Quarto, with linkml used to generate the `.qmd`

## Generating HTML

Destination = `docs/`. On GitHub, that folder is used to serve the content using GitHub pages. An intermediate folder `build/docs` is used to hold ther intermediate files prior to running the markdown to html generator.

Generating the `.qmd` files:
```
python tools/docgen.py \
  --log_level INFO
  --dialect quarto \
  --sort-by name \
  --format quarto \
  --mergeimports \
  --metadata \
  --directory docs \
  src/schema/isamples_core.yaml
```

Building the HTML using quarto:
```
# create intermediate folder
mkdir docs
# Copy static stuff from source to destination
cp src/docs/*.md docs/
# Copy quarto config and related artifacts to docs
cp quarto/* docs/
touch docs/.nojekyll
pushd docs
quarto render
popd
```
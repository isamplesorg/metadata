# All artifacts of the build should be preserved
.SECONDARY:

# ----------------------------------------
# Model documentation and schema directory
# ----------------------------------------
SRC_DIR = src
PKG_DIR = generated
TARGET_DIR = build
SCHEMA_DIR = $(SRC_DIR)/schemas
VOCAB_DIR = $(SRC_DIR)/vocabularies
MODEL_DOCS_DIR = $(SRC_DIR)/docs
SOURCE_FILES := $(shell find $(SCHEMA_DIR) -name '*.yaml')
SCHEMA_NAMES = $(patsubst $(SCHEMA_DIR)/%.yaml, %, $(SOURCE_FILES))
VOCAB_FILES := $(shell find $(VOCAB_DIR) -name '*.ttl')

SCHEMA_NAME = isamples_core
SCHEMA_SRC = $(SCHEMA_DIR)/$(SCHEMA_NAME).yaml
PKG_TGTS = jsonld_context json_schema owl shacl
TGTS = docs python $(PKG_TGTS)

# Targets by PKG_TGT
PKG_T_GRAPHQL = $(PKG_DIR)/graphql
PKG_T_JSON = $(PKG_DIR)/json
PKG_T_JSONLD_CONTEXT = $(PKG_DIR)/jsonld
PKG_T_JSON_SCHEMA = $(PKG_DIR)/json_schema
PKG_T_OWL = $(PKG_DIR)/owl
PKG_T_RDF = $(PKG_DIR)/rdf
PKG_T_SHEX = $(PKG_DIR)/shex
PKG_T_SQLDDL = $(PKG_DIR)/sqlddl
PKG_T_DOCS = docs
PKG_T_SHACL = $(PKG_DIR)/shacl
PKG_T_PYTHON = $(PKG_DIR)
PKG_T_MODEL = $(PKG_DIR)/model
PKG_T_SCHEMA = $(PKG_T_MODEL)/schema

# Global generation options
GEN_OPTS = --log_level WARNING
#ENV = export PIPENV_VENV_IN_PROJECT=true && export PIPENV_PIPFILE=make-venv/Pipfile && export PIPENV_IGNORE_VIRTUALENVS=1
#RUN = $(ENV) && pipenv run
RUN = poetry run

# ----------------------------------------
# TOP LEVEL TARGETS
# ----------------------------------------
all: gen

install:
	poetry install

# ---------------------------------------
# Test runner
# ----------------------------------------
test: install
    PYTHONPATH=PKG_DIR poetry run python -m unittest

# ---------------------------------------
# GEN: run generator for each target
# ---------------------------------------
gen: $(patsubst %,gen-%,$(TGTS))

# ---------------------------------------
# CLEAN: clear out all of the targets
# ---------------------------------------
clean:
	rm -rf $(TARGET_DIR)
	rm -rf docs
	rm -rf $(PKG_DIR)
	#poetry install --sync
.PHONY: clean

# ---------------------------------------
# SQUEAKY_CLEAN: remove all of the final targets to make sure we don't leave old artifacts around
# ---------------------------------------
squeaky-clean: uninstall clean $(patsubst %,squeaky-clean-%,$(PKG_TGTS))
	find docs/*  ! -name 'README.*' -exec rm -rf {} +
	find $(PKG_DIR)/model/schema  ! -name 'README.*' -type f -exec rm -f {} +
	find $(PKG_DIR) -name "*.py" ! -name "__init__.py" ! -name "linkml_files.py" -exec rm -f {} +
	cd make-venv && $(ENV) && pipenv --rm

squeaky-clean-%: clean
	find $(PKG_DIR)/$* ! -name 'README.*' ! -name $*  -type f -exec rm -f {} +

# ---------------------------------------
# T: List files to generate
# ---------------------------------------
t:
	echo $(SCHEMA_NAMES)

# ---------------------------------------
# ECHO: List all targets
# ---------------------------------------
echo:
	echo $(patsubst %,gen-%,$(TGTS))

tdir-%:
	rm -rf $(TARGET_DIR)/$*
	mkdir -p $(TARGET_DIR)/$*

# ---------------------------------------
# MARKDOWN DOCS
#      Generate documentation ready for mkdocs
# ---------------------------------------
gen-docs: $(TARGET_DIR)/docs/index.md vocabs
	# static sources
	cp -R $(MODEL_DOCS_DIR)/*.md $(TARGET_DIR)/docs
	# quarto configuation and customizations
	cp quarto/* $(TARGET_DIR)/docs
	#cat $(TARGET_DIR)/docs/_contents.yaml >> $(TARGET_DIR)/docs/_quarto.yml
	mkdir -p docs
	touch docs/.nojekyll
	# output from quarto is determined by the output-dir property in _quarto.yml
	cd $(TARGET_DIR)/docs && quarto render

vocabs:
	mkdir -p ${TARGET_DIR}/docs/vocabularies
	python tools/vocab2md.py ${VOCAB_DIR}/materialtype.ttl > $(TARGET_DIR)/docs/vocabularies/materialtype.md
	python tools/vocab2md.py ${VOCAB_DIR}/sampledfeature.ttl > $(TARGET_DIR)/docs/vocabularies/sampledfeature.md
	python tools/vocab2md.py ${VOCAB_DIR}/specimentype.ttl > $(TARGET_DIR)/docs/vocabularies/specimentype.md

$(TARGET_DIR)/docs/index.md: $(SCHEMA_DIR)/$(SCHEMA_NAME).yaml tdir-docs
	python tools/docgen.py $(GEN_OPTS) --dialect quarto --sort-by name --format quarto --mergeimports --metadata --directory $(TARGET_DIR)/docs $<

# ---------------------------------------
# YAML source
# ---------------------------------------
gen-model: $(patsubst %, $(PKG_T_SCHEMA)/%.yaml, $(SCHEMA_NAMES))

$(PKG_T_SCHEMA)/%.yaml: model/schema/%.yaml
	mkdir -p $(PKG_T_SCHEMA)
	cp $< $@

# ---------------------------------------
# PYTHON Source
# ---------------------------------------
gen-python: $(patsubst %, $(PKG_T_PYTHON)/%.py, $(SCHEMA_NAMES))
$(PKG_T_PYTHON)/%.py: $(TARGET_DIR)/python/%.py
	mkdir -p $(PKG_T_PYTHON)
	cp $< $@
$(TARGET_DIR)/python/%.py: $(SCHEMA_DIR)/%.yaml  tdir-python install
	$(RUN) gen-python $(GEN_OPTS)  --no-slots --no-mergeimports $< > $@

# ---------------------------------------
# GRAPHQL Source
# ---------------------------------------
gen-graphql: $(PKG_T_GRAPHQL)/$(SCHEMA_NAME).graphql
.PHONY: gen-graphql

$(PKG_T_GRAPHQL)/%.graphql: $(TARGET_DIR)/graphql/%.graphql
	mkdir -p $(PKG_T_GRAPHQL)
	cp $< $@

$(TARGET_DIR)/graphql/%.graphql: $(SCHEMA_DIR)/%.yaml tdir-graphql install
	$(RUN) gen-graphql $(GEN_OPTS) $< > $@

# ---------------------------------------
# JSON Schema
# ---------------------------------------
gen-json_schema: $(patsubst %, $(PKG_T_JSON_SCHEMA)/%.schema.json, $(SCHEMA_NAMES))
.PHONY: gen-json_schema

$(PKG_T_JSON_SCHEMA)/%.schema.json: $(TARGET_DIR)/json_schema/%.schema.json
	mkdir -p $(PKG_T_JSON_SCHEMA)
	cp $< $@

$(TARGET_DIR)/json_schema/%.schema.json: $(SCHEMA_DIR)/%.yaml tdir-json_schema install
	$(RUN) gen-json-schema $(GEN_OPTS) -t transaction $< > $@

# ---------------------------------------
# ShEx
# ---------------------------------------
gen-shex: $(patsubst %, $(PKG_T_SHEX)/%.shex, $(SCHEMA_NAMES)) $(patsubst %, $(PKG_T_SHEX)/%.shexj, $(SCHEMA_NAMES))
.PHONY: gen-shex

$(PKG_T_SHEX)/%.shex: $(TARGET_DIR)/shex/%.shex
	mkdir -p $(PKG_T_SHEX)
	cp $< $@
$(PKG_T_SHEX)/%.shexj: $(TARGET_DIR)/shex/%.shexj
	mkdir -p $(PKG_T_SHEX)
	cp $< $@

$(TARGET_DIR)/shex/%.shex: $(SCHEMA_DIR)/%.yaml tdir-shex install
	$(RUN) gen-shex --no-mergeimports $(GEN_OPTS) $< > $@
$(TARGET_DIR)/shex/%.shexj: $(SCHEMA_DIR)/%.yaml tdir-shex install
	$(RUN) gen-shex --no-mergeimports $(GEN_OPTS) -f json $< > $@

# ---------------------------------------
# OWL
# ---------------------------------------
gen-owl: $(PKG_T_OWL)/$(SCHEMA_NAME).owl.ttl
.PHONY: gen-owl

$(PKG_T_OWL)/%.owl.ttl: $(TARGET_DIR)/owl/%.owl.ttl
	mkdir -p $(PKG_T_OWL)
	cp $< $@
$(TARGET_DIR)/owl/%.owl.ttl: $(SCHEMA_DIR)/%.yaml tdir-owl install
	$(RUN) gen-owl $(GEN_OPTS) $< > $@

# ---------------------------------------
# SHACL
# ---------------------------------------
gen-shacl: $(PKG_T_SHACL)/$(SCHEMA_NAME).shacl.ttl
.PHONY: gen-shacl

$(PKG_T_SHACL)/%.shacl.ttl: $(TARGET_DIR)/shacl/%.shacl.ttl
	mkdir -p $(PKG_T_SHACL)
	cp $< $@
$(TARGET_DIR)/shacl/%.shacl.ttl: $(SCHEMA_DIR)/%.yaml tdir-shacl install
	$(RUN) gen-shacl $(GEN_OPTS) $< > $@

# ---------------------------------------
# JSON-LD Context
# ---------------------------------------
gen-jsonld_context: $(patsubst %, $(PKG_T_JSONLD_CONTEXT)/%.context.jsonld, $(SCHEMA_NAMES)) $(patsubst %, $(PKG_T_JSONLD_CONTEXT)/%.model.context.jsonld, $(SCHEMA_NAMES))
.PHONY: gen-jsonld_context

$(PKG_T_JSONLD_CONTEXT)/%.context.jsonld: $(TARGET_DIR)/jsonld_context/%.context.jsonld
	mkdir -p $(PKG_T_JSONLD_CONTEXT)
	cp $< $@

$(PKG_T_JSONLD_CONTEXT)/%.model.context.jsonld: $(TARGET_DIR)/jsonld_context/%.model.context.jsonld
	mkdir -p $(PKG_T_JSONLD_CONTEXT)
	cp $< $@

$(TARGET_DIR)/jsonld_context/%.context.jsonld: $(SCHEMA_DIR)/%.yaml tdir-jsonld_context install
	$(RUN) gen-jsonld-context $(GEN_OPTS) --no-mergeimports $< > $@

$(TARGET_DIR)/jsonld_context/%.model.context.jsonld: $(SCHEMA_DIR)/%.yaml tdir-jsonld_context install
	$(RUN) gen-jsonld-context $(GEN_OPTS) --no-mergeimports $< > $@

# ---------------------------------------
# Plain Old (PO) JSON
# ---------------------------------------
gen-json: $(patsubst %, $(PKG_T_JSON)/%.json, $(SCHEMA_NAMES))
.PHONY: gen-json

$(PKG_T_JSON)/%.json: $(TARGET_DIR)/json/%.json
	mkdir -p $(PKG_T_JSON)
	cp $< $@
$(TARGET_DIR)/json/%.json: $(SCHEMA_DIR)/%.yaml tdir-json install
	$(RUN) gen-jsonld $(GEN_OPTS) --no-mergeimports $< > $@

# ---------------------------------------
# RDF
# ---------------------------------------
gen-rdf: gen-jsonld $(patsubst %, $(PKG_T_RDF)/%.ttl, $(SCHEMA_NAMES)) $(patsubst %, $(PKG_T_RDF)/%.model.ttl, $(SCHEMA_NAMES))
.PHONY: gen-rdf

$(PKG_T_RDF)/%.ttl: $(TARGET_DIR)/rdf/%.ttl
	mkdir -p $(PKG_T_RDF)
	cp $< $@
$(PKG_T_RDF)/%.model.ttl: $(TARGET_DIR)/rdf/%.model.ttl
	mkdir -p $(PKG_T_RDF)
	cp $< $@

$(TARGET_DIR)/rdf/%.ttl: $(SCHEMA_DIR)/%.yaml $(PKG_DIR)/jsonld/%.context.jsonld tdir-rdf install
	$(RUN) gen-rdf $(GEN_OPTS) --context $(realpath $(word 2,$^)) $< > $@
$(TARGET_DIR)/rdf/%.model.ttl: $(SCHEMA_DIR)/%.yaml $(PKG_DIR)/jsonld/%.model.context.jsonld tdir-rdf install
	$(RUN) gen-rdf $(GEN_OPTS) --context $(realpath $(word 2,$^)) $< > $@

# ---------------------------------------
# SQLDDL
# ---------------------------------------
gen-sqlddl: $(PKG_T_SQLDDL)/$(SCHEMA_NAME).sql
.PHONY: gen-sqlddl

$(PKG_T_SQLDDL)/%.sql: $(TARGET_DIR)/sqlddl/%.sql
	mkdir -p $(PKG_T_SQLDDL)
	cp $< $@
$(TARGET_DIR)/sqlddl/%.sql: $(SCHEMA_DIR)/%.yaml tdir-sqlddl install
	$(RUN) gen-sqlddl $(GEN_OPTS) $< > $@



# test docs locally.
docserve: gen-docs
	$(RUN) mkdocs serve

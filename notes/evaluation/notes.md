# Notes on linkml evaluation

The general goal is to have a specification for the core model to provide a basis for content interchange and discovery across physical sample collections. The model must be extensible to support more specific domains.

## Functional evaluations

### dynamic enums

These are introduced in linkml 1.3, however there appears to be no tooling support.

A better option may be to define out vocabularies in linkml and import those into the coremodel.

We want to assert that:

Values of material_type are instances of class `skos:Concept` that are `skos:inScheme` `mat:materialsvocabulary`.
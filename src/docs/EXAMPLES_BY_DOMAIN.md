# iSamples Examples by Scientific Domain

**Purpose:** Demonstrate how the same iSamples schema works across different scientific domains with concrete real-world examples.

**Key Insight:** The iSamples model is truly **domain-agnostic** - the same 8 entity types and 14 predicates work for archaeology, geology, biology, and more. **Only the values change**, not the structure.

---

## Table of Contents

1. [Archaeology (OpenContext)](#archaeology-opencontext)
2. [Geology (SESAR - Projected)](#geology-sesar---projected)
3. [Biology (GEOME - Projected)](#biology-geome---projected)
4. [Cross-Domain Comparison](#cross-domain-comparison)
5. [Domain-Specific Patterns](#domain-specific-patterns)

---

## Archaeology (OpenContext)

**Data Source:** OpenContext (https://opencontext.org)
**Dataset Size:** 1,096,352 samples from archaeological excavations worldwide
**Primary Domain:** Cultural heritage, archaeological artifacts

### Sample Profile: Pottery Sherd from Çatalhöyük

#### Complete Graph Structure

```
MaterialSampleRecord (Pottery Sherd)
  ├─ produced_by ───────→ SamplingEvent (2023 Excavation)
  │                           ├─ sampling_site ───→ SamplingSite (Çatalhöyük South Area)
  │                           │                         └─ site_location ───→ GeospatialCoordLocation (37.666°N, 32.827°E)
  │                           ├─ sample_location ──→ GeospatialCoordLocation (37.6665°N, 32.8274°E, depth: 3.2m)
  │                           └─ responsibility ───→ Agent (Dr. Sarah Johnson)
  │
  ├─ has_material_category ─→ IdentifiedConcept (Earthenware)
  ├─ has_context_category ──→ IdentifiedConcept (Terrestrial > Archaeological)
  ├─ has_sample_object_type ─→ IdentifiedConcept (Sherd)
  ├─ keywords ──────────────→ IdentifiedConcept (Neolithic)
  ├─ keywords ──────────────→ IdentifiedConcept (Pottery)
  ├─ keywords ──────────────→ IdentifiedConcept (Red-slipped ware)
  └─ registrant ────────────→ Agent (OpenContext Data Curator)
```

#### Full YAML Example

```yaml
# === SAMPLE NODE ===
sample_pottery_001:
  otype: MaterialSampleRecord
  pid: "igsn:IEOCH0001"
  label: "Ceramic bowl rim fragment, Trench 5, Level 3"
  description: >
    Red-slipped pottery sherd with geometric incised decoration.
    Bowl rim fragment with 15cm estimated diameter.
    Fine-grained clay matrix with minimal tempering.
  sample_identifier: "CATAL-2023-T5-L3-P001"

# === SAMPLING EVENT NODE ===
event_excavation_001:
  otype: SamplingEvent
  pid: "event:catal-2023-t5-l3"
  label: "Çatalhöyük 2023, Trench 5, Level 3"
  description: >
    Systematic excavation of Neolithic domestic structure.
    Level 3 represents occupation phase dated 6500-6400 BCE.
    Standard archaeological excavation methodology with 3D recording.
  result_time: "2023-07-15T14:30:00Z"
  has_feature_of_interest: "Neolithic architectural feature: building floor"
  project: "Çatalhöyük Research Project"

# === SAMPLING SITE NODE ===
site_catalhoyuk:
  otype: SamplingSite
  pid: "site:catalhoyuk-south-area"
  label: "Çatalhöyük South Area"
  description: >
    Neolithic settlement mound in central Anatolia, Turkey.
    UNESCO World Heritage Site. Occupied 7100-5950 BCE.
  place_name:
    - "Çatalhöyük"
    - "Çatal Höyük"
    - "Chatal Huyuk"

# === GEOSPATIAL COORDINATE NODES ===
coords_site:
  otype: GeospatialCoordLocation
  pid: "coords:catalhoyuk-site-center"
  latitude: 37.666
  longitude: 32.827
  elevation: "1000 m above mean sea level"
  obfuscated: false

coords_sample:
  otype: GeospatialCoordLocation
  pid: "coords:catal-2023-t5-l3-p001"
  latitude: 37.6665
  longitude: 32.8274
  elevation: "3.2 m below surface"
  obfuscated: false

# === IDENTIFIED CONCEPT NODES ===
concept_earthenware:
  otype: IdentifiedConcept
  pid: "https://w3id.org/isample/vocabulary/material/0.9/earthenware"
  label: "Earthenware"
  scheme_name: "iSamples Material Type Vocabulary"
  scheme_uri: "https://w3id.org/isample/vocabulary/material/"

concept_archaeological:
  otype: IdentifiedConcept
  pid: "https://w3id.org/isample/vocabulary/sampledfeature/0.9/terrestrial_archaeological"
  label: "Terrestrial environment > Archaeological site"
  scheme_name: "iSamples Sampled Feature Vocabulary"

concept_sherd:
  otype: IdentifiedConcept
  pid: "https://w3id.org/isample/vocabulary/materialsampleobjecttype/0.9/sherd"
  label: "Sherd"
  scheme_name: "iSamples Material Sample Object Type Vocabulary"

keyword_neolithic:
  otype: IdentifiedConcept
  pid: "keyword:neolithic"
  label: "Neolithic"

keyword_pottery:
  otype: IdentifiedConcept
  pid: "keyword:pottery"
  label: "Pottery"

keyword_redslipped:
  otype: IdentifiedConcept
  pid: "keyword:red-slipped-ware"
  label: "Red-slipped ware"

# === AGENT NODES ===
agent_collector:
  otype: Agent
  pid: "https://orcid.org/0000-0002-1234-5678"
  name: "Dr. Sarah Johnson"
  affiliation: "University of Cambridge, McDonald Institute"
  contact_information: "sjohnson@cam.ac.uk"
  role: "Field Supervisor"

agent_registrant:
  otype: Agent
  pid: "agent:opencontext-curator"
  name: "OpenContext Data Team"
  affiliation: "The Alexandria Archive Institute"
  contact_information: "info@opencontext.org"
  role: "Data Curator"

# === EDGES ===
# Sample → Event
edge_produced_by:
  otype: _edge_
  s: sample_pottery_001
  p: produced_by
  o: [event_excavation_001]

# Event → Site
edge_sampling_site:
  otype: _edge_
  s: event_excavation_001
  p: sampling_site
  o: [site_catalhoyuk]

# Site → Site Coordinates
edge_site_location:
  otype: _edge_
  s: site_catalhoyuk
  p: site_location
  o: [coords_site]

# Event → Sample Coordinates
edge_sample_location:
  otype: _edge_
  s: event_excavation_001
  p: sample_location
  o: [coords_sample]

# Event → Collector
edge_responsibility:
  otype: _edge_
  s: event_excavation_001
  p: responsibility
  o: [agent_collector]

# Sample → Material Type
edge_material:
  otype: _edge_
  s: sample_pottery_001
  p: has_material_category
  o: [concept_earthenware]

# Sample → Context
edge_context:
  otype: _edge_
  s: sample_pottery_001
  p: has_context_category
  o: [concept_archaeological]

# Sample → Object Type
edge_object_type:
  otype: _edge_
  s: sample_pottery_001
  p: has_sample_object_type
  o: [concept_sherd]

# Sample → Keywords (multivalued)
edge_keyword_1:
  otype: _edge_
  s: sample_pottery_001
  p: keywords
  o: [keyword_neolithic]

edge_keyword_2:
  otype: _edge_
  s: sample_pottery_001
  p: keywords
  o: [keyword_pottery]

edge_keyword_3:
  otype: _edge_
  s: sample_pottery_001
  p: keywords
  o: [keyword_redslipped]

# Sample → Registrant
edge_registrant:
  otype: _edge_
  s: sample_pottery_001
  p: registrant
  o: [agent_registrant]
```

### Archaeology-Specific Patterns

**What's unique:**
- Heavy use of **keywords** for taxonomic and cultural terms
- **Detailed site names** (place_name with multiple spellings)
- **Depth measurements** instead of elevation ("3.2 m below surface")
- **Cultural periods** in keywords (Neolithic, Bronze Age, etc.)
- **No curation information** (samples often remain at excavation sites)

**Edge types used:** 10 of 14
- ✅ produced_by, has_material_category, has_context_category, has_sample_object_type
- ✅ keywords, registrant, sampling_site, sample_location, responsibility (Event), site_location
- ❌ curation, related_resource, has_context_category (Event), responsibility (Curation)

---

## Geology (SESAR - Projected)

**Data Source:** SESAR (System for Earth Sample Registration)
**Dataset Size:** ~1M+ rock, mineral, and sediment samples
**Primary Domain:** Earth sciences, petrology, geochemistry

### Sample Profile: Basalt Core from Mid-Ocean Ridge

#### Complete Graph Structure

```
MaterialSampleRecord (Basalt Core)
  ├─ produced_by ───────→ SamplingEvent (2023 Drilling)
  │                           ├─ sample_location ──→ GeospatialCoordLocation (45.5°N, -130.2°W, -2500m depth)
  │                           └─ responsibility ───→ Agent (Dr. Maria Rodriguez)
  │
  ├─ has_material_category ─→ IdentifiedConcept (Basalt)
  ├─ has_context_category ──→ IdentifiedConcept (Marine water body)
  ├─ has_sample_object_type ─→ IdentifiedConcept (Core)
  ├─ keywords ──────────────→ IdentifiedConcept (MORB - Mid-Ocean Ridge Basalt)
  ├─ curation ──────────────→ MaterialSampleCuration (Lamont Core Repository)
  │                               └─ responsibility ───→ Agent (Core Facility Manager)
  └─ registrant ────────────→ Agent (SESAR Data Manager)
```

#### Full YAML Example

```yaml
# === SAMPLE NODE ===
sample_basalt_core:
  otype: MaterialSampleRecord
  pid: "igsn:IESEA0001"
  label: "Basalt core from Juan de Fuca Ridge"
  description: >
    Fresh basalt core, 6cm diameter, 15cm length.
    Holocrystalline texture with plagioclase and pyroxene phenocrysts.
    Collected from pillow basalt at mid-ocean ridge spreading center.
  sample_identifier: "JDFR-2023-DR-001-C1"

# === SAMPLING EVENT NODE ===
event_drilling:
  otype: SamplingEvent
  pid: "event:jdfr-2023-dredge-001"
  label: "Juan de Fuca Ridge Dredge 001, 2023"
  description: >
    Rock dredge operation from R/V Thompson.
    Dredge deployed at 2500m depth on ridge axis.
    Standard petrological sampling protocol.
  result_time: "2023-08-22T10:45:00Z"
  has_feature_of_interest: "Mid-ocean ridge basalt outcrop"
  project: "NSF OCE-2023456: Juan de Fuca Ridge Magmatic Evolution"

# === GEOSPATIAL COORDINATE NODE ===
coords_sample:
  otype: GeospatialCoordLocation
  pid: "coords:jdfr-2023-dr-001"
  latitude: 45.5
  longitude: -130.2
  elevation: "-2500 m below sea level"
  obfuscated: false

# === IDENTIFIED CONCEPT NODES ===
concept_basalt:
  otype: IdentifiedConcept
  pid: "https://w3id.org/isample/vocabulary/material/0.9/basalt"
  label: "Basalt"
  scheme_name: "iSamples Material Type Vocabulary"

concept_marine:
  otype: IdentifiedConcept
  pid: "https://w3id.org/isample/vocabulary/sampledfeature/0.9/marinewaterbody"
  label: "Marine water body"
  scheme_name: "iSamples Sampled Feature Vocabulary"

concept_core:
  otype: IdentifiedConcept
  pid: "https://w3id.org/isample/vocabulary/materialsampleobjecttype/0.9/core"
  label: "Core"
  scheme_name: "iSamples Material Sample Object Type Vocabulary"

keyword_morb:
  otype: IdentifiedConcept
  pid: "keyword:morb"
  label: "MORB"
  description: "Mid-Ocean Ridge Basalt"

# === AGENT NODES ===
agent_collector:
  otype: Agent
  pid: "https://orcid.org/0000-0003-5678-9012"
  name: "Dr. Maria Rodriguez"
  affiliation: "Scripps Institution of Oceanography"
  role: "Chief Scientist"

agent_curator:
  otype: Agent
  pid: "agent:lamont-core-manager"
  name: "James Chen"
  affiliation: "Lamont-Doherty Core Repository"
  role: "Core Facility Manager"

agent_registrant:
  otype: Agent
  pid: "agent:sesar-manager"
  name: "SESAR Data Management Team"
  affiliation: "Lamont-Doherty Earth Observatory"
  role: "Sample Registry Manager"

# === CURATION NODE ===
curation_lamont:
  otype: MaterialSampleCuration
  pid: "curation:lamont-core-repo"
  label: "Lamont-Doherty Core Repository"
  description: >
    World-class marine core repository.
    Temperature-controlled storage, 4°C.
    Catalog available online.
  curation_location: "Lamont-Doherty Earth Observatory, Palisades, NY"
  access_constraints: "Request access via SESAR portal. Sampling approval required."

# === EDGES ===
edge_produced_by:
  s: sample_basalt_core
  p: produced_by
  o: [event_drilling]

edge_sample_location:
  s: event_drilling
  p: sample_location
  o: [coords_sample]

edge_responsibility_event:
  s: event_drilling
  p: responsibility
  o: [agent_collector]

edge_material:
  s: sample_basalt_core
  p: has_material_category
  o: [concept_basalt]

edge_context:
  s: sample_basalt_core
  p: has_context_category
  o: [concept_marine]

edge_object_type:
  s: sample_basalt_core
  p: has_sample_object_type
  o: [concept_core]

edge_keyword:
  s: sample_basalt_core
  p: keywords
  o: [keyword_morb]

edge_curation:
  s: sample_basalt_core
  p: curation
  o: [curation_lamont]

edge_curation_responsibility:
  s: curation_lamont
  p: responsibility
  o: [agent_curator]

edge_registrant:
  s: sample_basalt_core
  p: registrant
  o: [agent_registrant]
```

### Geology-Specific Patterns

**What's unique:**
- Heavy use of **curation** (samples stored in repositories)
- **Negative elevations** for marine samples ("-2500 m below sea level")
- **Formal project identifiers** (NSF grant numbers)
- **Repository access constraints** (destructive sampling approval)
- **Less use of keywords** (more reliance on formal material classification)

**Edge types used (projected):** 10 of 14
- ✅ produced_by, has_material_category, has_context_category, has_sample_object_type
- ✅ keywords, registrant, curation, responsibility (Event), responsibility (Curation), sample_location
- ❌ related_resource, sampling_site, site_location, has_context_category (Event)

---

## Biology (GEOME - Projected)

**Data Source:** GEOME (Genomic Observatories Metadatabase)
**Dataset Size:** ~100K+ tissue and DNA samples from marine organisms
**Primary Domain:** Marine biology, genomics, biodiversity

### Sample Profile: Coral Tissue Sample from Pacific Reef

#### Complete Graph Structure

```
MaterialSampleRecord (Tissue Sample)
  ├─ produced_by ───────→ SamplingEvent (2024 Field Collection)
  │                           ├─ sampling_site ───→ SamplingSite (Palmyra Atoll Reef)
  │                           │                         └─ site_location ───→ GeospatialCoordLocation (5.87°N, -162.08°W)
  │                           ├─ sample_location ──→ GeospatialCoordLocation (5.8715°N, -162.0823°W)
  │                           └─ responsibility ───→ Agent (Dr. Carlos Alvarez)
  │
  ├─ has_material_category ─→ IdentifiedConcept (Organic material > Tissue)
  ├─ has_context_category ──→ IdentifiedConcept (Marine > Marine biome)
  ├─ has_sample_object_type ─→ IdentifiedConcept (Specimen)
  ├─ keywords ──────────────→ IdentifiedConcept (Pocillopora damicornis)
  ├─ keywords ──────────────→ IdentifiedConcept (Coral)
  ├─ keywords ──────────────→ IdentifiedConcept (Scleractinia)
  ├─ related_resource ──────→ SampleRelation (Derived DNA extract)
  └─ registrant ────────────→ Agent (GEOME Data Manager)

# DNA extract linked via SampleRelation
MaterialSampleRecord (DNA Extract)
  └─ related_resource ──────→ SampleRelation (Derived from tissue)
```

#### Full YAML Example

```yaml
# === PARENT SAMPLE (TISSUE) ===
sample_tissue:
  otype: MaterialSampleRecord
  pid: "igsn:IEGEN0001"
  label: "Pocillopora damicornis tissue, Palmyra Atoll"
  description: >
    Tissue sample from branching coral colony.
    Approximately 1cm³ tissue preserved in 95% ethanol.
    Colony health: excellent. No visible bleaching.
  sample_identifier: "PALM-2024-CORAL-001-T"

# === CHILD SAMPLE (DNA EXTRACT) ===
sample_dna:
  otype: MaterialSampleRecord
  pid: "igsn:IEGEN0002"
  label: "DNA extract from Pocillopora damicornis tissue PALM-2024-CORAL-001-T"
  description: >
    High molecular weight DNA extracted using Qiagen DNeasy kit.
    Concentration: 45 ng/µL. 260/280 ratio: 1.82.
  sample_identifier: "PALM-2024-CORAL-001-DNA"

# === SAMPLING EVENT ===
event_collection:
  otype: SamplingEvent
  pid: "event:palmyra-2024-dive-005"
  label: "Palmyra Atoll 2024, Dive 005"
  description: >
    SCUBA collection at 12m depth.
    Reef flat dominated by Pocillopora and Porites.
    Minimal impact sampling protocol (1cm² fragments).
  result_time: "2024-06-15T11:20:00Z"
  has_feature_of_interest: "Coral reef ecosystem"
  project: "NSF OCE-2024123: Pacific Coral Genomics"

# === SAMPLING SITE ===
site_palmyra:
  otype: SamplingSite
  pid: "site:palmyra-atoll-reef"
  label: "Palmyra Atoll, Fore Reef Site A"
  description: >
    Pristine coral reef system. U.S. National Wildlife Refuge.
    High coral cover (>50%). Minimal anthropogenic impact.
  place_name:
    - "Palmyra Atoll"
    - "Palmyra Island"

# === GEOSPATIAL COORDINATES ===
coords_site:
  otype: GeospatialCoordLocation
  pid: "coords:palmyra-site-a"
  latitude: 5.87
  longitude: -162.08
  elevation: "-12 m below sea level (dive depth)"
  obfuscated: false

coords_sample:
  otype: GeospatialCoordLocation
  pid: "coords:palmyra-dive-005-001"
  latitude: 5.8715
  longitude: -162.0823
  elevation: "-12 m below sea level"
  obfuscated: false

# === IDENTIFIED CONCEPTS ===
concept_tissue:
  otype: IdentifiedConcept
  pid: "https://w3id.org/isample/vocabulary/material/0.9/organicmaterial"
  label: "Organic material > Tissue"
  scheme_name: "iSamples Material Type Vocabulary"

concept_marine_biome:
  otype: IdentifiedConcept
  pid: "https://w3id.org/isample/vocabulary/sampledfeature/0.9/marinebiome"
  label: "Marine biome"
  scheme_name: "iSamples Sampled Feature Vocabulary"

concept_specimen:
  otype: IdentifiedConcept
  pid: "https://w3id.org/isample/vocabulary/materialsampleobjecttype/0.9/specimen"
  label: "Specimen"
  scheme_name: "iSamples Material Sample Object Type Vocabulary"

keyword_species:
  otype: IdentifiedConcept
  pid: "taxon:pocillopora-damicornis"
  label: "Pocillopora damicornis"
  description: "Cauliflower coral"

keyword_coral:
  otype: IdentifiedConcept
  pid: "keyword:coral"
  label: "Coral"

keyword_scleractinia:
  otype: IdentifiedConcept
  pid: "taxon:scleractinia"
  label: "Scleractinia"
  description: "Stony corals"

# === AGENTS ===
agent_collector:
  otype: Agent
  pid: "https://orcid.org/0000-0001-9876-5432"
  name: "Dr. Carlos Alvarez"
  affiliation: "University of Hawaiʻi, Hawaiʻi Institute of Marine Biology"
  role: "Principal Investigator"

agent_registrant:
  otype: Agent
  pid: "agent:geome-manager"
  name: "GEOME Data Team"
  affiliation: "Smithsonian Institution"
  role: "Genomic Data Manager"

# === SAMPLE RELATION (PARENT-CHILD) ===
relation_dna_extract:
  otype: SampleRelation
  pid: "relation:tissue-to-dna-001"
  label: "DNA extracted from tissue"
  description: "High molecular weight DNA extraction for whole genome sequencing"
  relationship: "derivedFrom"
  target: "igsn:IEGEN0001"  # Points to parent tissue sample

# === EDGES ===
# Tissue sample edges
edge_tissue_event:
  s: sample_tissue
  p: produced_by
  o: [event_collection]

edge_tissue_material:
  s: sample_tissue
  p: has_material_category
  o: [concept_tissue]

edge_tissue_context:
  s: sample_tissue
  p: has_context_category
  o: [concept_marine_biome]

edge_tissue_object:
  s: sample_tissue
  p: has_sample_object_type
  o: [concept_specimen]

edge_tissue_keyword1:
  s: sample_tissue
  p: keywords
  o: [keyword_species]

edge_tissue_keyword2:
  s: sample_tissue
  p: keywords
  o: [keyword_coral]

edge_tissue_keyword3:
  s: sample_tissue
  p: keywords
  o: [keyword_scleractinia]

edge_tissue_registrant:
  s: sample_tissue
  p: registrant
  o: [agent_registrant]

# DNA sample → parent tissue relationship
edge_dna_relation:
  s: sample_dna
  p: related_resource
  o: [relation_dna_extract]

# Event edges
edge_event_site:
  s: event_collection
  p: sampling_site
  o: [site_palmyra]

edge_event_location:
  s: event_collection
  p: sample_location
  o: [coords_sample]

edge_event_responsibility:
  s: event_collection
  p: responsibility
  o: [agent_collector]

# Site edges
edge_site_location:
  s: site_palmyra
  p: site_location
  o: [coords_site]
```

### Biology-Specific Patterns

**What's unique:**
- Heavy use of **related_resource** (tissue → DNA → sequence data)
- **Taxonomic keywords** (species names, higher taxa)
- **Preservation methods** in descriptions ("95% ethanol")
- **Sample chains** (organism → tissue → extract → library)
- **Precise dive/collection coordinates**

**Edge types used (projected):** 11 of 14
- ✅ produced_by, has_material_category, has_context_category, has_sample_object_type
- ✅ keywords, registrant, related_resource, sampling_site, sample_location, responsibility (Event), site_location
- ❌ curation, has_context_category (Event), responsibility (Curation)

---

## Cross-Domain Comparison

### Entity Usage Comparison

| Entity Type | Archaeology | Geology | Biology |
|-------------|-------------|---------|---------|
| MaterialSampleRecord | Pottery, bone, charcoal | Rocks, cores, minerals | Tissue, DNA, specimens |
| SamplingEvent | Excavation, surface collection | Drilling, dredging | SCUBA, trap, net |
| SamplingSite | Archaeological sites | Formations, localities | Reefs, stations, plots |
| GeospatialCoordLocation | Depth below surface | Depth below sea level | Depth below sea level |
| IdentifiedConcept | Cultural periods, pottery types | Rock types, minerals | Taxa, specimen types |
| Agent | Archaeologists, curators | Geologists, repository staff | Marine biologists, geneticists |
| MaterialSampleCuration | Rarely used | Core repositories | Biobanks, tissue collections |
| SampleRelation | Rare | Rare | Common (parent-child chains) |

### Predicate Usage Comparison

| Predicate | Archaeology | Geology | Biology |
|-----------|-------------|---------|---------|
| produced_by | ✅ Every sample | ✅ Every sample | ✅ Every sample |
| has_material_category | Pottery, bone, stone | Basalt, granite, sediment | Tissue, DNA, whole organism |
| has_context_category | Terrestrial/Archaeological | Marine, Terrestrial, Subsurface | Marine biome, Terrestrial |
| has_sample_object_type | Sherd, artifact | Core, hand specimen | Specimen, tissue |
| keywords | Cultural terms, periods | Rock types, formation names | Taxonomic names |
| registrant | ✅ Common | ✅ Common | ✅ Common |
| curation | ❌ Rare | ✅ Very common | ⚪ Sometimes |
| related_resource | ❌ Rare | ❌ Rare | ✅ Very common |
| sampling_site | ✅ Common (site names) | ⚪ Sometimes | ✅ Common (stations, reefs) |
| sample_location | ✅ Very common | ✅ Very common | ✅ Very common |
| responsibility (Event) | ✅ Common | ✅ Common | ✅ Common |
| has_context_category (Event) | ❌ Not used | ❌ Not used | ❌ Not used |
| site_location | ✅ Common | ⚪ Sometimes | ✅ Common |
| responsibility (Curation) | ❌ Not used | ✅ Common | ⚪ Sometimes |

### Material Type Patterns

**Archaeology:**
- Anthropogenic material (pottery, glass, metal)
- Organic material (bone, charcoal, wood)
- Rock (stone tools, building materials)
- Soil (sediment samples)

**Geology:**
- Rock (igneous, sedimentary, metamorphic)
- Mineral (individual mineral specimens)
- Sediment (unconsolidated material)
- Fluid (water, hydrothermal fluids)

**Biology:**
- Organic material (tissue, DNA, whole organisms)
- Liquid water (seawater, freshwater samples)
- Biogenic non-organic material (shells, coral skeleton)

---

## Domain-Specific Patterns

### Pattern 1: Archaeological Depth Notation

**Challenge:** Archaeologists measure depth **below surface**, not elevation above sea level.

**Solution:** Use elevation field with descriptive text:
```yaml
elevation: "3.2 m below surface"
elevation: "Level 5, 4.8 m below datum"
```

### Pattern 2: Marine Sample Depths

**Challenge:** Marine samples need **negative elevation** (below sea level).

**Solution:**
```yaml
elevation: "-2500 m below sea level"
elevation: "-12 m (dive depth)"
```

### Pattern 3: Sample Chains (Biology)

**Challenge:** Tissue → DNA → Sequencing Library are all samples.

**Solution:** Use `related_resource` with `derivedFrom` relationship:
```yaml
# DNA sample points to tissue parent
dna_sample:
  related_resource:
    - relationship: "derivedFrom"
      target: "igsn:TISSUE001"

# Sequencing library points to DNA parent
library_sample:
  related_resource:
    - relationship: "derivedFrom"
      target: "igsn:DNA001"
```

### Pattern 4: Repository Storage (Geology)

**Challenge:** Core samples stored in repositories with access constraints.

**Solution:** Use `curation` entity:
```yaml
sample:
  curation:
    label: "Lamont-Doherty Core Repository"
    curation_location: "Palisades, NY"
    access_constraints: "Destructive sampling requires approval"
    responsibility:
      - name: "Core Facility Manager"
```

### Pattern 5: Multi-lingual Site Names (Archaeology)

**Challenge:** Archaeological sites have multiple name spellings.

**Solution:** Use `place_name` array:
```yaml
site:
  place_name:
    - "Çatalhöyük"
    - "Çatal Höyük"
    - "Chatal Huyuk"
    - "جاتال هويوك"  # Arabic
```

---

## Summary

**Key Takeaways:**

1. **Same schema, different values** - The iSamples model truly works across domains
2. **10-11 of 14 predicates used per domain** - Different domains use different subsets
3. **Context category distinguishes domains** - Terrestrial/Archaeological vs Marine biome vs Subsurface
4. **Material category is domain-specific** - Pottery vs Basalt vs Tissue
5. **Curation patterns differ** - Geology stores cores, archaeology often doesn't track storage
6. **Related_resource is biology-heavy** - Sample chains common in genomics, rare elsewhere

**Design Wisdom:**

✅ **Universal model:** 8 entity types work across all domains
✅ **Flexible values:** Controlled vocabularies adapt to domain needs
✅ **Optional predicates:** Each domain uses relevant subset
✅ **Extensible:** Can add domain-specific keywords without schema changes

**Next steps:**
- [QUERYING_THE_GRAPH.md](./QUERYING_THE_GRAPH.md) - SQL patterns for cross-domain queries
- [EDGE_TYPES_VISUAL.md](./EDGE_TYPES_VISUAL.md) - Visual diagrams of patterns

---

**Document Version:** 1.0
**Last Updated:** 2025-11-14
**Schema Version:** 20250207 (MaterialSampleRecord)
**Author:** Claude Code (Sonnet 4.5)

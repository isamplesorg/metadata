# iSamples Predicates Reference

**Purpose:** Detailed reference for each of the 14 relationship types (predicates) in the iSamples property graph.

**Audience:** Developers querying iSamples data, data providers creating metadata, tool builders integrating with iSamples.

> **Note on "Required" vs "Strongly Recommended":** The LinkML schema only marks `pid`, `label`, and `last_modified_time` as technically required fields. However, for meaningful PQG data and cross-domain interoperability, certain predicates are **strongly recommended**. These are marked with 🔶 below.

---

## Quick Reference Table

| Predicate | Subject → Object | Cardinality | Required | Description |
|-----------|------------------|-------------|----------|-------------|
| [produced_by](#produced_by) | MaterialSampleRecord → SamplingEvent | One | 🔶 Strongly Recommended | Sample creation event |
| [has_material_category](#has_material_category) | MaterialSampleRecord → IdentifiedConcept | Many | 🔶 Strongly Recommended | Material type |
| [has_context_category](#has_context_category) | MaterialSampleRecord → IdentifiedConcept | Many | 🔶 Strongly Recommended | Domain context |
| [has_sample_object_type](#has_sample_object_type) | MaterialSampleRecord → IdentifiedConcept | Many | 🔶 Strongly Recommended | Physical form |
| [keywords](#keywords) | MaterialSampleRecord → IdentifiedConcept | Many | ⚪ No | Discovery keywords |
| [registrant](#registrant) | MaterialSampleRecord → Agent | One | ⚪ No | Registering agent |
| [curation](#curation) | MaterialSampleRecord → MaterialSampleCuration | One | ⚪ No | Storage info |
| [related_resource](#related_resource) | MaterialSampleRecord → SampleRelation | Many | ⚪ No | Sample relationships |
| [sampling_site](#sampling_site) | SamplingEvent → SamplingSite | One | ⚪ No | Named location |
| [sample_location](#sample_location) | SamplingEvent → GeospatialCoordLocation | One | ⚪ No | Precise coords |
| [responsibility](#responsibility-samplingevent) | SamplingEvent → Agent | Many | ⚪ No | Collectors |
| [has_context_category](#has_context_category-samplingevent) | SamplingEvent → IdentifiedConcept | Many | ⚪ No | Event context |
| [site_location](#site_location) | SamplingSite → GeospatialCoordLocation | One | ⚪ No | Site coords |
| [responsibility](#responsibility-materialsamplecuration) | MaterialSampleCuration → Agent | Many | ⚪ No | Curators |

---

## MaterialSampleRecord Predicates

### produced_by

**Type:** MaterialSampleRecord → SamplingEvent
**Cardinality:** One
**Required:** 🔶 Strongly Recommended (essential for provenance)

#### Purpose
Links a material sample to the event that created/collected it. This is the **most important relationship** in iSamples - every sample should have provenance for meaningful interoperability.

#### Controlled Vocabulary
Not applicable - targets a SamplingEvent node.

#### Usage Example

**YAML:**
```yaml
# Sample node
sample_001:
  otype: MaterialSampleRecord
  pid: "igsn:SSH000001"
  label: "Pottery sherd from Trench 5"

# Event node
event_001:
  otype: SamplingEvent
  pid: "event:2023-catal-t5-001"
  label: "2023 Excavation, Trench 5, Level 3"
  result_time: "2023-07-15"

# Edge
edge_001:
  otype: _edge_
  s: sample_001  # Subject: the sample
  p: produced_by # Predicate
  o: [event_001] # Object: the event
```

#### SQL Query Pattern

**Find all samples and their collection dates:**
```sql
SELECT
    sample.pid AS sample_id,
    sample.label AS sample_label,
    event.pid AS event_id,
    event.label AS event_label,
    event.result_time AS collection_date
FROM pqg AS sample
JOIN pqg AS edge
    ON edge.s = sample.row_id
    AND edge.p = 'produced_by'
    AND edge.otype = '_edge_'
JOIN pqg AS event
    ON event.row_id = ANY(edge.o)
WHERE sample.otype = 'MaterialSampleRecord';
```

**Find samples collected in a specific time range:**
```sql
SELECT
    sample.pid,
    sample.label,
    event.result_time
FROM pqg AS sample
JOIN pqg AS edge ON edge.s = sample.row_id AND edge.p = 'produced_by'
JOIN pqg AS event ON event.row_id = ANY(edge.o)
WHERE sample.otype = 'MaterialSampleRecord'
  AND event.result_time BETWEEN '2023-01-01' AND '2023-12-31';
```

#### OpenContext Data Stats
- **Frequency:** 1,096,352 relationships (one per sample)
- **Unique subjects:** 1,096,352 samples
- **Unique objects:** 1,096,352 events (1:1 ratio)

#### Common Issues

❌ **Missing produced_by:**
```
Error: MaterialSampleRecord must have produced_by relationship
```
**Solution:** Every sample requires a SamplingEvent.

❌ **Multiple produced_by:**
```
Warning: Sample has multiple produced_by edges (should be one)
```
**Solution:** Cardinality is ONE - use `related_resource` to link derived samples.

---

### has_material_category

**Type:** MaterialSampleRecord → IdentifiedConcept
**Cardinality:** Many (required, minimum 1)
**Required:** ✅ Yes

#### Purpose
Classifies the physical material composition of the sample. Uses controlled vocabulary from iSamples Material Type Vocabulary.

#### Controlled Vocabulary
[iSamples Material Type Vocabulary](https://w3id.org/isample/vocabulary/material/)

**Top-level categories:**
- Rock
- Mineral
- Organic material
- Liquid water
- Anthropogenic material (includes pottery, glass, metals)
- Biogenic non-organic material
- Natural solid material
- Soil
- Particulate
- Fluid (non-water)

**Example subcategories:**
- Rock → Igneous rock → Basalt
- Anthropogenic material → Pottery → Earthenware
- Organic material → Tissue → Bone

#### Usage Example

**YAML:**
```yaml
# Sample node
sample_001:
  otype: MaterialSampleRecord
  pid: "igsn:SSH000001"
  label: "Ceramic bowl"

# Concept nodes (from controlled vocabulary)
concept_earthenware:
  otype: IdentifiedConcept
  pid: "https://w3id.org/isample/vocabulary/material/0.9/earthenware"
  label: "Earthenware"
  scheme_name: "iSamples Material Type Vocabulary"

concept_anthropogenic:
  otype: IdentifiedConcept
  pid: "https://w3id.org/isample/vocabulary/material/0.9/anthropogenicmaterial"
  label: "Anthropogenic material"

# Edges (multivalued - can have multiple material types)
edge_001:
  s: sample_001
  p: has_material_category
  o: [concept_earthenware]

edge_002:
  s: sample_001
  p: has_material_category
  o: [concept_anthropogenic]
```

#### SQL Query Pattern

**Find all samples of a specific material type:**
```sql
SELECT
    sample.pid,
    sample.label,
    concept.label AS material_type
FROM pqg AS sample
JOIN pqg AS edge
    ON edge.s = sample.row_id
    AND edge.p = 'has_material_category'
JOIN pqg AS concept
    ON concept.row_id = ANY(edge.o)
WHERE sample.otype = 'MaterialSampleRecord'
  AND concept.label ILIKE '%earthenware%';
```

**Count samples by material type:**
```sql
SELECT
    concept.label AS material_type,
    COUNT(DISTINCT sample.pid) AS sample_count
FROM pqg AS sample
JOIN pqg AS edge ON edge.s = sample.row_id AND edge.p = 'has_material_category'
JOIN pqg AS concept ON concept.row_id = ANY(edge.o)
WHERE sample.otype = 'MaterialSampleRecord'
GROUP BY concept.label
ORDER BY sample_count DESC;
```

#### OpenContext Data Stats
- **Frequency:** 1,096,352 relationships
- **Unique subjects:** 1,096,352 samples (one per sample)
- **Unique objects:** 10 material type concepts

**Top material types in OpenContext:**
1. Anthropogenic material (pottery, artifacts)
2. Rock (stone tools, building materials)
3. Organic material (bone, charcoal)
4. Soil (sediment samples)

#### Common Issues

❌ **Using free text instead of controlled vocabulary:**
```yaml
# Wrong:
has_material_category: "pottery"

# Right:
has_material_category:
  - pid: "https://w3id.org/isample/vocabulary/material/0.9/earthenware"
    label: "Earthenware"
```

---

### has_context_category

**Type:** MaterialSampleRecord → IdentifiedConcept
**Cardinality:** Many (required, minimum 1)
**Required:** ✅ Yes

#### Purpose
Classifies the broad context or sampled feature type. Indicates the domain (archaeology, marine biology, geology, etc.) and environment.

#### Controlled Vocabulary
[iSamples Sampled Feature Vocabulary](https://w3id.org/isample/vocabulary/sampledfeature/)

**Top-level categories:**
- Terrestrial environment
  - Archaeological
  - Subsurface
  - Surface
- Marine environment
  - Marine biome
  - Marine water body
  - Submerged terrestrial
- Atmosphere
- Extraterrestrial
- Laboratory or production environment

#### Usage Example

**YAML:**
```yaml
sample_001:
  otype: MaterialSampleRecord
  pid: "igsn:SSH000001"

concept_archaeological:
  otype: IdentifiedConcept
  pid: "https://w3id.org/isample/vocabulary/sampledfeature/0.9/terrestrial_archaeological"
  label: "Terrestrial environment > Archaeological site"
  scheme_name: "iSamples Sampled Feature Vocabulary"

edge:
  s: sample_001
  p: has_context_category
  o: [concept_archaeological]
```

#### SQL Query Pattern

**Find all archaeological samples:**
```sql
SELECT
    sample.pid,
    sample.label,
    concept.label AS context
FROM pqg AS sample
JOIN pqg AS edge ON edge.s = sample.row_id AND edge.p = 'has_context_category'
JOIN pqg AS concept ON concept.row_id = ANY(edge.o)
WHERE sample.otype = 'MaterialSampleRecord'
  AND concept.label ILIKE '%archaeological%';
```

#### OpenContext Data Stats
- **Frequency:** 1,096,352 relationships
- **Unique subjects:** 1,096,352 samples
- **Unique objects:** 2 context concepts (OpenContext is archaeology-focused)

---

### has_sample_object_type

**Type:** MaterialSampleRecord → IdentifiedConcept
**Cardinality:** Many (required, minimum 1)
**Required:** ✅ Yes

#### Purpose
Describes the physical form or object type of the sample. Answers "What kind of object is this?"

#### Controlled Vocabulary
[iSamples Material Sample Object Type Vocabulary](https://w3id.org/isample/vocabulary/materialsampleobjecttype/)

**Common types:**
- Core
- Hand specimen
- Thin section
- Powder
- Cube
- Sherd (pottery fragment)
- Specimen (biological)
- Aggregate (multiple pieces)
- Other solid object

#### Usage Example

**YAML:**
```yaml
sample_001:
  otype: MaterialSampleRecord
  pid: "igsn:SSH000001"
  label: "Pottery fragment"

concept_sherd:
  otype: IdentifiedConcept
  pid: "https://w3id.org/isample/vocabulary/materialsampleobjecttype/0.9/sherd"
  label: "Sherd"
  scheme_name: "iSamples Material Sample Object Type Vocabulary"

edge:
  s: sample_001
  p: has_sample_object_type
  o: [concept_sherd]
```

#### SQL Query Pattern

**Find all core samples:**
```sql
SELECT
    sample.pid,
    sample.label,
    concept.label AS object_type
FROM pqg AS sample
JOIN pqg AS edge ON edge.s = sample.row_id AND edge.p = 'has_sample_object_type'
JOIN pqg AS concept ON concept.row_id = ANY(edge.o)
WHERE concept.label = 'Core';
```

#### OpenContext Data Stats
- **Frequency:** 1,096,352 relationships
- **Unique subjects:** 1,096,352 samples
- **Unique objects:** 5 object type concepts

---

### keywords

**Type:** MaterialSampleRecord → IdentifiedConcept
**Cardinality:** Many (optional)
**Required:** ⚪ No

#### Purpose
Free-text keywords for discovery and search. Can include taxonomic names, geographic terms, cultural periods, etc.

#### Controlled Vocabulary
Not strictly controlled - can use various vocabularies or free text wrapped in IdentifiedConcept.

#### Usage Example

**YAML:**
```yaml
sample_001:
  otype: MaterialSampleRecord
  pid: "igsn:SSH000001"

keyword_neolithic:
  otype: IdentifiedConcept
  pid: "keyword:neolithic"
  label: "Neolithic"

keyword_pottery:
  otype: IdentifiedConcept
  pid: "keyword:pottery"
  label: "Pottery"

keyword_catalhoyuk:
  otype: IdentifiedConcept
  pid: "keyword:catalhoyuk"
  label: "Çatalhöyük"

# Multiple edges for multiple keywords
edge_001:
  s: sample_001
  p: keywords
  o: [keyword_neolithic]

edge_002:
  s: sample_001
  p: keywords
  o: [keyword_pottery]

edge_003:
  s: sample_001
  p: keywords
  o: [keyword_catalhoyuk]
```

#### SQL Query Pattern

**Find samples with specific keyword:**
```sql
SELECT
    sample.pid,
    sample.label,
    concept.label AS keyword
FROM pqg AS sample
JOIN pqg AS edge ON edge.s = sample.row_id AND edge.p = 'keywords'
JOIN pqg AS concept ON concept.row_id = ANY(edge.o)
WHERE concept.label ILIKE '%neolithic%';
```

**Find samples with multiple keywords (AND logic):**
```sql
WITH sample_keywords AS (
  SELECT
    sample.pid,
    sample.label,
    concept.label AS keyword
  FROM pqg AS sample
  JOIN pqg AS edge ON edge.s = sample.row_id AND edge.p = 'keywords'
  JOIN pqg AS concept ON concept.row_id = ANY(edge.o)
)
SELECT pid, label
FROM sample_keywords
WHERE keyword IN ('Neolithic', 'Pottery')
GROUP BY pid, label
HAVING COUNT(DISTINCT keyword) = 2;
```

#### OpenContext Data Stats
- **Frequency:** 1,096,297 relationships (not all samples have keywords)
- **Unique subjects:** 1,096,297 samples
- **Unique objects:** 4,033 unique keyword concepts

---

### registrant

**Type:** MaterialSampleRecord → Agent
**Cardinality:** One (optional)
**Required:** ⚪ No

#### Purpose
Identifies the person or organization that registered the sample metadata.

#### Usage Example

**YAML:**
```yaml
sample_001:
  otype: MaterialSampleRecord
  pid: "igsn:SSH000001"

agent_curator:
  otype: Agent
  pid: "https://orcid.org/0000-0002-1234-5678"
  name: "Jane Smith"
  affiliation: "OpenContext"
  role: "Data Curator"

edge:
  s: sample_001
  p: registrant
  o: [agent_curator]
```

#### SQL Query Pattern

**Find all samples registered by a specific person:**
```sql
SELECT
    sample.pid,
    sample.label,
    agent.name AS registrant_name
FROM pqg AS sample
JOIN pqg AS edge ON edge.s = sample.row_id AND edge.p = 'registrant'
JOIN pqg AS agent ON agent.row_id = ANY(edge.o)
WHERE agent.name ILIKE '%smith%';
```

#### OpenContext Data Stats
- **Frequency:** 413,635 relationships (38% of samples)
- **Unique subjects:** 413,635 samples
- **Unique objects:** 340 agents

---

### curation

**Type:** MaterialSampleRecord → MaterialSampleCuration
**Cardinality:** One (optional)
**Required:** ⚪ No

#### Purpose
Links sample to its curation information (storage location, access constraints, curation history).

#### Usage Example

**YAML:**
```yaml
sample_001:
  otype: MaterialSampleRecord
  pid: "igsn:SSH000001"

curation_001:
  otype: MaterialSampleCuration
  pid: "curation:smithsonian-nmnh-001"
  label: "Smithsonian NMNH Anthropology Collection"
  curation_location: "National Museum of Natural History, Washington DC"
  access_constraints: "Appointment required"

edge:
  s: sample_001
  p: curation
  o: [curation_001]
```

#### SQL Query Pattern

**Find samples stored at specific location:**
```sql
SELECT
    sample.pid,
    sample.label,
    curation.label AS collection_name,
    curation.curation_location
FROM pqg AS sample
JOIN pqg AS edge ON edge.s = sample.row_id AND edge.p = 'curation'
JOIN pqg AS curation ON curation.row_id = ANY(edge.o)
WHERE curation.curation_location ILIKE '%smithsonian%';
```

#### OpenContext Data Stats
- **Frequency:** 0 (OpenContext does not track curation information)

---

### related_resource

**Type:** MaterialSampleRecord → SampleRelation
**Cardinality:** Many (optional)
**Required:** ⚪ No

#### Purpose
Links sample to other samples via defined relationships (parent-child, sibling, etc.).

#### Usage Example

**YAML:**
```yaml
# Parent sample
parent_sample:
  otype: MaterialSampleRecord
  pid: "igsn:SSH000001"
  label: "Whole rock core"

# Child sample
child_sample:
  otype: MaterialSampleRecord
  pid: "igsn:SSH000002"
  label: "Thin section from core"

# Relation describing the connection
relation_001:
  otype: SampleRelation
  pid: "relation:subsample-001"
  label: "Thin section derived from core"
  relationship: "derivedFrom"
  target: "igsn:SSH000001"  # Points to parent

# Edge from child to relation
edge:
  s: child_sample
  p: related_resource
  o: [relation_001]
```

#### SQL Query Pattern

**Find all child samples of a parent:**
```sql
SELECT
    child.pid AS child_pid,
    child.label AS child_label,
    relation.relationship AS relation_type,
    parent.pid AS parent_pid,
    parent.label AS parent_label
FROM pqg AS child
JOIN pqg AS edge ON edge.s = child.row_id AND edge.p = 'related_resource'
JOIN pqg AS relation ON relation.row_id = ANY(edge.o)
JOIN pqg AS parent ON parent.pid = relation.target
WHERE parent.pid = 'igsn:SSH000001';
```

#### OpenContext Data Stats
- **Frequency:** 0 (OpenContext does not track sample relationships)

---

## SamplingEvent Predicates

### sampling_site

**Type:** SamplingEvent → SamplingSite
**Cardinality:** One (optional)
**Required:** ⚪ No

#### Purpose
Links sampling event to a named sampling site.

#### Usage Example

**YAML:**
```yaml
event_001:
  otype: SamplingEvent
  pid: "event:2023-catal-001"

site_001:
  otype: SamplingSite
  pid: "site:catalhoyuk-south"
  label: "Çatalhöyük South Area"
  place_name: ["Çatalhöyük", "Çatal Höyük"]

edge:
  s: event_001
  p: sampling_site
  o: [site_001]
```

#### SQL Query Pattern

**Find all samples from a specific site:**
```sql
SELECT
    sample.pid,
    sample.label,
    site.label AS site_name
FROM pqg AS sample
JOIN pqg AS edge1 ON edge1.s = sample.row_id AND edge1.p = 'produced_by'
JOIN pqg AS event ON event.row_id = ANY(edge1.o)
JOIN pqg AS edge2 ON edge2.s = event.row_id AND edge2.p = 'sampling_site'
JOIN pqg AS site ON site.row_id = ANY(edge2.o)
WHERE site.label ILIKE '%çatalhöyük%';
```

#### OpenContext Data Stats
- **Frequency:** 1,096,352 relationships
- **Unique subjects:** 1,096,352 events
- **Unique objects:** 18,213 sites

---

### sample_location

**Type:** SamplingEvent → GeospatialCoordLocation
**Cardinality:** One (optional)
**Required:** ⚪ No

#### Purpose
Precise geographic coordinates where sample was collected.

#### Usage Example

**YAML:**
```yaml
event_001:
  otype: SamplingEvent
  pid: "event:2023-catal-001"

coords_001:
  otype: GeospatialCoordLocation
  pid: "coords:37.6665-32.8274"
  latitude: 37.6665
  longitude: 32.8274
  elevation: "1015 m above mean sea level"

edge:
  s: event_001
  p: sample_location
  o: [coords_001]
```

#### SQL Query Pattern

**Find all samples with coordinates (most important query!):**
```sql
SELECT
    sample.pid,
    sample.label,
    coords.latitude,
    coords.longitude,
    coords.elevation
FROM pqg AS sample
JOIN pqg AS edge1 ON edge1.s = sample.row_id AND edge1.p = 'produced_by'
JOIN pqg AS event ON event.row_id = ANY(edge1.o)
JOIN pqg AS edge2 ON edge2.s = event.row_id AND edge2.p = 'sample_location'
JOIN pqg AS coords ON coords.row_id = ANY(edge2.o)
WHERE sample.otype = 'MaterialSampleRecord'
  AND coords.latitude IS NOT NULL;
```

**Find samples within bounding box:**
```sql
SELECT
    sample.pid,
    coords.latitude,
    coords.longitude
FROM pqg AS sample
JOIN pqg AS edge1 ON edge1.s = sample.row_id AND edge1.p = 'produced_by'
JOIN pqg AS event ON event.row_id = ANY(edge1.o)
JOIN pqg AS edge2 ON edge2.s = event.row_id AND edge2.p = 'sample_location'
JOIN pqg AS coords ON coords.row_id = ANY(edge2.o)
WHERE coords.latitude BETWEEN 37.0 AND 38.0
  AND coords.longitude BETWEEN 32.0 AND 33.0;
```

#### OpenContext Data Stats
- **Frequency:** 1,096,274 relationships (99.99% of events)
- **Unique subjects:** 1,096,274 events
- **Unique objects:** 190,566 coordinate pairs

---

### responsibility (SamplingEvent)

**Type:** SamplingEvent → Agent
**Cardinality:** Many (optional)
**Required:** ⚪ No

#### Purpose
Identifies person(s) responsible for sample collection at the event.

#### Usage Example

**YAML:**
```yaml
event_001:
  otype: SamplingEvent
  pid: "event:2023-catal-001"

agent_001:
  otype: Agent
  pid: "https://orcid.org/0000-0002-1234-5678"
  name: "Dr. Jane Smith"
  role: "Principal Investigator"

agent_002:
  otype: Agent
  pid: "https://orcid.org/0000-0002-5678-1234"
  name: "John Doe"
  role: "Field Technician"

edge_001:
  s: event_001
  p: responsibility
  o: [agent_001]

edge_002:
  s: event_001
  p: responsibility
  o: [agent_002]
```

#### SQL Query Pattern

**Find all samples collected by specific person:**
```sql
SELECT
    sample.pid,
    sample.label,
    agent.name AS collector
FROM pqg AS sample
JOIN pqg AS edge1 ON edge1.s = sample.row_id AND edge1.p = 'produced_by'
JOIN pqg AS event ON event.row_id = ANY(edge1.o)
JOIN pqg AS edge2 ON edge2.s = event.row_id AND edge2.p = 'responsibility'
JOIN pqg AS agent ON agent.row_id = ANY(edge2.o)
WHERE agent.name ILIKE '%smith%';
```

#### OpenContext Data Stats
- **Frequency:** 1,095,272 relationships
- **Unique subjects:** 1,095,272 events
- **Unique objects:** 197 agents

---

### has_context_category (SamplingEvent)

**Type:** SamplingEvent → IdentifiedConcept
**Cardinality:** Many (optional)
**Required:** ⚪ No

#### Purpose
Context classification at the event level (separate from sample-level context).

#### Usage Example

**YAML:**
```yaml
event_001:
  otype: SamplingEvent
  pid: "event:marine-expedition-001"

concept_marine:
  otype: IdentifiedConcept
  pid: "https://w3id.org/isample/vocabulary/sampledfeature/0.9/marinebiome"
  label: "Marine biome"

edge:
  s: event_001
  p: has_context_category
  o: [concept_marine]
```

#### OpenContext Data Stats
- **Frequency:** 0 (OpenContext does not use event-level context)

---

## SamplingSite Predicates

### site_location

**Type:** SamplingSite → GeospatialCoordLocation
**Cardinality:** One (optional)
**Required:** ⚪ No

#### Purpose
Geographic coordinates for the sampling site (typically less precise than sample_location).

#### Usage Example

**YAML:**
```yaml
site_001:
  otype: SamplingSite
  pid: "site:catalhoyuk"
  label: "Çatalhöyük"

coords_site:
  otype: GeospatialCoordLocation
  pid: "coords:site-catalhoyuk"
  latitude: 37.666
  longitude: 32.827
  elevation: "1000 m above mean sea level"

edge:
  s: site_001
  p: site_location
  o: [coords_site]
```

#### SQL Query Pattern

**Find all sites with coordinates:**
```sql
SELECT
    site.pid,
    site.label AS site_name,
    coords.latitude,
    coords.longitude
FROM pqg AS site
JOIN pqg AS edge ON edge.s = site.row_id AND edge.p = 'site_location'
JOIN pqg AS coords ON coords.row_id = ANY(edge.o)
WHERE site.otype = 'SamplingSite';
```

#### OpenContext Data Stats
- **Frequency:** 18,213 relationships
- **Unique subjects:** 18,213 sites
- **Unique objects:** 18,213 coordinate pairs (1:1)

---

## MaterialSampleCuration Predicates

### responsibility (MaterialSampleCuration)

**Type:** MaterialSampleCuration → Agent
**Cardinality:** Many (optional)
**Required:** ⚪ No

#### Purpose
Identifies person(s) responsible for sample curation.

#### Usage Example

**YAML:**
```yaml
curation_001:
  otype: MaterialSampleCuration
  pid: "curation:smithsonian-001"

agent_curator:
  otype: Agent
  pid: "curator:jsmith"
  name: "Jane Smith"
  role: "Collection Manager"

edge:
  s: curation_001
  p: responsibility
  o: [agent_curator]
```

#### OpenContext Data Stats
- **Frequency:** 0 (OpenContext does not track curation)

---

## Cross-Reference: Predicate Usage by Domain

### OpenContext (Archaeology) - Uses 10 of 14

✅ **Used:**
1. produced_by
2. has_material_category
3. has_context_category
4. has_sample_object_type
5. keywords
6. registrant
7. sampling_site
8. sample_location
9. responsibility (SamplingEvent)
10. site_location

❌ **Not used:**
- curation
- related_resource
- has_context_category (SamplingEvent)
- responsibility (MaterialSampleCuration)

### Expected SESAR (Geology) - Projected 8-10 of 14

✅ **Likely used:**
1. produced_by
2. has_material_category
3. has_context_category
4. has_sample_object_type
5. sample_location
6. curation
7. responsibility (SamplingEvent)
8. responsibility (MaterialSampleCuration)

### Expected GEOME (Biology) - Projected 9-11 of 14

✅ **Likely used:**
1. produced_by
2. has_material_category
3. has_context_category
4. has_sample_object_type
5. keywords
6. related_resource (parent-child samples)
7. sampling_site
8. sample_location
9. responsibility (SamplingEvent)

---

## Summary

**Key Takeaways:**

1. **4 predicates are strongly recommended** - produced_by, has_material_category, has_context_category, has_sample_object_type (essential for interoperability, but not schema-required)
2. **3 predicates involve coordinates** - sample_location, site_location (plus is_part_of for nested sites)
3. **3 predicates involve agents** - registrant, responsibility (SamplingEvent), responsibility (MaterialSampleCuration)
4. **2 predicates share names** - responsibility, has_context_category (different subjects)
5. **Different domains use different subsets** - Same schema, different instantiations

> **Note on `is_part_of`:** The schema also defines `is_part_of` (SamplingSite → SamplingSite) for nested site hierarchies (e.g., "Trench 5" is_part_of "Çatalhöyük"). This is excluded from the "14 predicates" count as it represents site containment rather than sample description, and is not commonly used in PQG data.

**Next steps:**
- [EXAMPLES_BY_DOMAIN.md](./EXAMPLES_BY_DOMAIN.md) - See these predicates in real-world examples
- [QUERYING_THE_GRAPH.md](./QUERYING_THE_GRAPH.md) - More complex query patterns

---

**Document Version:** 1.0
**Last Updated:** 2025-11-14
**Schema Version:** 20250207 (MaterialSampleRecord)
**Author:** Claude Code (Sonnet 4.5)

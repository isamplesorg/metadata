# Understanding the iSamples Property Graph

**Purpose:** This guide helps you understand how iSamples metadata is structured as a property graph, making it easier to query, validate, and work with material sample data.

**Key Insight:** The iSamples property graph has a well-defined **grammar** consisting of 8 entity types and 14 relationship types. Understanding this grammar is essential for working with PQG-formatted data.

---

## Table of Contents

1. [What is a Property Graph?](#what-is-a-property-graph)
2. [The 8 Entity Types (oTypes)](#the-8-entity-types-otypes)
3. [The 14 Relationship Types (Predicates)](#the-14-relationship-types-predicates)
4. [The 14 Sentence Types](#the-14-sentence-types)
5. [Why This Structure?](#why-this-structure)
6. [Graph Traversal Patterns](#graph-traversal-patterns)
7. [Storage Format](#storage-format)

---

## What is a Property Graph?

A **property graph** represents data as:
- **Nodes** (entities with properties)
- **Edges** (relationships between nodes)

**Why use a graph?**
- Captures complex relationships naturally
- Enables flexible multi-hop queries
- Supports domain-agnostic modeling
- Facilitates data integration across sources

**iSamples Graph Example:**
```
MaterialSampleRecord (pottery sherd)
    |
    |-- produced_by --> SamplingEvent (2023 excavation)
    |                       |
    |                       |-- sampling_site --> SamplingSite (Çatalhöyük)
    |                       |                         |
    |                       |                         |-- site_location --> GeospatialCoordLocation
    |                       |
    |                       |-- sample_location --> GeospatialCoordLocation
    |                       |
    |                       |-- responsibility --> Agent (Dr. Smith)
    |
    |-- has_material_category --> IdentifiedConcept (Earthenware)
    |
    |-- keywords --> IdentifiedConcept (Neolithic, Pottery)
```

---

## The 8 Entity Types (oTypes)

These are the **node types** in the iSamples graph. Each node has an `otype` field that identifies its type.

### 1. MaterialSampleRecord

**What it represents:** The physical sample itself - the core entity in iSamples.

**Domain examples:**
- Archaeology: Pottery sherd, bone fragment, textile
- Geology: Rock core, mineral specimen, sediment sample
- Biology: Tissue sample, DNA extract, whole organism

**Key properties:**
- `pid` - Unique identifier (typically IGSN)
- `label` - Human-readable name
- `description` - Detailed description
- `sample_identifier` - Canonical sample ID

**Recommended relationships** (marked `recommended: true` in schema for interoperability):
- Should have `produced_by` → SamplingEvent (provenance)
- Should have `has_material_category` → IdentifiedConcept (what it's made of)
- Should have `has_context_category` → IdentifiedConcept (domain context)
- Should have `has_sample_object_type` → IdentifiedConcept (physical form)

> **Schema Alignment (2026-01-29):** The LinkML schema requires `pid`, `label`, and `last_modified_time` as mandatory fields. The relationships above are marked `recommended: true` in the schema for cross-domain interoperability. Additionally, `pid` has been added to `GeospatialCoordLocation` and `SampleRelation` for consistent entity identification.

**Example:**
```yaml
otype: MaterialSampleRecord
pid: "igsn:SSH000001"
label: "Ceramic bowl fragment from Trench 5"
description: "Red-slipped pottery sherd with geometric decoration"
```

---

### 2. SamplingEvent

**What it represents:** The activity that collected/created the sample.

**Domain examples:**
- Archaeology: Excavation, surface collection, test pit
- Geology: Core drilling, outcrop sampling, dredge
- Biology: Field collection, trap deployment, specimen preparation

**Key properties:**
- `pid` - Event identifier
- `label` - Event name/code
- `description` - Sampling procedure details
- `result_time` - When sample was collected (date/datetime)
- `has_feature_of_interest` - What was sampled
- `project` - Project identifier or name

**Relationships:**
- Links TO: SamplingSite, GeospatialCoordLocation, Agent
- Links FROM: MaterialSampleRecord (via `produced_by`)

**Example:**
```yaml
otype: SamplingEvent
pid: "event:2023-catal-t5-001"
label: "Trench 5, Level 3, 2023-07-15"
result_time: "2023-07-15"
has_feature_of_interest: "Neolithic architectural feature"
```

---

### 3. SamplingSite

**What it represents:** Named location where sampling occurred.

**Domain examples:**
- Archaeology: Site name (Çatalhöyük, Pompeii)
- Geology: Formation/locality name (Yellowstone Core Site YC-01)
- Biology: Research station, reef system, forest plot

**Key properties:**
- `pid` - Site identifier
- `label` - Site name
- `description` - Site description
- `place_name` - One or more names for the site

**Relationships:**
- Links TO: GeospatialCoordLocation (via `site_location`)
- Links TO: SamplingSite (via `is_part_of` for nested sites)
- Links FROM: SamplingEvent (via `sampling_site`)

**Example:**
```yaml
otype: SamplingSite
pid: "site:catalhoyuk-south"
label: "Çatalhöyük South Area"
place_name: ["Çatalhöyük", "Çatal Höyük", "Chatal Huyuk"]
```

---

### 4. GeospatialCoordLocation

**What it represents:** Precise geographic coordinates (WGS84).

**Key properties:**
- `pid` - Coordinate identifier
- `latitude` - Decimal degrees (-90 to 90)
- `longitude` - Decimal degrees (-180 to 180)
- `elevation` - String with value, units, datum (e.g., "401 m above mean sea level")
- `obfuscated` - Boolean flag if coordinates are intentionally imprecise

**Relationships:**
- Links FROM: SamplingEvent (via `sample_location`)
- Links FROM: SamplingSite (via `site_location`)

**Example:**
```yaml
otype: GeospatialCoordLocation
pid: "coord:37.6665-32.8274"
latitude: 37.6665
longitude: 32.8274
elevation: "1015 m above mean sea level"
obfuscated: false
```

---

### 5. IdentifiedConcept

**What it represents:** Controlled vocabulary terms for classification and keywords.

**Used for:**
- Material types (rock, ceramic, DNA, etc.)
- Sampled feature types (terrestrial, marine, archaeological)
- Sample object types (core, hand specimen, thin section)
- Free-text keywords for discovery

**Key properties:**
- `pid` - Concept URI (from controlled vocabulary)
- `label` - Human-readable term
- `scheme_name` - Vocabulary name
- `scheme_uri` - Vocabulary identifier

**Vocabularies:**
- [Material Type Vocabulary](https://w3id.org/isample/vocabulary/material/)
- [Sampled Feature Vocabulary](https://w3id.org/isample/vocabulary/sampledfeature/)
- [Material Sample Object Type Vocabulary](https://w3id.org/isample/vocabulary/materialsampleobjecttype/)

**Example:**
```yaml
otype: IdentifiedConcept
pid: "https://w3id.org/isample/vocabulary/material/0.9/earthenware"
label: "Earthenware"
scheme_name: "iSamples Material Type Vocabulary"
scheme_uri: "https://w3id.org/isample/vocabulary/material/"
```

---

### 6. Agent

**What it represents:** Person or organization with a role in sample lifecycle.

**Roles:**
- Collector (sampling event)
- Registrant (sample registration)
- Curator (sample storage)

**Key properties:**
- `pid` - Agent identifier (ORCID preferred)
- `name` - Person/organization name
- `affiliation` - Institutional affiliation
- `contact_information` - Email, phone, address
- `role` - Role relative to sample

**Example:**
```yaml
otype: Agent
pid: "https://orcid.org/0000-0002-1234-5678"
name: "Dr. Jane Smith"
affiliation: "University of Example"
contact_information: "jsmith@example.edu"
role: "Principal Investigator"
```

---

### 7. MaterialSampleCuration

**What it represents:** Information about sample storage, access, and curation history.

**Key properties:**
- `pid` - Curation record identifier
- `label` - Collection/storage name
- `description` - Curation procedures
- `curation_location` - Where sample is stored
- `access_constraints` - Access restrictions

**Relationships:**
- Links TO: Agent (via `responsibility`)
- Links FROM: MaterialSampleRecord (via `curation`)

**Example:**
```yaml
otype: MaterialSampleCuration
pid: "curation:smithsonian-nmnh-123"
label: "Smithsonian NMNH Anthropology Collection"
curation_location: "National Museum of Natural History, Washington DC"
access_constraints: "Appointment required, no destructive sampling"
```

---

### 8. SampleRelation

**What it represents:** Relationship between samples (parent-child, sibling, etc.).

**Use cases:**
- Parent sample → subsample
- Whole organism → tissue → DNA extract
- Core sample → thin section → analysis aliquot

**Key properties:**
- `pid` - Relation identifier
- `label` - Relation description
- `description` - Details of relationship
- `relationship` - Relation type (e.g., "derivedFrom")
- `target` - PID of related sample

**Example:**
```yaml
otype: SampleRelation
pid: "relation:subsample-001"
label: "Subsample for radiocarbon dating"
relationship: "derivedFrom"
target: "igsn:SSH000001"
```

---

## The 14 Relationship Types (Predicates)

These are the **edge types** (predicates) that connect nodes in the iSamples graph. Each edge has:
- `s` (subject) - Source node row_id
- `p` (predicate) - Relationship type
- `o` (object) - Target node row_id(s)

### From MaterialSampleRecord (8 predicates)

| Predicate | Target Type | Cardinality | Description |
|-----------|-------------|-------------|-------------|
| `produced_by` | SamplingEvent | One | Links sample to collection event |
| `has_material_category` | IdentifiedConcept | Many | What is it made of? |
| `has_context_category` | IdentifiedConcept | Many | What domain/environment? |
| `has_sample_object_type` | IdentifiedConcept | Many | What form does it take? |
| `keywords` | IdentifiedConcept | Many | Discovery keywords |
| `registrant` | Agent | One | Who registered this sample? |
| `curation` | MaterialSampleCuration | One | Where is it stored? |
| `related_resource` | SampleRelation | Many | Links to related samples |

### From SamplingEvent (4 predicates)

| Predicate | Target Type | Cardinality | Description |
|-----------|-------------|-------------|-------------|
| `sampling_site` | SamplingSite | One | Where was it collected? |
| `sample_location` | GeospatialCoordLocation | One | Precise coordinates |
| `responsibility` | Agent | Many | Who collected it? |
| `has_context_category` | IdentifiedConcept | Many | Sampling context |

### From SamplingSite (1 predicate)

| Predicate | Target Type | Cardinality | Description |
|-----------|-------------|-------------|-------------|
| `site_location` | GeospatialCoordLocation | One | Site coordinates |

### From MaterialSampleCuration (1 predicate)

| Predicate | Target Type | Cardinality | Description |
|-----------|-------------|-------------|-------------|
| `responsibility` | Agent | Many | Who curates it? |

---

## The 14 Sentence Types

Think of these as the **grammar** of iSamples metadata. Each represents a valid statement you can make about samples:

### Core Sample Provenance (3 sentence types)

1. **"This sample was produced by this sampling event"**
   - `MaterialSampleRecord --produced_by--> SamplingEvent`
   - Every sample MUST have this relationship
   - Links sample to its collection context

2. **"This sample is made of this material type"**
   - `MaterialSampleRecord --has_material_category--> IdentifiedConcept`
   - Required: At least one material classification
   - Example: Earthenware, Basalt, DNA

3. **"This sample represents this context"**
   - `MaterialSampleRecord --has_context_category--> IdentifiedConcept`
   - Required: Domain classification
   - Example: Terrestrial/Archaeological, Marine Biome

### Sample Classification (2 sentence types)

4. **"This sample takes this physical form"**
   - `MaterialSampleRecord --has_sample_object_type--> IdentifiedConcept`
   - Required: Object type
   - Example: Sherd, Core, Specimen

5. **"This sample is described by these keywords"**
   - `MaterialSampleRecord --keywords--> IdentifiedConcept`
   - Optional: Discovery keywords
   - Example: Neolithic, Pottery, Red-slipped

### Sample Stewardship (2 sentence types)

6. **"This sample was registered by this person"**
   - `MaterialSampleRecord --registrant--> Agent`
   - Optional: Who created the metadata record
   - Example: Data curator, Collection manager

7. **"This sample is stored here"**
   - `MaterialSampleRecord --curation--> MaterialSampleCuration`
   - Optional: Storage and access information

### Sample Relationships (1 sentence type)

8. **"This sample relates to that sample"**
   - `MaterialSampleRecord --related_resource--> SampleRelation`
   - Optional: Parent-child, sibling relationships
   - Example: Subsample, Derived from

### Event Location (2 sentence types)

9. **"This event occurred at this site"**
   - `SamplingEvent --sampling_site--> SamplingSite`
   - Optional: Named sampling location
   - Example: Çatalhöyük, Yellowstone Core Site

10. **"This event occurred at these coordinates"**
    - `SamplingEvent --sample_location--> GeospatialCoordLocation`
    - Optional but common: Precise sample coordinates
    - Example: 37.6665°N, 32.8274°E

### Event Responsibility (2 sentence types)

11. **"This person collected at this event"**
    - `SamplingEvent --responsibility--> Agent`
    - Optional: Field collectors, project team

12. **"This event belongs to this context"**
    - `SamplingEvent --has_context_category--> IdentifiedConcept`
    - Optional: Event-level context classification

### Site Location (1 sentence type)

13. **"This site is located at these coordinates"**
    - `SamplingSite --site_location--> GeospatialCoordLocation`
    - Optional: Site-level coordinates (less precise than sample)

### Curation Responsibility (1 sentence type)

14. **"This person curates this collection"**
    - `MaterialSampleCuration --responsibility--> Agent`
    - Optional: Curators, collection managers

---

## Why This Structure?

### Multi-Hop Traversal by Design

**Finding a sample's coordinates requires multiple hops:**

```
MaterialSampleRecord
    → produced_by → SamplingEvent
        → sample_location → GeospatialCoordLocation
```

**Why not store coordinates directly on the sample?**

✅ **Benefits of separation:**
1. **Shared locations** - Multiple samples from same event share one coordinate
2. **Different precision** - Site coordinates vs exact sample coordinates
3. **Reusable events** - One event can produce many samples
4. **Flexible modeling** - Some samples have site but not precise coords

❌ **Drawbacks of flat structure:**
- Duplicate coordinates across samples
- Can't distinguish site-level vs sample-level precision
- Harder to maintain data consistency

### Domain-Agnostic Design

The 8 entity types work across **all scientific domains**:

- **Archaeology:** Pottery, bones, charcoal → Terrestrial/Archaeological context
- **Geology:** Cores, outcrops, minerals → Terrestrial/Subsurface context
- **Biology:** Tissue, DNA, specimens → Marine Biome or Terrestrial context

**Same schema, different values** - This is true domain-agnostic modeling.

### Graph Query Flexibility

**Example queries enabled by graph structure:**

1. "Find all samples collected by Agent X"
   - `MaterialSampleRecord → produced_by → SamplingEvent → responsibility → Agent`

2. "Find all samples within 10km of a location"
   - `MaterialSampleRecord → produced_by → SamplingEvent → sample_location → GeospatialCoordLocation`

3. "Find all earthenware samples with keywords 'Neolithic' AND 'pottery'"
   - `MaterialSampleRecord → has_material_category → IdentifiedConcept` (Earthenware)
   - `MaterialSampleRecord → keywords → IdentifiedConcept` (Neolithic, Pottery)

4. "Find parent sample for a given subsample"
   - `MaterialSampleRecord → related_resource → SampleRelation` (where relationship="derivedFrom")

---

## Graph Traversal Patterns

### Pattern 1: Sample → Coordinates (2-3 hops)

**Path:**
```
Sample → produced_by → Event → sample_location → Coords
```

**SQL example:**
```sql
SELECT
    sample.pid AS sample_id,
    coords.latitude,
    coords.longitude
FROM pqg AS sample
JOIN pqg AS edge1 ON edge1.s = sample.row_id AND edge1.p = 'produced_by'
JOIN pqg AS event ON event.row_id = ANY(edge1.o)
JOIN pqg AS edge2 ON edge2.s = event.row_id AND edge2.p = 'sample_location'
JOIN pqg AS coords ON coords.row_id = ANY(edge2.o)
WHERE sample.otype = 'MaterialSampleRecord'
```

### Pattern 2: Sample → Site Name (3 hops)

**Path:**
```
Sample → produced_by → Event → sampling_site → Site
```

**SQL example:**
```sql
SELECT
    sample.label AS sample_label,
    site.label AS site_name,
    site.place_name
FROM pqg AS sample
JOIN pqg AS edge1 ON edge1.s = sample.row_id AND edge1.p = 'produced_by'
JOIN pqg AS event ON event.row_id = ANY(edge1.o)
JOIN pqg AS edge2 ON edge2.s = event.row_id AND edge2.p = 'sampling_site'
JOIN pqg AS site ON site.row_id = ANY(edge2.o)
WHERE sample.otype = 'MaterialSampleRecord'
```

### Pattern 3: Sample → Collector (2-3 hops)

**Path:**
```
Sample → produced_by → Event → responsibility → Agent
```

**SQL example:**
```sql
SELECT
    sample.label AS sample_label,
    agent.name AS collector_name,
    event.result_time
FROM pqg AS sample
JOIN pqg AS edge1 ON edge1.s = sample.row_id AND edge1.p = 'produced_by'
JOIN pqg AS event ON event.row_id = ANY(edge1.o)
JOIN pqg AS edge2 ON edge2.s = event.row_id AND edge2.p = 'responsibility'
JOIN pqg AS agent ON agent.row_id = ANY(edge2.o)
WHERE sample.otype = 'MaterialSampleRecord'
```

### Pattern 4: Material Type Filter (1 hop)

**Path:**
```
Sample → has_material_category → Concept
```

**SQL example:**
```sql
SELECT
    sample.pid,
    sample.label,
    concept.label AS material_type
FROM pqg AS sample
JOIN pqg AS edge ON edge.s = sample.row_id AND edge.p = 'has_material_category'
JOIN pqg AS concept ON concept.row_id = ANY(edge.o)
WHERE concept.label = 'Earthenware'
```

---

## Storage Format

### Unified Table Structure

PQG stores **both nodes and edges in a single table**:

```sql
CREATE TABLE pqg (
    row_id INTEGER PRIMARY KEY,
    pid VARCHAR UNIQUE NOT NULL,
    otype VARCHAR,  -- Node type or '_edge_'

    -- Edge fields (NULL for non-edge nodes)
    s INTEGER,      -- Subject row_id
    p VARCHAR,      -- Predicate
    o INTEGER[],    -- Object row_id(s)
    n VARCHAR,      -- Named graph

    -- Entity properties (NULL for edges)
    label VARCHAR,
    description TEXT,
    latitude DECIMAL,
    longitude DECIMAL,
    elevation VARCHAR,
    ...
);
```

### Node Rows

**Example: MaterialSampleRecord node**
```
row_id: 1
pid: "igsn:SSH000001"
otype: "MaterialSampleRecord"
s: NULL
p: NULL
o: NULL
n: NULL
label: "Ceramic bowl fragment"
description: "Red-slipped pottery..."
```

### Edge Rows

**Example: produced_by edge**
```
row_id: 1001
pid: "edge_12345"
otype: "_edge_"
s: 1        (sample row_id)
p: "produced_by"
o: [2]      (event row_id)
n: NULL
label: NULL
description: NULL
```

### Query Pattern

**Find all edges of a specific type:**
```sql
SELECT
    subject.pid AS subject_pid,
    edge.p AS predicate,
    object.pid AS object_pid
FROM pqg AS edge
JOIN pqg AS subject ON edge.s = subject.row_id
JOIN pqg AS object ON object.row_id = ANY(edge.o)
WHERE edge.otype = '_edge_'
  AND subject.otype = 'MaterialSampleRecord'
  AND edge.p = 'produced_by'
  AND object.otype = 'SamplingEvent'
```

---

## Summary

**The iSamples property graph is defined by:**

✅ **8 entity types (nodes)** - MaterialSampleRecord, SamplingEvent, SamplingSite, GeospatialCoordLocation, IdentifiedConcept, Agent, MaterialSampleCuration, SampleRelation

✅ **14 relationship types (edges)** - The complete grammar of valid connections

✅ **14 sentence types** - All possible statements you can make about samples

**Key takeaway:** Understanding these building blocks enables you to:
- Query iSamples data effectively
- Validate metadata completeness
- Integrate new data sources
- Build tools that work across domains

**Next steps:**
- [PREDICATES_REFERENCE.md](./PREDICATES_REFERENCE.md) - Detailed reference for each predicate
- [EXAMPLES_BY_DOMAIN.md](./EXAMPLES_BY_DOMAIN.md) - Real-world examples
- [QUERYING_THE_GRAPH.md](./QUERYING_THE_GRAPH.md) - Query patterns and SQL

---

**Document Version:** 1.0
**Last Updated:** 2025-11-14
**Schema Version:** 20250207 (MaterialSampleRecord)
**Author:** Claude Code (Sonnet 4.5) based on iSamples LinkML schema analysis

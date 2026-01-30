# Visual Guide to iSamples Edge Types

This document provides visual representations of the iSamples property graph structure using diagrams and charts.

## Table of Contents

1. [Complete Entity Relationship Diagram](#complete-entity-relationship-diagram)
2. [Edge Type Matrix](#edge-type-matrix)
3. [Sample-Centric View](#sample-centric-view)
4. [Event-Centric View](#event-centric-view)
5. [Graph Traversal Examples](#graph-traversal-examples)
6. [Edge Type Heatmap](#edge-type-heatmap)
7. [Storage Structure Diagram](#storage-structure-diagram)

---

## Complete Entity Relationship Diagram

This diagram shows all 8 entity types and the 14 relationship types (predicates) connecting them.

```mermaid
graph TB
    MSR[MaterialSampleRecord<br/>📋 Sample]
    Event[SamplingEvent<br/>🎯 Collection Event]
    Site[SamplingSite<br/>📍 Named Location]
    Coords[GeospatialCoordLocation<br/>🌍 Coordinates]
    Concept[IdentifiedConcept<br/>🏷️ Vocabulary Term]
    Agent[Agent<br/>👤 Person/Organization]
    Curation[MaterialSampleCuration<br/>📦 Repository Info]
    Relation[SampleRelation<br/>🔗 Sample Links]

    MSR -->|produced_by| Event
    MSR -->|has_material_category| Concept
    MSR -->|has_context_category| Concept
    MSR -->|has_sample_object_type| Concept
    MSR -->|keywords| Concept
    MSR -->|registrant| Agent
    MSR -->|curation| Curation
    MSR -->|related_resource| Relation

    Event -->|sampling_site| Site
    Event -->|sample_location| Coords
    Event -->|has_context_category| Concept
    Event -->|responsibility| Agent

    Site -->|site_location| Coords

    Curation -->|responsibility| Agent

    classDef core fill:#e1f5ff,stroke:#0077be,stroke-width:3px
    classDef event fill:#fff4e1,stroke:#ff8c00,stroke-width:2px
    classDef location fill:#e8f5e9,stroke:#4caf50,stroke-width:2px
    classDef vocab fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px
    classDef supporting fill:#fce4ec,stroke:#e91e63,stroke-width:2px

    class MSR core
    class Event event
    class Site,Coords location
    class Concept vocab
    class Agent,Curation,Relation supporting
```

**Legend:**
- **📋 MaterialSampleRecord (blue):** The physical sample - central entity
- **🎯 SamplingEvent (orange):** When/how the sample was collected
- **📍 SamplingSite (green):** Named locations (e.g., "Çatalhöyük")
- **🌍 GeospatialCoordLocation (green):** Latitude/longitude coordinates
- **🏷️ IdentifiedConcept (purple):** Controlled vocabulary terms
- **👤 Agent (pink):** People and organizations
- **📦 MaterialSampleCuration (pink):** Repository/archive information
- **🔗 SampleRelation (pink):** Links between related samples

---

## Edge Type Matrix

This table shows which entity types (subjects) connect to which entity types (objects) via which predicates.

| **Subject Type** | **Predicate** | **Object Type** | **Multivalued** | **Required** |
|------------------|---------------|-----------------|-----------------|--------------|
| MaterialSampleRecord | `produced_by` | SamplingEvent | No | Yes |
| MaterialSampleRecord | `has_material_category` | IdentifiedConcept | Yes | No |
| MaterialSampleRecord | `has_context_category` | IdentifiedConcept | Yes | No |
| MaterialSampleRecord | `has_sample_object_type` | IdentifiedConcept | Yes | No |
| MaterialSampleRecord | `keywords` | IdentifiedConcept | Yes | No |
| MaterialSampleRecord | `registrant` | Agent | No | No |
| MaterialSampleRecord | `curation` | MaterialSampleCuration | No | No |
| MaterialSampleRecord | `related_resource` | SampleRelation | Yes | No |
| SamplingEvent | `sampling_site` | SamplingSite | No | No |
| SamplingEvent | `sample_location` | GeospatialCoordLocation | No | No |
| SamplingEvent | `has_context_category` | IdentifiedConcept | Yes | No |
| SamplingEvent | `responsibility` | Agent | Yes | No |
| SamplingSite | `site_location` | GeospatialCoordLocation | No | No |
| MaterialSampleCuration | `responsibility` | Agent | Yes | No |

**Total:** 14 edge types forming the complete iSamples grammar

---

## Sample-Centric View

This diagram focuses on relationships emanating from a MaterialSampleRecord (the core entity).

```mermaid
graph LR
    Sample[MaterialSampleRecord<br/>'Pottery Sherd 42']

    Sample -->|produced_by<br/>REQUIRED| Event[SamplingEvent<br/>'Excavation Layer 3']
    Sample -->|has_material_category| Mat[IdentifiedConcept<br/>'Ceramic']
    Sample -->|has_context_category| Ctx[IdentifiedConcept<br/>'Archaeological']
    Sample -->|has_sample_object_type| Type[IdentifiedConcept<br/>'Pottery']
    Sample -->|keywords| KW1[IdentifiedConcept<br/>'Neolithic']
    Sample -->|keywords| KW2[IdentifiedConcept<br/>'Painted']
    Sample -->|registrant| Reg[Agent<br/>'J. Smith']
    Sample -->|curation| Cur[MaterialSampleCuration<br/>'Museum Archive']
    Sample -->|related_resource| Rel[SampleRelation<br/>'Parent Sample Link']

    classDef sample fill:#e1f5ff,stroke:#0077be,stroke-width:4px
    classDef required fill:#ffebee,stroke:#c62828,stroke-width:3px
    classDef optional fill:#f5f5f5,stroke:#757575,stroke-width:1px

    class Sample sample
    class Event required
    class Mat,Ctx,Type,KW1,KW2,Reg,Cur,Rel optional
```

**Key observations:**
- **`produced_by` is recommended in schema** - every sample should link to a SamplingEvent for provenance
- **Multiple keywords** can be assigned (multivalued)
- **IdentifiedConcept used 4 different ways** - material, context, object type, keywords
- **4 relationship types to IdentifiedConcept** enable rich categorization

---

## Event-Centric View

This diagram shows how SamplingEvent acts as a bridge between samples and location/collector information.

```mermaid
graph TB
    subgraph Samples
        S1[Sample 1]
        S2[Sample 2]
        S3[Sample 3]
    end

    subgraph Event Context
        Event[SamplingEvent<br/>'2023-06-15 Excavation']
    end

    subgraph Location
        Site[SamplingSite<br/>'Çatalhöyük']
        Coords1[GeospatialCoordLocation<br/>'Event Location']
        Coords2[GeospatialCoordLocation<br/>'Site Centroid']
    end

    subgraph People
        Agent1[Agent<br/>'Dr. Smith']
        Agent2[Agent<br/>'Lab Tech']
    end

    subgraph Classification
        Context[IdentifiedConcept<br/>'Archaeological']
    end

    S1 -->|produced_by| Event
    S2 -->|produced_by| Event
    S3 -->|produced_by| Event

    Event -->|sampling_site| Site
    Event -->|sample_location| Coords1
    Event -->|responsibility| Agent1
    Event -->|responsibility| Agent2
    Event -->|has_context_category| Context

    Site -->|site_location| Coords2

    classDef event fill:#fff4e1,stroke:#ff8c00,stroke-width:3px
    classDef samples fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef location fill:#e8f5e9,stroke:#4caf50,stroke-width:2px
    classDef people fill:#fce4ec,stroke:#e91e63,stroke-width:2px
    classDef vocab fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px

    class Event event
    class S1,S2,S3 samples
    class Site,Coords1,Coords2 location
    class Agent1,Agent2 people
    class Context vocab
```

**Key observations:**
- **Multiple samples** can share the same SamplingEvent (batch collection)
- **Two paths to coordinates:** Event location (specific) vs Site location (general)
- **Multiple agents** can be responsible for an event (multivalued)
- **Event bridges samples to context** - who, when, where

---

## Graph Traversal Examples

### Example 1: Find Sample Coordinates (2-hop traversal)

```mermaid
graph LR
    A[MaterialSampleRecord] -->|1. produced_by| B[SamplingEvent]
    B -->|2. sample_location| C[GeospatialCoordLocation]

    style A fill:#e1f5ff,stroke:#0077be,stroke-width:3px
    style B fill:#fff4e1,stroke:#ff8c00,stroke-width:2px
    style C fill:#e8f5e9,stroke:#4caf50,stroke-width:2px
```

**SQL Pattern:**
```sql
SELECT sample.*, coords.*
FROM pqg AS sample
JOIN pqg AS edge1 ON edge1.s = sample.row_id AND edge1.p = 'produced_by'
JOIN pqg AS event ON event.row_id = ANY(edge1.o)
JOIN pqg AS edge2 ON edge2.s = event.row_id AND edge2.p = 'sample_location'
JOIN pqg AS coords ON coords.row_id = ANY(edge2.o)
```

### Example 2: Find Sample Site Name (3-hop traversal)

```mermaid
graph LR
    A[MaterialSampleRecord] -->|1. produced_by| B[SamplingEvent]
    B -->|2. sampling_site| C[SamplingSite]
    C -->|3. site_location| D[GeospatialCoordLocation]

    style A fill:#e1f5ff,stroke:#0077be,stroke-width:3px
    style B fill:#fff4e1,stroke:#ff8c00,stroke-width:2px
    style C fill:#e8f5e9,stroke:#4caf50,stroke-width:2px
    style D fill:#e8f5e9,stroke:#4caf50,stroke-width:2px
```

**SQL Pattern:**
```sql
SELECT sample.*, site.label AS site_name, coords.*
FROM pqg AS sample
JOIN pqg AS edge1 ON edge1.s = sample.row_id AND edge1.p = 'produced_by'
JOIN pqg AS event ON event.row_id = ANY(edge1.o)
JOIN pqg AS edge2 ON edge2.s = event.row_id AND edge2.p = 'sampling_site'
JOIN pqg AS site ON site.row_id = ANY(edge2.o)
JOIN pqg AS edge3 ON edge3.s = site.row_id AND edge3.p = 'site_location'
JOIN pqg AS coords ON coords.row_id = ANY(edge3.o)
```

### Example 3: Find Sample Collector (2-hop traversal)

```mermaid
graph LR
    A[MaterialSampleRecord] -->|1. produced_by| B[SamplingEvent]
    B -->|2. responsibility| C[Agent]

    style A fill:#e1f5ff,stroke:#0077be,stroke-width:3px
    style B fill:#fff4e1,stroke:#ff8c00,stroke-width:2px
    style C fill:#fce4ec,stroke:#e91e63,stroke-width:2px
```

**SQL Pattern:**
```sql
SELECT sample.*, agent.*
FROM pqg AS sample
JOIN pqg AS edge1 ON edge1.s = sample.row_id AND edge1.p = 'produced_by'
JOIN pqg AS event ON event.row_id = ANY(edge1.o)
JOIN pqg AS edge2 ON edge2.s = event.row_id AND edge2.p = 'responsibility'
JOIN pqg AS agent ON agent.row_id = ANY(edge2.o)
```

### Example 4: Find Repository Curator (2-hop traversal)

```mermaid
graph LR
    A[MaterialSampleRecord] -->|1. curation| B[MaterialSampleCuration]
    B -->|2. responsibility| C[Agent]

    style A fill:#e1f5ff,stroke:#0077be,stroke-width:3px
    style B fill:#fce4ec,stroke:#e91e63,stroke-width:2px
    style C fill:#fce4ec,stroke:#e91e63,stroke-width:2px
```

**SQL Pattern:**
```sql
SELECT sample.*, curation.*, curator.*
FROM pqg AS sample
JOIN pqg AS edge1 ON edge1.s = sample.row_id AND edge1.p = 'curation'
JOIN pqg AS curation ON curation.row_id = ANY(edge1.o)
JOIN pqg AS edge2 ON edge2.s = curation.row_id AND edge2.p = 'responsibility'
JOIN pqg AS curator ON curator.row_id = ANY(edge2.o)
```

---

## Edge Type Heatmap

This matrix shows the "connectivity density" between entity types in the OpenContext dataset.

### Actual Edge Counts (OpenContext Dataset - 11.6M total records)

| **From/To** | **Material<br/>Sample<br/>Record** | **Sampling<br/>Event** | **Sampling<br/>Site** | **Geospatial<br/>Coord<br/>Location** | **Identified<br/>Concept** | **Agent** | **Material<br/>Sample<br/>Curation** | **Sample<br/>Relation** |
|-------------|:----------------------------------:|:----------------------:|:---------------------:|:--------------------------------------:|:--------------------------:|:---------:|:------------------------------------:|:-----------------------:|
| **MaterialSampleRecord** | - | 🔥🔥🔥<br/>1.1M | - | - | 🔥🔥🔥🔥🔥<br/>9.4M | ❄️<br/>~1K | ❄️<br/>~1K | ❄️<br/>~1K |
| **SamplingEvent** | - | - | 🔥🔥<br/>384K | 🔥🔥🔥<br/>1.1M | 🔥🔥🔥<br/>1.1M | 🔥<br/>73K | - | - |
| **SamplingSite** | - | - | - | 🔥🔥<br/>384K | - | - | - | - |
| **MaterialSampleCuration** | - | - | - | - | - | ❄️<br/>~1K | - | - |

**Legend:**
- 🔥🔥🔥🔥🔥 = >5M edges (ultra-dense)
- 🔥🔥🔥 = 1M-5M edges (very dense)
- 🔥🔥 = 100K-1M edges (dense)
- 🔥 = 10K-100K edges (moderate)
- ❄️ = <10K edges (sparse)
- `-` = 0 edges (no relationship)

**Key insights:**
1. **MaterialSampleRecord → IdentifiedConcept** is the densest relationship (9.4M edges)
   - Includes: material categories, context categories, object types, keywords
2. **MaterialSampleRecord → SamplingEvent** is critical infrastructure (1.1M edges)
   - Required relationship - every sample has exactly one event
3. **Event → Coordinates** enables geospatial queries (1.1M edges)
4. **Curation and Relation** are rarely used in OpenContext data
   - More common in geology (SESAR) and biology (GEOME) domains

---

## Storage Structure Diagram

This diagram shows how entities and edges are stored in the unified PQG table.

```mermaid
graph TB
    subgraph "PQG Table (Unified Storage)"
        subgraph "Entity Rows (otype != '_edge_')"
            E1["row_id: 1<br/>pid: 'iSamples:...'<br/>otype: 'MaterialSampleRecord'<br/>label: 'Sample 42'<br/>description: '...'"]
            E2["row_id: 2<br/>pid: 'iSamples:...'<br/>otype: 'SamplingEvent'<br/>label: 'Excavation 2023'<br/>event_date: '2023-06-15'"]
            E3["row_id: 3<br/>pid: 'iSamples:...'<br/>otype: 'GeospatialCoordLocation'<br/>latitude: 37.5<br/>longitude: 32.8"]
        end

        subgraph "Edge Rows (otype = '_edge_')"
            Edge1["row_id: 100<br/>otype: '_edge_'<br/>s: 1<br/>p: 'produced_by'<br/>o: [2]"]
            Edge2["row_id: 101<br/>otype: '_edge_'<br/>s: 2<br/>p: 'sample_location'<br/>o: [3]"]
        end
    end

    E1 -.->|"s=1"| Edge1
    Edge1 -.->|"o=[2]"| E2
    E2 -.->|"s=2"| Edge2
    Edge2 -.->|"o=[3]"| E3

    style E1 fill:#e1f5ff,stroke:#0077be,stroke-width:2px
    style E2 fill:#fff4e1,stroke:#ff8c00,stroke-width:2px
    style E3 fill:#e8f5e9,stroke:#4caf50,stroke-width:2px
    style Edge1 fill:#ffebee,stroke:#c62828,stroke-width:2px
    style Edge2 fill:#ffebee,stroke:#c62828,stroke-width:2px
```

**How it works:**
1. **Entity rows** have `otype` set to their entity type (e.g., `MaterialSampleRecord`)
2. **Edge rows** have `otype = '_edge_'`
3. **Edge `s` field** points to subject entity's `row_id`
4. **Edge `p` field** contains the predicate name (e.g., `produced_by`)
5. **Edge `o` field** is an **array** of object entity `row_id`s (supports multivalued)
6. **Joining** requires matching `edge.s = subject.row_id` and `object.row_id = ANY(edge.o)`

---

## Predicate Usage Patterns

This chart shows how often each predicate appears in the OpenContext dataset.

```mermaid
%%{init: {'theme':'base'}}%%
graph LR
    subgraph "Most Common (>1M edges each)"
        P1["has_sample_object_type<br/>1,124,480 edges"]
        P2["produced_by<br/>1,096,352 edges"]
        P3["has_material_category<br/>1,095,920 edges"]
        P4["has_context_category<br/>1,095,912 edges"]
        P5["keywords<br/>1,070,912 edges"]
    end

    subgraph "Common (100K-1M edges)"
        P6["sample_location<br/>1,095,912 edges"]
        P7["sampling_site<br/>383,912 edges"]
        P8["site_location<br/>383,912 edges"]
    end

    subgraph "Moderate (10K-100K edges)"
        P9["responsibility (Event)<br/>72,520 edges"]
    end

    subgraph "Rare (<10K edges)"
        P10["registrant<br/>~1,000 edges"]
        P11["curation<br/>~500 edges"]
        P12["responsibility (Curation)<br/>~500 edges"]
    end

    subgraph "Not Used in OpenContext"
        P13["related_resource<br/>0 edges"]
    end

    style P1 fill:#c62828,color:#fff
    style P2 fill:#c62828,color:#fff
    style P3 fill:#c62828,color:#fff
    style P4 fill:#c62828,color:#fff
    style P5 fill:#c62828,color:#fff
    style P6 fill:#f57c00,color:#fff
    style P7 fill:#f57c00,color:#fff
    style P8 fill:#f57c00,color:#fff
    style P9 fill:#fbc02d
    style P10 fill:#aed581
    style P11 fill:#aed581
    style P12 fill:#aed581
    style P13 fill:#e0e0e0
```

**Domain patterns:**
- **OpenContext (archaeology):** Heavy use of categorization (material, context, object type)
- **SESAR (geology):** More use of `curation` and `registrant` (institutional tracking)
- **GEOME (biology):** Heavy use of `related_resource` (parent-child sample chains)

---

## Multi-Hop Traversal Map

This diagram shows common multi-hop query patterns and their path lengths.

```mermaid
graph TB
    MSR[MaterialSampleRecord<br/>'Start Here']

    MSR -->|1 hop| Event[SamplingEvent]
    MSR -->|1 hop| Material[Material Category]
    MSR -->|1 hop| Context[Context Category]
    MSR -->|1 hop| Registrant[Registrant]

    Event -->|+1 = 2 hops| Coords1[Event Coordinates]
    Event -->|+1 = 2 hops| Site[Sampling Site]
    Event -->|+1 = 2 hops| Collector[Collector]
    Event -->|+1 = 2 hops| EventContext[Event Context]

    Site -->|+1 = 3 hops| Coords2[Site Coordinates]

    MSR -->|1 hop| Curation[Curation Info]
    Curation -->|+1 = 2 hops| Curator[Curator]

    MSR -->|1 hop| Related[Related Samples]

    classDef hop1 fill:#e1f5ff,stroke:#0077be,stroke-width:2px
    classDef hop2 fill:#fff4e1,stroke:#ff8c00,stroke-width:2px
    classDef hop3 fill:#e8f5e9,stroke:#4caf50,stroke-width:2px

    class MSR,Material,Context,Registrant,Event,Curation,Related hop1
    class Coords1,Site,Collector,EventContext,Curator hop2
    class Coords2 hop3
```

**Path complexity:**
- **1-hop queries:** Direct attributes (material, context, keywords, registrant)
- **2-hop queries:** Location, collector, site name (most common complex queries)
- **3-hop queries:** Site coordinates (rare - usually use event coordinates instead)

---

## Entity Type Connectivity

This diagram shows how "connected" each entity type is (number of relationship types it participates in).

```mermaid
graph LR
    subgraph "Highly Connected (Hub Nodes)"
        MSR["MaterialSampleRecord<br/>8 outgoing edge types<br/>📊 Centrality: HIGH"]
        Event["SamplingEvent<br/>4 outgoing edge types<br/>📊 Centrality: HIGH"]
    end

    subgraph "Moderately Connected"
        Site["SamplingSite<br/>1 outgoing edge type<br/>📊 Centrality: MEDIUM"]
        Curation["MaterialSampleCuration<br/>1 outgoing edge type<br/>📊 Centrality: MEDIUM"]
    end

    subgraph "Leaf Nodes (No Outgoing Edges)"
        Concept["IdentifiedConcept<br/>0 outgoing<br/>5 incoming edge types<br/>📊 Centrality: HIGH (target)"]
        Agent["Agent<br/>0 outgoing<br/>3 incoming edge types<br/>📊 Centrality: MEDIUM (target)"]
        Coords["GeospatialCoordLocation<br/>0 outgoing<br/>2 incoming edge types<br/>📊 Centrality: MEDIUM (target)"]
        Relation["SampleRelation<br/>0 outgoing<br/>1 incoming edge type<br/>📊 Centrality: LOW (target)"]
    end

    style MSR fill:#c62828,color:#fff
    style Event fill:#f57c00,color:#fff
    style Site fill:#fbc02d
    style Curation fill:#fbc02d
    style Concept fill:#9c27b0,color:#fff
    style Agent fill:#7b1fa2,color:#fff
    style Coords fill:#7b1fa2,color:#fff
    style Relation fill:#aed581
```

**Key observations:**
1. **MaterialSampleRecord** is the primary hub (8 outgoing relationship types)
2. **SamplingEvent** is secondary hub (4 outgoing relationship types)
3. **IdentifiedConcept** is most popular target (5 different incoming predicates)
4. **Agent, Coords** are intermediate targets (2-3 incoming predicates each)
5. **SampleRelation** is rarely used (1 incoming predicate, sparse in data)

---

## The 14 Sentence Types (Grammar Summary)

Visual summary of the complete iSamples "grammar":

```mermaid
graph TB
    subgraph "1. MaterialSampleRecord Sentences (8 types)"
        S1["Sample --produced_by→ Event<br/>REQUIRED"]
        S2["Sample --has_material_category→ Concept<br/>Material type"]
        S3["Sample --has_context_category→ Concept<br/>Sampled feature"]
        S4["Sample --has_sample_object_type→ Concept<br/>Object classification"]
        S5["Sample --keywords→ Concept<br/>Discovery terms"]
        S6["Sample --registrant→ Agent<br/>Who registered"]
        S7["Sample --curation→ Curation<br/>Archive info"]
        S8["Sample --related_resource→ Relation<br/>Sample links"]
    end

    subgraph "2. SamplingEvent Sentences (4 types)"
        E1["Event --sampling_site→ Site<br/>Named location"]
        E2["Event --sample_location→ Coords<br/>Exact coordinates"]
        E3["Event --has_context_category→ Concept<br/>Event type"]
        E4["Event --responsibility→ Agent<br/>Collector"]
    end

    subgraph "3. SamplingSite Sentences (1 type)"
        T1["Site --site_location→ Coords<br/>Site centroid"]
    end

    subgraph "4. MaterialSampleCuration Sentences (1 type)"
        C1["Curation --responsibility→ Agent<br/>Curator"]
    end

    style S1 fill:#c62828,color:#fff
    style S2 fill:#e57373,color:#fff
    style S3 fill:#e57373,color:#fff
    style S4 fill:#e57373,color:#fff
    style S5 fill:#e57373,color:#fff
    style S6 fill:#e57373,color:#fff
    style S7 fill:#e57373,color:#fff
    style S8 fill:#e57373,color:#fff
    style E1 fill:#f57c00,color:#fff
    style E2 fill:#f57c00,color:#fff
    style E3 fill:#f57c00,color:#fff
    style E4 fill:#f57c00,color:#fff
    style T1 fill:#4caf50,color:#fff
    style C1 fill:#9c27b0,color:#fff
```

**Total:** 14 edge types = Complete grammar of iSamples property graphs

---

## Cross-Domain Comparison

How different scientific domains use the 14 edge types:

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#e1f5ff'}}}%%
graph TB
    subgraph "All Domains Use (Core Infrastructure)"
        Core["produced_by<br/>has_material_category<br/>has_context_category<br/>sample_location"]
    end

    subgraph "Archaeology Heavy Use (OpenContext)"
        Arch["keywords<br/>has_sample_object_type<br/>sampling_site<br/>site_location"]
    end

    subgraph "Geology Heavy Use (SESAR)"
        Geo["registrant<br/>curation<br/>responsibility (Curation)"]
    end

    subgraph "Biology Heavy Use (GEOME)"
        Bio["related_resource<br/>responsibility (Event)"]
    end

    style Core fill:#4caf50,color:#fff
    style Arch fill:#ff8c00,color:#fff
    style Geo fill:#2196f3,color:#fff
    style Bio fill:#9c27b0,color:#fff
```

**Why different patterns?**
- **Archaeology:** Heavy emphasis on discovery/publication (keywords, object types)
- **Geology:** Institutional tracking (registrants, repositories, curators)
- **Biology:** Sample lineage (parent-child relationships via related_resource)
- **All domains:** Need material classification and geographic coordinates

---

## Graph Query Complexity Chart

This chart shows the complexity distribution of common queries:

| **Query Type** | **Hops** | **Joins** | **Complexity** | **Example** |
|----------------|:--------:|:---------:|:--------------:|-------------|
| Get sample label | 0 | 0 | ⭐ | `SELECT label FROM pqg WHERE pid=?` |
| Get material category | 1 | 2 | ⭐⭐ | Sample → Category |
| Get sample coordinates | 2 | 4 | ⭐⭐⭐ | Sample → Event → Coords |
| Get collector name | 2 | 4 | ⭐⭐⭐ | Sample → Event → Agent |
| Get site name | 2 | 4 | ⭐⭐⭐ | Sample → Event → Site |
| Get site coordinates | 3 | 6 | ⭐⭐⭐⭐ | Sample → Event → Site → Coords |
| Get all related samples | 2-4 | 4-8 | ⭐⭐⭐⭐⭐ | Sample → Relation → Samples (recursive) |

**Performance tip:** Cache 2-hop queries (coordinates, collectors) - they're the most common complex pattern.

---

## Next Steps

- **SQL examples**: See [QUERYING_THE_GRAPH.md](QUERYING_THE_GRAPH.md) for detailed SQL patterns
- **Predicate details**: See [PREDICATES_REFERENCE.md](PREDICATES_REFERENCE.md) for each relationship type
- **Conceptual guide**: See [UNDERSTANDING_THE_GRAPH.md](UNDERSTANDING_THE_GRAPH.md) for foundations
- **Real examples**: See [EXAMPLES_BY_DOMAIN.md](EXAMPLES_BY_DOMAIN.md) for complete YAML samples

---

**Last updated:** 2025-11-14
**Part of:** iSamples Property Graph Documentation Suite

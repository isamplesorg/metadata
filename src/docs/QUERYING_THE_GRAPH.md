# Querying the Property Graph: Practical SQL Patterns

This guide provides practical SQL query patterns for working with iSamples property graph data. All queries are designed for DuckDB, but the patterns work with other SQL databases.

## Table of Contents

1. [Understanding the Storage Model](#understanding-the-storage-model)
2. [Basic Entity Queries](#basic-entity-queries)
3. [Single-Hop Traversals](#single-hop-traversals)
4. [Multi-Hop Traversals](#multi-hop-traversals)
5. [Aggregation and Statistics](#aggregation-and-statistics)
6. [Filtering and Search](#filtering-and-search)
7. [Complex Query Patterns](#complex-query-patterns)
8. [Performance Optimization](#performance-optimization)
9. [Common Query Recipes](#common-query-recipes)

---

## Understanding the Storage Model

### The Unified Table Structure

All nodes and edges are stored in a single table with these key columns:

```sql
CREATE TABLE pqg (
    row_id INTEGER PRIMARY KEY,    -- Internal identifier
    pid TEXT,                       -- Persistent identifier (for entities)
    otype TEXT,                     -- Object type: entity type OR '_edge_'
    s INTEGER,                      -- Subject row_id (for edges)
    p TEXT,                         -- Predicate (for edges)
    o INTEGER[],                    -- Array of object row_ids (for edges)
    n TEXT,                         -- Named graph / source identifier (e.g., 'OPENCONTEXT', 'SESAR')
    -- Plus entity-specific columns (label, description, etc.)
);
```

### Key Concepts

1. **Entities** have `otype` ∈ {MaterialSampleRecord, SamplingEvent, ...}
2. **Edges** have `otype = '_edge_'`
3. **Relationships** require joining through edge rows
4. **Multi-valued predicates** store multiple objects in `o` array

---

## Basic Entity Queries

### Count Entities by Type

```sql
-- Get counts of each entity type
SELECT
    otype,
    COUNT(*) as count
FROM pqg
WHERE otype != '_edge_'
GROUP BY otype
ORDER BY count DESC;
```

**Example output (OpenContext data):**
```
otype                            count
MaterialSampleRecord          1,096,352
IdentifiedConcept             8,270,644
GeospatialCoordLocation       1,095,912
SamplingSite                    383,912
SamplingEvent                 1,095,912
Agent                            72,520
```

### Find Entity by PID

```sql
-- Look up a specific sample
SELECT *
FROM pqg
WHERE pid = 'iSamples:OPENCONTEXT:1b22b93b-...'
  AND otype = 'MaterialSampleRecord';
```

### List All Samples with Basic Info

```sql
-- Get first 1000 samples with labels
SELECT
    pid,
    label,
    description
FROM pqg
WHERE otype = 'MaterialSampleRecord'
LIMIT 1000;
```

---

## Single-Hop Traversals

### Pattern: Entity → Edge → Entity

For a single relationship, you need:
1. Start entity (subject)
2. Edge row connecting them
3. Target entity (object)

### Example: Find Sampling Events for Samples

```sql
-- Which sampling event produced this sample?
SELECT
    sample.pid AS sample_id,
    sample.label AS sample_label,
    event.pid AS event_id,
    event.label AS event_label
FROM pqg AS sample
-- Join to edge
JOIN pqg AS edge
    ON edge.s = sample.row_id
    AND edge.p = 'produced_by'
    AND edge.otype = '_edge_'
-- Join to target entity
JOIN pqg AS event
    ON event.row_id = ANY(edge.o)
    AND event.otype = 'SamplingEvent'
WHERE sample.otype = 'MaterialSampleRecord'
LIMIT 100;
```

**Key pattern:**
- `edge.s = sample.row_id` - Edge starts at sample
- `edge.p = 'produced_by'` - Predicate identifies relationship type
- `event.row_id = ANY(edge.o)` - Handle multi-valued predicates
- Always filter by `otype` for performance

### Example: Find Material Categories for Sample

```sql
-- What material types does this sample have?
SELECT
    sample.pid AS sample_id,
    sample.label AS sample_label,
    material.pid AS material_category_id,
    material.label AS material_category
FROM pqg AS sample
JOIN pqg AS edge
    ON edge.s = sample.row_id
    AND edge.p = 'has_material_category'
JOIN pqg AS material
    ON material.row_id = ANY(edge.o)
    AND material.otype = 'IdentifiedConcept'
WHERE sample.pid = 'iSamples:OPENCONTEXT:...'
  AND sample.otype = 'MaterialSampleRecord';
```

**Note:** `has_material_category` is **multivalued**, so a sample may have multiple material types. The `ANY(edge.o)` handles this array.

---

## Multi-Hop Traversals

### Pattern: Chaining Relationships

Many useful queries require following multiple edges:

```
MaterialSampleRecord
  --produced_by--> SamplingEvent
  --sample_location--> GeospatialCoordLocation
```

### Example: Samples with Coordinates (2-hop)

```sql
-- Find all samples with geographic coordinates
SELECT
    sample.pid AS sample_id,
    sample.label AS sample_label,
    coords.latitude,
    coords.longitude,
    coords.elevation
FROM pqg AS sample
-- First hop: sample → event
JOIN pqg AS edge1
    ON edge1.s = sample.row_id
    AND edge1.p = 'produced_by'
JOIN pqg AS event
    ON event.row_id = ANY(edge1.o)
    AND event.otype = 'SamplingEvent'
-- Second hop: event → coordinates
JOIN pqg AS edge2
    ON edge2.s = event.row_id
    AND edge2.p = 'sample_location'
JOIN pqg AS coords
    ON coords.row_id = ANY(edge2.o)
    AND coords.otype = 'GeospatialCoordLocation'
WHERE sample.otype = 'MaterialSampleRecord'
  AND coords.latitude IS NOT NULL
  AND coords.longitude IS NOT NULL
LIMIT 1000;
```

**Performance note:** This is the most common query pattern in iSamples - optimize it with indexes on `row_id`, `s`, `p`, `otype`.

### Example: Samples → Site Name (3-hop)

```sql
-- Get sampling site names for samples
SELECT
    sample.pid AS sample_id,
    sample.label AS sample_label,
    site.pid AS site_id,
    site.label AS site_name,
    site_coords.latitude AS site_lat,
    site_coords.longitude AS site_lon
FROM pqg AS sample
-- Hop 1: sample → event
JOIN pqg AS edge1
    ON edge1.s = sample.row_id
    AND edge1.p = 'produced_by'
JOIN pqg AS event
    ON event.row_id = ANY(edge1.o)
    AND event.otype = 'SamplingEvent'
-- Hop 2: event → site
JOIN pqg AS edge2
    ON edge2.s = event.row_id
    AND edge2.p = 'sampling_site'
JOIN pqg AS site
    ON site.row_id = ANY(edge2.o)
    AND site.otype = 'SamplingSite'
-- Hop 3: site → coordinates
JOIN pqg AS edge3
    ON edge3.s = site.row_id
    AND edge3.p = 'site_location'
JOIN pqg AS site_coords
    ON site_coords.row_id = ANY(edge3.o)
    AND site_coords.otype = 'GeospatialCoordLocation'
WHERE sample.otype = 'MaterialSampleRecord'
LIMIT 1000;
```

**Design note:** `sampling_site` is optional in iSamples schema, so use `LEFT JOIN` if you want samples without sites.

---

## Aggregation and Statistics

### Count Edge Types in Dataset

```sql
-- Which relationship types are actually used?
SELECT
    otype AS subject_type,
    p AS predicate,
    COUNT(*) AS edge_count
FROM pqg
WHERE otype = '_edge_'
GROUP BY otype, p
ORDER BY edge_count DESC;
```

**Example output (OpenContext):**
```
subject_type  predicate                  edge_count
_edge_        has_sample_object_type      1,124,480
_edge_        produced_by                 1,096,352
_edge_        has_material_category       1,095,920
_edge_        has_context_category        1,095,912
_edge_        keywords                    1,070,912
```

### Samples per Material Category

```sql
-- How many samples for each material type?
SELECT
    material.label AS material_category,
    COUNT(DISTINCT sample.pid) AS sample_count
FROM pqg AS sample
JOIN pqg AS edge
    ON edge.s = sample.row_id
    AND edge.p = 'has_material_category'
JOIN pqg AS material
    ON material.row_id = ANY(edge.o)
    AND material.otype = 'IdentifiedConcept'
WHERE sample.otype = 'MaterialSampleRecord'
GROUP BY material.label
ORDER BY sample_count DESC
LIMIT 20;
```

### Geographic Bounding Box

```sql
-- Find extent of all sample locations
SELECT
    MIN(coords.latitude) AS min_lat,
    MAX(coords.latitude) AS max_lat,
    MIN(coords.longitude) AS min_lon,
    MAX(coords.longitude) AS max_lon,
    COUNT(DISTINCT sample.pid) AS sample_count
FROM pqg AS sample
JOIN pqg AS edge1 ON edge1.s = sample.row_id AND edge1.p = 'produced_by'
JOIN pqg AS event ON event.row_id = ANY(edge1.o)
JOIN pqg AS edge2 ON edge2.s = event.row_id AND edge2.p = 'sample_location'
JOIN pqg AS coords ON coords.row_id = ANY(edge2.o)
WHERE sample.otype = 'MaterialSampleRecord'
  AND coords.latitude IS NOT NULL
  AND coords.longitude IS NOT NULL;
```

---

## Filtering and Search

### Filter by Material Category

```sql
-- Find all pottery samples
SELECT
    sample.pid,
    sample.label,
    material.label AS material_type
FROM pqg AS sample
JOIN pqg AS edge
    ON edge.s = sample.row_id
    AND edge.p = 'has_material_category'
JOIN pqg AS material
    ON material.row_id = ANY(edge.o)
    AND material.otype = 'IdentifiedConcept'
WHERE sample.otype = 'MaterialSampleRecord'
  AND material.label ILIKE '%pottery%'
LIMIT 1000;
```

**Note:** Use `ILIKE` for case-insensitive matching, `LIKE` for case-sensitive.

### Filter by Geographic Region

```sql
-- Find samples in Turkey (approximate bounding box)
SELECT
    sample.pid,
    sample.label,
    coords.latitude,
    coords.longitude
FROM pqg AS sample
JOIN pqg AS edge1 ON edge1.s = sample.row_id AND edge1.p = 'produced_by'
JOIN pqg AS event ON event.row_id = ANY(edge1.o)
JOIN pqg AS edge2 ON edge2.s = event.row_id AND edge2.p = 'sample_location'
JOIN pqg AS coords ON coords.row_id = ANY(edge2.o)
WHERE sample.otype = 'MaterialSampleRecord'
  AND coords.latitude BETWEEN 36.0 AND 42.0
  AND coords.longitude BETWEEN 26.0 AND 45.0
LIMIT 1000;
```

### Filter by Keyword

```sql
-- Find samples with specific keyword
SELECT
    sample.pid,
    sample.label,
    keyword.label AS keyword
FROM pqg AS sample
JOIN pqg AS edge
    ON edge.s = sample.row_id
    AND edge.p = 'keywords'
JOIN pqg AS keyword
    ON keyword.row_id = ANY(edge.o)
    AND keyword.otype = 'IdentifiedConcept'
WHERE sample.otype = 'MaterialSampleRecord'
  AND keyword.label ILIKE '%neolithic%'
LIMIT 1000;
```

### Combine Multiple Filters

```sql
-- Find pottery samples from Turkey with coordinates
SELECT
    sample.pid,
    sample.label,
    material.label AS material,
    coords.latitude,
    coords.longitude
FROM pqg AS sample
-- Material category
JOIN pqg AS mat_edge
    ON mat_edge.s = sample.row_id
    AND mat_edge.p = 'has_material_category'
JOIN pqg AS material
    ON material.row_id = ANY(mat_edge.o)
    AND material.otype = 'IdentifiedConcept'
-- Coordinates
JOIN pqg AS event_edge
    ON event_edge.s = sample.row_id
    AND event_edge.p = 'produced_by'
JOIN pqg AS event
    ON event.row_id = ANY(event_edge.o)
JOIN pqg AS coord_edge
    ON coord_edge.s = event.row_id
    AND coord_edge.p = 'sample_location'
JOIN pqg AS coords
    ON coords.row_id = ANY(coord_edge.o)
    AND coords.otype = 'GeospatialCoordLocation'
WHERE sample.otype = 'MaterialSampleRecord'
  AND material.label ILIKE '%pottery%'
  AND coords.latitude BETWEEN 36.0 AND 42.0
  AND coords.longitude BETWEEN 26.0 AND 45.0
LIMIT 1000;
```

---

## Complex Query Patterns

### Find Samples Missing Specific Relationships

```sql
-- Samples without material category (quality check)
SELECT
    sample.pid,
    sample.label
FROM pqg AS sample
WHERE sample.otype = 'MaterialSampleRecord'
  AND NOT EXISTS (
    SELECT 1
    FROM pqg AS edge
    WHERE edge.s = sample.row_id
      AND edge.p = 'has_material_category'
      AND edge.otype = '_edge_'
  )
LIMIT 1000;
```

### Samples with Multiple Material Categories

```sql
-- Samples categorized as multiple material types
SELECT
    sample.pid,
    sample.label,
    ARRAY_AGG(material.label) AS material_categories,
    COUNT(*) AS category_count
FROM pqg AS sample
JOIN pqg AS edge
    ON edge.s = sample.row_id
    AND edge.p = 'has_material_category'
JOIN pqg AS material
    ON material.row_id = ANY(edge.o)
    AND material.otype = 'IdentifiedConcept'
WHERE sample.otype = 'MaterialSampleRecord'
GROUP BY sample.pid, sample.label
HAVING COUNT(*) > 1
ORDER BY category_count DESC
LIMIT 100;
```

### Hierarchical Queries (Parent-Child Samples)

```sql
-- Find child samples and their parents via SampleRelation
-- Note: SampleRelation has 'relationship' (type) and 'target' (PID) fields
SELECT
    child.pid AS child_id,
    child.label AS child_label,
    relation.relationship AS relationship_type,
    relation.target AS parent_pid
FROM pqg AS child
-- Child → SampleRelation edge
JOIN pqg AS edge1
    ON edge1.s = child.row_id
    AND edge1.p = 'related_resource'
JOIN pqg AS relation
    ON relation.row_id = ANY(edge1.o)
    AND relation.otype = 'SampleRelation'
WHERE child.otype = 'MaterialSampleRecord'
  AND relation.relationship = 'isPartOf'
LIMIT 1000;

-- To resolve the parent sample details, join on PID:
SELECT
    child.pid AS child_id,
    child.label AS child_label,
    relation.relationship AS relationship_type,
    parent.pid AS parent_id,
    parent.label AS parent_label
FROM pqg AS child
JOIN pqg AS edge1
    ON edge1.s = child.row_id
    AND edge1.p = 'related_resource'
JOIN pqg AS relation
    ON relation.row_id = ANY(edge1.o)
    AND relation.otype = 'SampleRelation'
JOIN pqg AS parent
    ON parent.pid = relation.target
    AND parent.otype = 'MaterialSampleRecord'
WHERE child.otype = 'MaterialSampleRecord'
  AND relation.relationship = 'isPartOf'
LIMIT 1000;
```

### Spatial Proximity Search

```sql
-- Find samples within ~10km of a point (approximate)
-- 1 degree latitude ≈ 111km, 1 degree longitude ≈ 111km * cos(latitude)
WITH target AS (
    SELECT 37.5 AS target_lat, 32.8 AS target_lon  -- Çatalhöyük
)
SELECT
    sample.pid,
    sample.label,
    coords.latitude,
    coords.longitude,
    -- Approximate distance in km
    111.0 * SQRT(
        POWER(coords.latitude - target.target_lat, 2) +
        POWER((coords.longitude - target.target_lon) * COS(RADIANS(target.target_lat)), 2)
    ) AS distance_km
FROM pqg AS sample
CROSS JOIN target
JOIN pqg AS edge1 ON edge1.s = sample.row_id AND edge1.p = 'produced_by'
JOIN pqg AS event ON event.row_id = ANY(edge1.o)
JOIN pqg AS edge2 ON edge2.s = event.row_id AND edge2.p = 'sample_location'
JOIN pqg AS coords ON coords.row_id = ANY(edge2.o)
WHERE sample.otype = 'MaterialSampleRecord'
  AND coords.latitude IS NOT NULL
  AND coords.longitude IS NOT NULL
  AND ABS(coords.latitude - target.target_lat) < 0.1    -- Pre-filter
  AND ABS(coords.longitude - target.target_lon) < 0.1
ORDER BY distance_km
LIMIT 100;
```

**Note:** For precise geospatial calculations, use PostGIS or DuckDB spatial extension.

---

## Performance Optimization

### Use Indexes

```sql
-- Create indexes for common join patterns
CREATE INDEX idx_row_id ON pqg(row_id);
CREATE INDEX idx_edge_s ON pqg(s);
CREATE INDEX idx_edge_p ON pqg(p);
CREATE INDEX idx_otype ON pqg(otype);
CREATE INDEX idx_pid ON pqg(pid);

-- Note: DuckDB does not support partial indexes (WHERE clause in CREATE INDEX).
-- For PostgreSQL, you can use partial indexes:
-- CREATE INDEX idx_edge_s ON pqg(s) WHERE otype = '_edge_';
```

### Filter Early

```sql
-- ❌ BAD: Filter after all joins
SELECT sample.pid, coords.latitude
FROM pqg AS sample
JOIN pqg AS edge1 ON edge1.s = sample.row_id
JOIN pqg AS event ON event.row_id = ANY(edge1.o)
JOIN pqg AS edge2 ON edge2.s = event.row_id
JOIN pqg AS coords ON coords.row_id = ANY(edge2.o)
WHERE sample.otype = 'MaterialSampleRecord'  -- Too late!
  AND coords.latitude > 40.0;

-- ✅ GOOD: Filter in JOIN conditions
SELECT sample.pid, coords.latitude
FROM pqg AS sample
JOIN pqg AS edge1
    ON edge1.s = sample.row_id
    AND edge1.p = 'produced_by'
    AND edge1.otype = '_edge_'
JOIN pqg AS event
    ON event.row_id = ANY(edge1.o)
    AND event.otype = 'SamplingEvent'
JOIN pqg AS edge2
    ON edge2.s = event.row_id
    AND edge2.p = 'sample_location'
    AND edge2.otype = '_edge_'
JOIN pqg AS coords
    ON coords.row_id = ANY(edge2.o)
    AND coords.otype = 'GeospatialCoordLocation'
    AND coords.latitude > 40.0  -- Filter here!
WHERE sample.otype = 'MaterialSampleRecord';
```

### Use CTEs for Readability

```sql
-- Break complex queries into steps
WITH samples_with_events AS (
    SELECT
        sample.row_id AS sample_row_id,
        sample.pid AS sample_pid,
        sample.label AS sample_label,
        event.row_id AS event_row_id
    FROM pqg AS sample
    JOIN pqg AS edge ON edge.s = sample.row_id AND edge.p = 'produced_by'
    JOIN pqg AS event ON event.row_id = ANY(edge.o)
    WHERE sample.otype = 'MaterialSampleRecord'
      AND event.otype = 'SamplingEvent'
),
events_with_coords AS (
    SELECT
        swe.sample_row_id,
        swe.sample_pid,
        swe.sample_label,
        coords.latitude,
        coords.longitude
    FROM samples_with_events swe
    JOIN pqg AS edge ON edge.s = swe.event_row_id AND edge.p = 'sample_location'
    JOIN pqg AS coords ON coords.row_id = ANY(edge.o)
    WHERE coords.otype = 'GeospatialCoordLocation'
      AND coords.latitude IS NOT NULL
)
SELECT * FROM events_with_coords
LIMIT 1000;
```

### Limit Result Sets

```sql
-- Always use LIMIT for exploratory queries
SELECT * FROM pqg LIMIT 1000;  -- ✅

-- Dangerous without LIMIT on large datasets
SELECT * FROM pqg;  -- ❌ Could return millions of rows
```

---

## Common Query Recipes

### Recipe 1: Export Samples with Full Metadata

```sql
-- Complete sample export with all key attributes
SELECT
    sample.pid AS sample_id,
    sample.label AS sample_name,
    sample.description,
    material.label AS material_type,
    context.label AS context_category,
    coords.latitude,
    coords.longitude,
    coords.elevation,
    site.label AS site_name,
    agent.name AS collector
FROM pqg AS sample
-- Material
LEFT JOIN pqg AS mat_edge ON mat_edge.s = sample.row_id AND mat_edge.p = 'has_material_category'
LEFT JOIN pqg AS material ON material.row_id = ANY(mat_edge.o) AND material.otype = 'IdentifiedConcept'
-- Context
LEFT JOIN pqg AS ctx_edge ON ctx_edge.s = sample.row_id AND ctx_edge.p = 'has_context_category'
LEFT JOIN pqg AS context ON context.row_id = ANY(ctx_edge.o) AND context.otype = 'IdentifiedConcept'
-- Event and location
LEFT JOIN pqg AS event_edge ON event_edge.s = sample.row_id AND event_edge.p = 'produced_by'
LEFT JOIN pqg AS event ON event.row_id = ANY(event_edge.o) AND event.otype = 'SamplingEvent'
LEFT JOIN pqg AS coord_edge ON coord_edge.s = event.row_id AND coord_edge.p = 'sample_location'
LEFT JOIN pqg AS coords ON coords.row_id = ANY(coord_edge.o) AND coords.otype = 'GeospatialCoordLocation'
-- Site
LEFT JOIN pqg AS site_edge ON site_edge.s = event.row_id AND site_edge.p = 'sampling_site'
LEFT JOIN pqg AS site ON site.row_id = ANY(site_edge.o) AND site.otype = 'SamplingSite'
-- Collector
LEFT JOIN pqg AS agent_edge ON agent_edge.s = event.row_id AND agent_edge.p = 'responsibility'
LEFT JOIN pqg AS agent ON agent.row_id = ANY(agent_edge.o) AND agent.otype = 'Agent'
WHERE sample.otype = 'MaterialSampleRecord'
LIMIT 10000;
```

### Recipe 2: Validate Data Quality

```sql
-- Find samples with potential data issues
SELECT
    'No material category' AS issue,
    COUNT(*) AS count
FROM pqg AS sample
WHERE sample.otype = 'MaterialSampleRecord'
  AND NOT EXISTS (
    SELECT 1 FROM pqg AS edge
    WHERE edge.s = sample.row_id AND edge.p = 'has_material_category'
  )
UNION ALL
SELECT
    'No sampling event',
    COUNT(*)
FROM pqg AS sample
WHERE sample.otype = 'MaterialSampleRecord'
  AND NOT EXISTS (
    SELECT 1 FROM pqg AS edge
    WHERE edge.s = sample.row_id AND edge.p = 'produced_by'
  )
UNION ALL
SELECT
    'No coordinates',
    COUNT(*)
FROM pqg AS sample
WHERE sample.otype = 'MaterialSampleRecord'
  AND NOT EXISTS (
    SELECT 1 FROM pqg AS e1
    JOIN pqg AS event ON event.row_id = ANY(e1.o)
    JOIN pqg AS e2 ON e2.s = event.row_id AND e2.p = 'sample_location'
    WHERE e1.s = sample.row_id AND e1.p = 'produced_by'
  );
```

### Recipe 3: Generate GeoJSON

```sql
-- Create GeoJSON for web mapping
SELECT json_object(
    'type', 'FeatureCollection',
    'features', json_group_array(
        json_object(
            'type', 'Feature',
            'geometry', json_object(
                'type', 'Point',
                'coordinates', json_array(coords.longitude, coords.latitude)
            ),
            'properties', json_object(
                'id', sample.pid,
                'label', sample.label,
                'material', material.label
            )
        )
    )
) AS geojson
FROM pqg AS sample
JOIN pqg AS mat_edge ON mat_edge.s = sample.row_id AND mat_edge.p = 'has_material_category'
JOIN pqg AS material ON material.row_id = ANY(mat_edge.o)
JOIN pqg AS event_edge ON event_edge.s = sample.row_id AND event_edge.p = 'produced_by'
JOIN pqg AS event ON event.row_id = ANY(event_edge.o)
JOIN pqg AS coord_edge ON coord_edge.s = event.row_id AND coord_edge.p = 'sample_location'
JOIN pqg AS coords ON coords.row_id = ANY(coord_edge.o)
WHERE sample.otype = 'MaterialSampleRecord'
  AND coords.latitude IS NOT NULL
  AND coords.longitude IS NOT NULL
LIMIT 1000;
```

### Recipe 4: Time Series Analysis

```sql
-- Samples by collection year (if date data available)
SELECT
    EXTRACT(YEAR FROM event.result_time) AS collection_year,
    COUNT(DISTINCT sample.pid) AS sample_count
FROM pqg AS sample
JOIN pqg AS edge ON edge.s = sample.row_id AND edge.p = 'produced_by'
JOIN pqg AS event ON event.row_id = ANY(edge.o)
WHERE sample.otype = 'MaterialSampleRecord'
  AND event.otype = 'SamplingEvent'
  AND event.result_time IS NOT NULL
GROUP BY collection_year
ORDER BY collection_year;
```

---

## Next Steps

- **Visual diagrams**: See [EDGE_TYPES_VISUAL.md](EDGE_TYPES_VISUAL.md) for entity relationship diagrams
- **Predicate reference**: See [PREDICATES_REFERENCE.md](PREDICATES_REFERENCE.md) for detailed predicate documentation
- **Graph structure**: See [UNDERSTANDING_THE_GRAPH.md](UNDERSTANDING_THE_GRAPH.md) for conceptual overview
- **Real examples**: See [EXAMPLES_BY_DOMAIN.md](EXAMPLES_BY_DOMAIN.md) for complete domain-specific examples

---

## Tips and Best Practices

1. **Always filter by `otype`** in JOIN conditions for performance
2. **Use `ANY(edge.o)`** to handle multi-valued predicates correctly
3. **Start simple** - test single-hop queries before chaining multiple relationships
4. **Use CTEs** to break down complex queries into understandable steps
5. **Add LIMIT** to all exploratory queries
6. **Check for NULL values** in coordinate and date fields
7. **Use LEFT JOIN** when relationships are optional
8. **Explain your queries** with `EXPLAIN QUERY PLAN` to optimize performance
9. **Batch queries** when possible instead of running thousands individually
10. **Document your patterns** - complex graph traversals are hard to remember!

---

**Last updated:** 2025-11-14
**Part of:** iSamples Property Graph Documentation Suite

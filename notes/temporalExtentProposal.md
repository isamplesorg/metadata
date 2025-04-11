# Temporal Extent
The temporal extent extension for the iSamples sample metadata scheme allows declaration of a time position or interval that is significant for understanding the context of a material sample. Typically this is the time at which the sampled feature originated, was used, was alive or some other event in the history of the sample. Temporal extents can be specified using various systems (see [Time Ontology](https://w3c.github.io/sdw/time/), and allowing any possible representation would complicate interperability. We thus provide recommendations for a subset of approaches.

Extents can be specified with calendar dates, numerical coordinates, or using named temporal eras.  Example numeric systems include years before present (with various interpretations of what 'present' means), C.E./B.C.E years, unix time, julian date.  Reference systems based on named eras include various geological time scales, the dynasties of ancient Egypt, reigns of English kings, ceramic-style chronologies. 
For isamplesPurposes the following scheme is proposed. 
MaterialSampleReord has optional temporalExtent property
the value of the temporalExtent property is a TimePosition object with the following properties.
- numeric_younger_bound: decimal number
- numeric_older_bound: decimal number
- numeric_reference_system: identifiedConcept
- era_name_younger: identifiedConcept
- era_name_older: identifiedConcept
- era_reference_system: identifiedConcept
- date_time: string (ISO8601)
- event: identifiedConcept
- evidence: text

## Explanation

To be useful, a temporal extent specification must include at least one numeric bound, named era bound, or date-time specification. 

The identifiedConcept value type used in various places is based on the pattern used in schema.org, DataCite and other metadata schemes, allowing inclusion of a label, identifier, and specification of the containing vocabulary. 

### Numeric bounds
A numeric value that is a position on a one-dimension temporal coordinate system.  Values are quantized at some level, e.g. to the year, thousand year, million year. The units are specified in the numeric reference system definition. A younger and older bound can be provided; The extent is specified by a single value (the lower and upper bound are not distinct at the resolution of the value), the lower and upper bound are the same value.  The bounds should include the uncertainty limits on the values. 
### Numeric_reference_system
Name, URI, or text description specifying the temporal coordinate system, including origin, unit of measure, and positive direction.  
### Named eras
Name and optional URI (identifier) for a time ordinal era, which is a time interval defined by bounding events that do not necessarily have known temporal coordinates. Chronologic relationships between events (before, after..) might be known to allow determination of temporal topologic relationships ([Allen, 1984](http://dx.doi.org/10.1016/0004-3702%2884%2990008-0), [Allen and Ferguson, 1997](http://dx.doi.org/10.1007/978-0-585-28322-7_7) ) between the intervals. 
### Era reference system
A set of time ordinal eras used to assign temporal positions (https://w3c.github.io/sdw/time/#time:TRS). Note that in the original W3C formulation, the boundaries of the eras were required to be date-time positions; the [Cox and Richard 2014](http://dx.doi.org/10.1007/s12145-014-0170-6) formulation for the geologic time scale generalizes this to allow other boundary definitions applicable in domains dealing with intervals that predate calendar time.
### Data and time
This field is for extents that are within the scope of define calendar dates and/or times that can be represented using the syntax defined by [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) (see [Wikipedia page](https://en.wikipedia.org/wiki/ISO_8601) for a non-paywall description). This syntax allows representing individual dates with or without time(and time zone), as well as intervals (closed or open ended). 
### Event
Material samples (endurants) do not have an age; events have an age (temporal extent). We are interested in the events that will assist in sample discovery and assessment using iSamples metadata.  The value here would ideally be a registered identifier for a scheme useful across domains; multiple values might be provided with different granularity, ranging from cross domain to research-group specific. Use of the schema.org/DefinedTerm construct (or a similare implementation) allow inclusion of the identifier, label. and scheme name.
### Evidence
Text description of the basis for assigning a temporal extent to event in the history of the sample.

#Reading
[ŠUMRADA, 2003, Temporal Data and Temporal Reference Systems](https://www.fig.net/resources/proceedings/fig_proceedings/fig_2003/TS_10/TS10_3_Sumrada.pdf)

Schema;
YAML definition additions:
classes:
  MaterialSampleRecord:
    slots:
      - temporal_extent
  TimePosition:
    slots:
      - numeric_younger_bound
      - numeric_older_bound
      - numeric_reference_system
      - era_name_younger
      - era_name_older
      - era_reference_system
      - date_time
      - event
      - evidence
    IdentifiedConcept:
      slots:
        -
  slots:
    temporal_extent:
      range: TimePosition
      multivalued: true
    numeric_younger_bound:
      range: decimal
      multivalued: false
    numeric_older_bound:
      range: decimal
      multivalued: false
    numeric_reference_system:
      range:IdentifiedConcept
      multivalued: false
    era_name_younger:
      range:IdentifiedConcept
      multivalued: false
    era_name_older:
      range:IdentifiedConcept
      multivalued: false
    era_reference_system
    date_time
      range: string
      any_of:
       - range: date
       - range: datetime
       - pattern: "^(?:[1]?[0-9]{3}|20[0-2][0-9])$"
       - pattern: "^(?:[1]?[0-9]{3}|20[0-2][0-9])-(?:0[1-9]|1[0-2])$"
      description: use ISO8601 syntax
    event:
      range:IdentifiedConcept
      multivalued: false
    evidence:
      range: string
  

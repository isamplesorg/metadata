# Temporal Extent
The temporal extent extension for the iSamples sample metadata scheme allows declaration of a time position or interval that is significant for understanding the context of a material sample. Typically this is the time at which the sampled feature originated, was used, was alive or some other event in the history of the sample. Temporal extents can be specified using various systems (see [Time Ontology](https://w3c.github.io/sdw/time/), and allowing any possible representation would complicate interperability. We thus provide recommendations for a subset of approaches.

Extents can be specified with calendar dates, numerical coordinates, or using named temporal eras.  Example numeric systems include years before present (with various interpretations of what 'present' means), C.E./B.C.E years, unix time, julian date.  Reference systems based on named eras include various geological time scales, the dynasties of ancient Egypt, reigns of English kings, ceramic-style chronologies. 
For isamplesPurposes the following scheme is proposed. 
MaterialSampleReord has optional temporalExtent property
the value of the temporalExtent property is a TimePosition object with the following properties
- numeric_younger_bound: decimal number
- numeric_older_bound: decimal number
- numeric_reference_system: name or URI identifing the temporal coordinate system, including origin, unit of measure, and positive direction.
- 

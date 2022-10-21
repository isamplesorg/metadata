
# physicalSample


**metamodel version:** 1.7.0

**version:** 20221007


Startup schema for iSamples sample registry integration. updated from 0.2 by synchronizing the vocabulary enumerations, change 'id' to '@id' and 'schema' to '$schema'.  Schema name is iSamplesSchemaBasic0.2.1.json. Target JSON schema version is http://json-schema.org/draft-07/schema# SMR 2022-10-07


### Classes

 * [Curation](Curation.md) - object contains information about current storage of sample, access to sample, and events in curation history. Curation as used here starts when the sample is removed from its original context, and might include various processing steps for preservation.  Processing related to analysis preparation such as crushing, dissolution, evaporation, filtering are considered part of the sampling method for the derived child sample.
 * [GeospatialDDCoordLocation](GeospatialDDCoordLocation.md)
 * [PhysicalSampleRecord](PhysicalSampleRecord.md) - This is a data object that is a digital representation of a physical sample, and thus shares the same identifier as the physical object. It provides  descriptive properties for any iSamples physical sample, URI for the metadata record is same as URI for physical sample-- digital object is considered twin of physical object, a representation. IGSN is recommended. Must be a URI that can be dereferenced on the web.
 * [SampleRelation](SampleRelation.md)
 * [SamplingEvent](SamplingEvent.md)
 * [SamplingSite](SamplingSite.md)

### Mixins


### Slots

 * [$schema]($schema.md) - identifier for the JSON schema for validating this document
 * [@id](@id.md) - identifier for this document
 * [accessConstraints](accessConstraints.md) - cultural, legal or other policy issues that bear on access to view, borrow, or subsample a sample or visit a sampling site.
 * [authorizedBy](authorizedBy.md)
 * [compliesWith](compliesWith.md)
 * [curation](curation.md)
 * [curationLocation](curationLocation.md) - information about where and how the sample is currently stored
 * [description](description.md) - free text description of the subject of a triple.
 * [elevation](elevation.md) - should be a number and Unit of measure, and the datum. e.g. 401 m above mean sea level.
 * [hasContextCategory](hasContextCategory.md) - top level context, based on the kind of feature sampled.  Specific identification of the sampled feature of interest is done through the SamplingEvent/Feature of Interest property.
 * [hasFeatureOfInterest](hasFeatureOfInterest.md) - what does the sample represent.
 * [hasMaterialCategory](hasMaterialCategory.md) - specify the kind of material that constitutes the sample
 * [hasSpecimenCategory](hasSpecimenCategory.md) - specify the kind of object that the specimen is
 * [informalClassification](informalClassification.md) - free text classification terms, not from a controlled vocabulary; generally terms applied by collector
 * [keywords](keywords.md) - free text categorization of sample to support discovery
 * [label](label.md) - a human intelligible string used to identify a thing, i.e. the name to use for the thing; should be unique in the scope of a sample collection or dataset.
     * [PhysicalSampleRecord➞label](PhysicalSampleRecord_label.md)
 * [latitude](latitude.md) - angular coordinate measured positive north from the equator.
 * [location](location.md) - geopatial location of site; required default is WGS84 latitude, longitude in decimal degrees. Elevation as a string with number, unit of measure, and datum.
 * [longitude](longitude.md) - angular coordinate measured positive eastward from the prime meridian.
 * [placeName](placeName.md) - one or more names by which the sampling site is known.
 * [producedBy](producedBy.md) - object that documents the sampling event--who, where, when the specimen was obtained
 * [registrant](registrant.md) - identification of the agent that registered the sample, with contact information. Should include person name and affiliation, or position name and affiliation, or just organization name. e-mail address is preferred contact information.
 * [relatedResource](relatedResource.md) - link to related resource with relationship property to indicate nature of connection. Target should be identifier for a resource.
 * [relationship](relationship.md) - term to identify realationship between host sample and the sample relation target. Should be controlled vocabulary (ScopedName). for now start with string, 'derivedFrom'.
 * [responsibility](responsibility.md) - String with person name and affiliation, or organization name, and their role relative to the parent element.
 * [resultTime](resultTime.md) - Date on which the sample was collected.
 * [sampleidentifier](sampleidentifier.md) - URI that identifies the physical sample described by this record
     * [PhysicalSampleRecord➞sampleidentifier](PhysicalSampleRecord_sampleidentifier.md)
 * [samplingPurpose](samplingPurpose.md) - term to specify why a sample was collection.
 * [samplingSite](samplingSite.md) - object that identifies the place where the sample was collected
 * [target](target.md) - identifier for the target resource in the relationship. Start with string, should be Identifier object.

### Enums

 * [contextcategory](contextcategory.md) - top level context, based on the kind of feature sampled,from the SampledFeature vocabulary.  Specific identification of the sampled feature of interest is done through the SamplingEvent/Feature of Interest property.
 * [materialtype](materialtype.md) - categories for kinds of material that constitute the sample
 * [specimencategory](specimencategory.md) - specify the kind of object that the specimen is

### Subsets


### Types


#### Built in

 * **Decimal**
 * **str**

#### Defined

 * [Date](types/Date.md)  (**str**) 
 * [Decimal](types/Decimal.md)  (**Decimal**) 
 * [String](types/String.md)  (**str**) 

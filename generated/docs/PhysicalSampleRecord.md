
# Class: PhysicalSampleRecord


This is a data object that is a digital representation of a physical sample, and thus shares the same identifier as the physical object. It provides  descriptive properties for any iSamples physical sample, URI for the metadata record is same as URI for physical sample-- digital object is considered twin of physical object, a representation. IGSN is recommended. Must be a URI that can be dereferenced on the web.

URI: [isam:PhysicalSampleRecord](http://resource.isamples.org/schema/PhysicalSampleRecord)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SamplingEvent],[SampleRelation],[SampleRelation]<relatedResource%200..1-++[PhysicalSampleRecord&#124;$schema:string%20%3F;@id:string%20%3F;label:string;sampleidentifier:string;description:string%20%3F;hasContextCategory:string%20*;hasMaterialCategory:materialtype%20*;hasSpecimenCategory:string%20*;informalClassification:string%20*;keywords:string%20*;registrant:string%20%3F;samplingPurpose:string%20%3F;authorizedBy:string%20%3F;compliesWith:string%20%3F],[Curation]<curation%200..1-++[PhysicalSampleRecord],[SamplingEvent]<producedBy%200..1-++[PhysicalSampleRecord],[Curation])](https://yuml.me/diagram/nofunky;dir:TB/class/[SamplingEvent],[SampleRelation],[SampleRelation]<relatedResource%200..1-++[PhysicalSampleRecord&#124;$schema:string%20%3F;@id:string%20%3F;label:string;sampleidentifier:string;description:string%20%3F;hasContextCategory:string%20*;hasMaterialCategory:materialtype%20*;hasSpecimenCategory:string%20*;informalClassification:string%20*;keywords:string%20*;registrant:string%20%3F;samplingPurpose:string%20%3F;authorizedBy:string%20%3F;compliesWith:string%20%3F],[Curation]<curation%200..1-++[PhysicalSampleRecord],[SamplingEvent]<producedBy%200..1-++[PhysicalSampleRecord],[Curation])

## Referenced by Class


## Attributes


### Own

 * [$schema]($schema.md)  <sub>0..1</sub>
     * Description: identifier for the JSON schema for validating this document
     * Range: [String](types/String.md)
 * [@id](@id.md)  <sub>0..1</sub>
     * Description: identifier for this document
     * Range: [String](types/String.md)
 * [PhysicalSampleRecord➞label](PhysicalSampleRecord_label.md)  <sub>1..1</sub>
     * Description: a human intelligible string used to identify a thing, i.e. the name to use for the thing; should be unique in the scope of a sample collection or dataset.
     * Range: [String](types/String.md)
 * [PhysicalSampleRecord➞sampleidentifier](PhysicalSampleRecord_sampleidentifier.md)  <sub>1..1</sub>
     * Description: URI that identifies the physical sample described by this record
     * Range: [String](types/String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Description: free text description of the subject of a triple.
     * Range: [String](types/String.md)
 * [hasContextCategory](hasContextCategory.md)  <sub>0..\*</sub>
     * Description: top level context, based on the kind of feature sampled.  Specific identification of the sampled feature of interest is done through the SamplingEvent/Feature of Interest property.
     * Range: [String](types/String.md)
 * [hasMaterialCategory](hasMaterialCategory.md)  <sub>0..\*</sub>
     * Description: specify the kind of material that constitutes the sample
     * Range: [materialtype](materialtype.md)
 * [hasSpecimenCategory](hasSpecimenCategory.md)  <sub>0..\*</sub>
     * Description: specify the kind of object that the specimen is
     * Range: [String](types/String.md)
 * [informalClassification](informalClassification.md)  <sub>0..\*</sub>
     * Description: free text classification terms, not from a controlled vocabulary; generally terms applied by collector
     * Range: [String](types/String.md)
 * [keywords](keywords.md)  <sub>0..\*</sub>
     * Description: free text categorization of sample to support discovery
     * Range: [String](types/String.md)
 * [producedBy](producedBy.md)  <sub>0..1</sub>
     * Description: object that documents the sampling event--who, where, when the specimen was obtained
     * Range: [SamplingEvent](SamplingEvent.md)
 * [registrant](registrant.md)  <sub>0..1</sub>
     * Description: identification of the agent that registered the sample, with contact information. Should include person name and affiliation, or position name and affiliation, or just organization name. e-mail address is preferred contact information.
     * Range: [String](types/String.md)
 * [samplingPurpose](samplingPurpose.md)  <sub>0..1</sub>
     * Description: term to specify why a sample was collection.
     * Range: [String](types/String.md)
 * [curation](curation.md)  <sub>0..1</sub>
     * Range: [Curation](Curation.md)
 * [relatedResource](relatedResource.md)  <sub>0..1</sub>
     * Description: link to related resource with relationship property to indicate nature of connection. Target should be identifier for a resource.
     * Range: [SampleRelation](SampleRelation.md)
 * [authorizedBy](authorizedBy.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [compliesWith](compliesWith.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)

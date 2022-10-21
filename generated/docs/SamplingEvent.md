
# Class: SamplingEvent




URI: [isam:SamplingEvent](http://resource.isamples.org/schema/SamplingEvent)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SamplingSite],[SamplingSite]<samplingSite%200..1-++[SamplingEvent&#124;@id:string%20%3F;label:string%20%3F;description:string%20%3F;hasFeatureOfInterest:string%20%3F;responsibility:string%20*;resultTime:date%20%3F],[PhysicalSampleRecord]++-%20producedBy%200..1>[SamplingEvent],[PhysicalSampleRecord])](https://yuml.me/diagram/nofunky;dir:TB/class/[SamplingSite],[SamplingSite]<samplingSite%200..1-++[SamplingEvent&#124;@id:string%20%3F;label:string%20%3F;description:string%20%3F;hasFeatureOfInterest:string%20%3F;responsibility:string%20*;resultTime:date%20%3F],[PhysicalSampleRecord]++-%20producedBy%200..1>[SamplingEvent],[PhysicalSampleRecord])

## Referenced by Class

 *  **[PhysicalSampleRecord](PhysicalSampleRecord.md)** *[producedBy](producedBy.md)*  <sub>0..1</sub>  **[SamplingEvent](SamplingEvent.md)**

## Attributes


### Own

 * [@id](@id.md)  <sub>0..1</sub>
     * Description: identifier for this document
     * Range: [String](types/String.md)
 * [label](label.md)  <sub>0..1</sub>
     * Description: a human intelligible string used to identify a thing, i.e. the name to use for the thing; should be unique in the scope of a sample collection or dataset.
     * Range: [String](types/String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Description: free text description of the subject of a triple.
     * Range: [String](types/String.md)
 * [hasFeatureOfInterest](hasFeatureOfInterest.md)  <sub>0..1</sub>
     * Description: what does the sample represent.
     * Range: [String](types/String.md)
 * [responsibility](responsibility.md)  <sub>0..\*</sub>
     * Description: String with person name and affiliation, or organization name, and their role relative to the parent element.
     * Range: [String](types/String.md)
 * [resultTime](resultTime.md)  <sub>0..1</sub>
     * Description: Date on which the sample was collected.
     * Range: [Date](types/Date.md)
 * [samplingSite](samplingSite.md)  <sub>0..1</sub>
     * Description: object that identifies the place where the sample was collected
     * Range: [SamplingSite](SamplingSite.md)

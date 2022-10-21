
# Class: SampleRelation




URI: [isam:SampleRelation](http://resource.isamples.org/schema/SampleRelation)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[PhysicalSampleRecord]++-%20relatedResource%200..1>[SampleRelation&#124;label:string%20%3F;description:string%20%3F;relationship:string%20%3F;target:string%20%3F],[PhysicalSampleRecord])](https://yuml.me/diagram/nofunky;dir:TB/class/[PhysicalSampleRecord]++-%20relatedResource%200..1>[SampleRelation&#124;label:string%20%3F;description:string%20%3F;relationship:string%20%3F;target:string%20%3F],[PhysicalSampleRecord])

## Referenced by Class

 *  **None** *[relatedResource](relatedResource.md)*  <sub>0..1</sub>  **[SampleRelation](SampleRelation.md)**

## Attributes


### Own

 * [label](label.md)  <sub>0..1</sub>
     * Description: a human intelligible string used to identify a thing, i.e. the name to use for the thing; should be unique in the scope of a sample collection or dataset.
     * Range: [String](types/String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Description: free text description of the subject of a triple.
     * Range: [String](types/String.md)
 * [relationship](relationship.md)  <sub>0..1</sub>
     * Description: term to identify realationship between host sample and the sample relation target. Should be controlled vocabulary (ScopedName). for now start with string, 'derivedFrom'.
     * Range: [String](types/String.md)
 * [target](target.md)  <sub>0..1</sub>
     * Description: identifier for the target resource in the relationship. Start with string, should be Identifier object.
     * Range: [String](types/String.md)

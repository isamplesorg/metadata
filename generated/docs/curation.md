
# Class: Curation


object contains information about current storage of sample, access to sample, and events in curation history. Curation as used here starts when the sample is removed from its original context, and might include various processing steps for preservation.  Processing related to analysis preparation such as crushing, dissolution, evaporation, filtering are considered part of the sampling method for the derived child sample.

URI: [isam:Curation](http://resource.isamples.org/schema/Curation)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[PhysicalSampleRecord]++-%20curation%200..1>[Curation&#124;label:string%20%3F;description:string%20%3F;accessConstraints:string%20*;curationLocation:string%20%3F;responsibility:string%20*],[PhysicalSampleRecord])](https://yuml.me/diagram/nofunky;dir:TB/class/[PhysicalSampleRecord]++-%20curation%200..1>[Curation&#124;label:string%20%3F;description:string%20%3F;accessConstraints:string%20*;curationLocation:string%20%3F;responsibility:string%20*],[PhysicalSampleRecord])

## Referenced by Class

 *  **None** *[curation](curation.md)*  <sub>0..1</sub>  **[Curation](Curation.md)**

## Attributes


### Own

 * [label](label.md)  <sub>0..1</sub>
     * Description: a human intelligible string used to identify a thing, i.e. the name to use for the thing; should be unique in the scope of a sample collection or dataset.
     * Range: [String](types/String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Description: free text description of the subject of a triple.
     * Range: [String](types/String.md)
 * [accessConstraints](accessConstraints.md)  <sub>0..\*</sub>
     * Description: cultural, legal or other policy issues that bear on access to view, borrow, or subsample a sample or visit a sampling site.
     * Range: [String](types/String.md)
 * [curationLocation](curationLocation.md)  <sub>0..1</sub>
     * Description: information about where and how the sample is currently stored
     * Range: [String](types/String.md)
 * [responsibility](responsibility.md)  <sub>0..\*</sub>
     * Description: String with person name and affiliation, or organization name, and their role relative to the parent element.
     * Range: [String](types/String.md)

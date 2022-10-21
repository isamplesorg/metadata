
# Class: SamplingSite




URI: [isam:SamplingSite](http://resource.isamples.org/schema/SamplingSite)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[GeospatialDDCoordLocation]<location%200..1-++[SamplingSite&#124;label:string%20%3F;description:string%20%3F;placeName:string%20*],[SamplingEvent]++-%20samplingSite%200..1>[SamplingSite],[SamplingEvent],[GeospatialDDCoordLocation])](https://yuml.me/diagram/nofunky;dir:TB/class/[GeospatialDDCoordLocation]<location%200..1-++[SamplingSite&#124;label:string%20%3F;description:string%20%3F;placeName:string%20*],[SamplingEvent]++-%20samplingSite%200..1>[SamplingSite],[SamplingEvent],[GeospatialDDCoordLocation])

## Referenced by Class

 *  **[SamplingEvent](SamplingEvent.md)** *[samplingSite](samplingSite.md)*  <sub>0..1</sub>  **[SamplingSite](SamplingSite.md)**

## Attributes


### Own

 * [label](label.md)  <sub>0..1</sub>
     * Description: a human intelligible string used to identify a thing, i.e. the name to use for the thing; should be unique in the scope of a sample collection or dataset.
     * Range: [String](types/String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Description: free text description of the subject of a triple.
     * Range: [String](types/String.md)
 * [location](location.md)  <sub>0..1</sub>
     * Description: geopatial location of site; required default is WGS84 latitude, longitude in decimal degrees. Elevation as a string with number, unit of measure, and datum.
     * Range: [GeospatialDDCoordLocation](GeospatialDDCoordLocation.md)
 * [placeName](placeName.md)  <sub>0..\*</sub>
     * Description: one or more names by which the sampling site is known.
     * Range: [String](types/String.md)

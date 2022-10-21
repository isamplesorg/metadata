
# Class: GeospatialDDCoordLocation




URI: [isam:GeospatialDDCoordLocation](http://resource.isamples.org/schema/GeospatialDDCoordLocation)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SamplingSite],[SamplingSite]++-%20location%200..1>[GeospatialDDCoordLocation&#124;elevation:string%20%3F;latitude:decimal%20%3F;longitude:decimal%20%3F])](https://yuml.me/diagram/nofunky;dir:TB/class/[SamplingSite],[SamplingSite]++-%20location%200..1>[GeospatialDDCoordLocation&#124;elevation:string%20%3F;latitude:decimal%20%3F;longitude:decimal%20%3F])

## Referenced by Class

 *  **[SamplingSite](SamplingSite.md)** *[location](location.md)*  <sub>0..1</sub>  **[GeospatialDDCoordLocation](GeospatialDDCoordLocation.md)**

## Attributes


### Own

 * [elevation](elevation.md)  <sub>0..1</sub>
     * Description: should be a number and Unit of measure, and the datum. e.g. 401 m above mean sea level.
     * Range: [String](types/String.md)
 * [latitude](latitude.md)  <sub>0..1</sub>
     * Description: angular coordinate measured positive north from the equator.
     * Range: [Decimal](types/Decimal.md)
 * [longitude](longitude.md)  <sub>0..1</sub>
     * Description: angular coordinate measured positive eastward from the prime meridian.
     * Range: [Decimal](types/Decimal.md)

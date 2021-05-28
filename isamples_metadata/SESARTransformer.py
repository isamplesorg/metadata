import typing
import logging
from isamples_metadata.Transformer import Transformer


class SESARTransformer(Transformer):
    """Concrete transformer class for going from a SESAR record to an iSamples record"""

    def transform(self) -> typing.Dict:
        transformed_record = super(SESARTransformer, self).transform()
        return transformed_record

    def _source_record_description(self) -> typing.Dict:
        return self.source_record["description"]

    def _supplement_metadata(self) -> typing.Dict:
        description = self._source_record_description()
        if description is not None:
            return self._source_record_description()["supplementMetadata"]
        return {}

    @staticmethod
    def _logger():
        return logging.getLogger("isamples_metadata.SESARTransformer")

    def sample_identifier_scheme(self) -> typing.AnyStr:
        return "igsn"

    def sample_identifier_value(self) -> typing.AnyStr:
        return self.source_record["igsn"]

    def sample_label(self) -> typing.AnyStr:
        return self._source_record_description()["sampleName"]

    def sample_description(self) -> typing.AnyStr:
        # TODO: implement
        return Transformer.NOT_PROVIDED

    def has_context_categories(self) -> typing.List:
        return ["Subsurface fluid reservoir"]

    def has_material_categories(self) -> typing.List:
        return ["Gaseous material"]

    def has_specimen_categories(self) -> typing.List:
        return ["Container with fluid"]

    def keywords(self) -> typing.List:
        return [self._source_record_description()["sampleType"]]

    def _contributor_name_with_role(self, role_name: typing.AnyStr):
        contributor_name = ""
        contributors = self._source_record_description()["contributors"]
        if contributors is not None and len(contributors) > 0:
            contributors_with_role = list(
                filter(
                    lambda contributor_dict: contributor_dict["roleName"] == role_name,
                    contributors,
                )
            )
            if len(contributors_with_role) > 0:
                contributor_name = contributors_with_role[0]["contributor"][0]["name"]
        return contributor_name

    def sample_registrant(self) -> typing.AnyStr:
        return self._contributor_name_with_role("Sample Registrant")

    def sample_sampling_purpose(self) -> typing.AnyStr:
        # TODO: implement
        return ""

    def produced_by_label(self) -> typing.AnyStr:
        return self._source_record_description()["collectionMethod"]

    def produced_by_description(self) -> typing.AnyStr:
        description_components = list()
        description_dict = self._source_record_description()
        if description_dict is not None:
            supplement_metadata = self._supplement_metadata()
            if supplement_metadata is not None:
                if "cruiseFieldPrgrm" in supplement_metadata:
                    description_components.append(
                        "cruiseFieldPrgrm:{0}".format(
                            supplement_metadata["cruiseFieldPrgrm"]
                        )
                    )
                if "launchPlatformName" in supplement_metadata:
                    description_components.append(
                        "launchPlatformName:{0}".format(
                            supplement_metadata["launchPlatformName"]
                        )
                    )

            if "collectionMethod" in description_dict:
                description_components.append(description_dict["collectionMethod"])
            if "description" in description_dict:
                description_components.append(description_dict["description"])

            if supplement_metadata is not None:
                launch_type_str = ""
                if "launchTypeName" in supplement_metadata:
                    launch_type_str += "launch type:{0}, ".format(
                        supplement_metadata["launchTypeName"]
                    )
                if "navigationType" in supplement_metadata:
                    launch_type_str += "navigation type:{0}".format(
                        supplement_metadata["navigationType"]
                    )
                if len(launch_type_str) > 0:
                    description_components.append(launch_type_str)

            return ". ".join(description_components)

        return Transformer.NOT_PROVIDED

    def produced_by_feature_of_interest(self) -> typing.AnyStr:
        supplement_metadata = self._supplement_metadata()
        if (
            supplement_metadata is not None
            and "primaryLocationType" in supplement_metadata
        ):
            return supplement_metadata["primaryLocationType"]
        return Transformer.NOT_PROVIDED

    def produced_by_responsibilities(self) -> typing.List:
        responsibilities = list()
        description_dict = self._source_record_description()
        collector = description_dict["collector"]
        if collector is not None:
            responsibilities.append("{},,Collector".format(collector))

        owner = self._contributor_name_with_role("Sample Owner")
        if len(owner) > 0:
            responsibilities.append("{},,Sample Owner".format(owner))

        return responsibilities

    def produced_by_result_time(self) -> typing.AnyStr:
        result_time = Transformer.NOT_PROVIDED
        description = self._source_record_description()
        if "collectionStartDate" in description:
            result_time = description["collectionStartDate"]
        elif "log" in description:
            # try reading it out of the log
            result_time = description["log"][0]["timestamp"]
        return result_time

    def sampling_site_description(self) -> typing.AnyStr:
        description_dict = self._source_record_description()
        if description_dict is not None:
            supplement_metadata = self._supplement_metadata()
            if (
                supplement_metadata is not None
                and "locationDescription" in supplement_metadata
            ):
                return supplement_metadata["locationDescription"]
        return Transformer.NOT_PROVIDED

    def sampling_site_label(self) -> typing.AnyStr:
        # TODO: implement
        return Transformer.NOT_PROVIDED

    def sampling_site_elevation(self) -> typing.AnyStr:
        supplement_metadata = self._supplement_metadata()
        if supplement_metadata is not None and "elevation" in supplement_metadata:
            elevation_value = supplement_metadata["elevation"]
            elevation_unit = supplement_metadata["elevationUnit"]
            elevation_unit_abbreviation = ""
            if elevation_unit is not None:
                if elevation_unit == "meters":
                    elevation_unit_abbreviation = "m"
                else:
                    self._logger().error(
                        "Received elevation in unexpected unit: ", elevation_unit
                    )
            elevation_str = str(elevation_value)
            if len(elevation_unit_abbreviation) > 0:
                elevation_str += " " + elevation_unit_abbreviation
            return elevation_str
        return Transformer.NOT_PROVIDED

    def _geo_location_float_value(self, key_name: typing.AnyStr):
        geo_location = self._source_record_description()["geoLocation"]
        if geo_location is not None:
            string_val = geo_location["geo"][0][key_name]
            if string_val is not None:
                return float(string_val)
        return 0.0

    def sampling_site_latitude(self) -> typing.SupportsFloat:
        return self._geo_location_float_value("latitude")

    def sampling_site_longitude(self) -> typing.SupportsFloat:
        return self._geo_location_float_value("longitude")

    def sampling_site_place_names(self) -> typing.List:
        place_names = list()
        supplement_metadata = self._supplement_metadata()
        if "primaryLocationName" in supplement_metadata:
            primary_location_name = supplement_metadata["primaryLocationName"]
            place_names.extend(primary_location_name.split("; "))
        if "province" in supplement_metadata:
            place_names.append(supplement_metadata["province"])
        if "county" in supplement_metadata:
            place_names.append(supplement_metadata["county"])
        if "city" in supplement_metadata:
            place_names.append(supplement_metadata["city"])
        return place_names

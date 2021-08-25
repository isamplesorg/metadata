import typing
import logging

from isamples_metadata.Transformer import (
    Transformer,
    AbstractCategoryMapper,
    StringPairedCategoryMapper,
    StringOrderedCategoryMapper,
    StringEqualityCategoryMapper,
    StringEndsWithCategoryMapper,
    AbstractCategoryMetaMapper,
)


class MaterialCategoryMetaMapper(AbstractCategoryMetaMapper):
    _endsWithRockMapper = StringEndsWithCategoryMapper("Rock", "Rock")
    _endsWithMineralMapper = StringEndsWithCategoryMapper("Mineral", "Mineral")
    _endsWithAqueousMapper = StringEndsWithCategoryMapper("aqueous", "Water")
    _endsWithSedimentMapper = StringEndsWithCategoryMapper("Sediment", "Sediment")
    _endsWithSoilMapper = StringEndsWithCategoryMapper("Soil", "Soil")
    _endsWithParticulateMapper = StringEndsWithCategoryMapper(
        "Particulate", "Particulate"
    )
    _endsWithBiologyMapper = StringEndsWithCategoryMapper("Biology", "Organic material")
    _endsWithSyntheticMapper = StringEndsWithCategoryMapper(
        "Synthetic", "Anthropogenic material"
    )
    _equalsRockMapper = StringEqualityCategoryMapper(
        [
            "Glass>Other",
            "Igneous>Other",
            "Igneous>Volcanic>Felsic>NotApplicable",
            "Igneous>Volcanic>Other",
            "Metamorphic>Other",
            "Sedimentary>Other",
            "Xenolithic>Other",
        ],
        "Rock",
    )
    _equalsSedimentMapper = StringEqualityCategoryMapper(["Tephra"], "Sediment")
    _equalsOrganicMaterialMapper = StringEqualityCategoryMapper(
        ["Siderite>Mineral", "Macrobiology>Other", "Organic Material"],
        "Organic material",
    )
    _equalsNonAqueousLiquidMaterialMapper = StringEqualityCategoryMapper(
        ["Liquid>organic"], "Non-aqueous liquid material"
    )
    _equalsMineralMapper = StringEqualityCategoryMapper(
        [
            "Ore>Other",
            "FeldsparGroup>Other",
            "Epidote>Other",
            "Enstatite>Other",
            "Betpakdalite>Other",
            "Aurichalcite>Other",
            "Augite>Other",
            "Aragonite>Biology",
            "AmphiboleGroup>Other",
            "Actinolite>Other",
        ],
        "Mineral",
    )
    _equalsIceMapper = StringEqualityCategoryMapper(["Ice"], "Ice")
    _equalsGasMapper = StringEqualityCategoryMapper(["Gas"], "Gaseous material")
    _equalsBiogenicMapper = StringEqualityCategoryMapper(
        ["Macrobiology>Coral>Biology", "Coral>Biology"], "Biogenic non-organic material"
    )

    @classmethod
    def categories_mappers(cls) -> typing.List[AbstractCategoryMapper]:
        return [
            cls._endsWithRockMapper,
            cls._endsWithMineralMapper,
            cls._endsWithAqueousMapper,
            cls._endsWithSedimentMapper,
            cls._endsWithSoilMapper,
            cls._endsWithParticulateMapper,
            cls._endsWithBiologyMapper,
            cls._endsWithSyntheticMapper,
            cls._equalsRockMapper,
            cls._equalsSedimentMapper,
            cls._equalsIceMapper,
            cls._equalsOrganicMaterialMapper,
            cls._equalsNonAqueousLiquidMaterialMapper,
            cls._equalsMineralMapper,
            cls._equalsIceMapper,
            cls._equalsGasMapper,
            cls._equalsBiogenicMapper,
        ]


class SpecimenCategoryMetaMapper(AbstractCategoryMetaMapper):
    _otherSolidObjectsMapper = StringEqualityCategoryMapper(
        [
            "Core",
            "Core Half Round",
            "Core Piece",
            "Core Quarter Round",
            "Core Section",
            "Core Section Half",
            "Core Sub-Piece",
            "Core Whole Round",
            "Grab",
            "Individual Sample",
            "Individual Sample>Cube",
            "Individual Sample>Cylinder",
            "Individual Sample>Slab",
            "Individual Sample>Specimen",
            "Oriented Core",
        ],
        "Other solid object",
    )
    _containersWithFluidMapper = StringEqualityCategoryMapper(
        [
            "CTD",
            "Individual Sample>Gas",
            "Individual Sample>Liquid",
        ],
        "Liquid or gas sample",
    )
    _experimentalProductsMapper = StringEqualityCategoryMapper(
        ["Experimental Specimen"], "Experiment product"
    )
    _biomeAggregationsMapper = StringEqualityCategoryMapper(
        ["Trawl"], "Biome aggregation"
    )
    _analyticalPreparationsMapper = StringEqualityCategoryMapper(
        [
            "Individual Sample>Bead",
            "Individual Sample>Chemical Fraction",
            "Individual Sample>Culture",
            "Individual Sample>Mechanical Fraction",
            "Individual Sample>Powder",
            "Individual Sample>Smear",
            "Individual Sample>Thin Section",
            "Individual Sample>Toothpick",
            "Individual Sample>U-Channel",
            "Rock Powder",
        ],
        "Analytical preparation",
    )
    _aggregationsMapper = StringEqualityCategoryMapper(
        ["Cuttings", "Dredge"], "Aggregation"
    )

    @classmethod
    def categories_mappers(cls) -> typing.List[AbstractCategoryMapper]:
        return [
            cls._otherSolidObjectsMapper,
            cls._containersWithFluidMapper,
            cls._experimentalProductsMapper,
            cls._biomeAggregationsMapper,
            cls._analyticalPreparationsMapper,
            cls._aggregationsMapper,
        ]


class ContextCategoryMetaMapper(AbstractCategoryMetaMapper):
    _endsWithRockMapper = StringEndsWithCategoryMapper("Rock", "Earth interior")
    _endsWithMineralMapper = StringEndsWithCategoryMapper("Mineral", "Earth interior")
    _equalsGasMapper = StringEqualityCategoryMapper(
        ["Gas"], "Subsurface fluid reservoir"
    )
    # This one is actually incorrect as written, we need to use the combo of material and primaryLocationType
    _endsWithSoilMapper = StringEndsWithCategoryMapper(
        "Soil", "Subaerial surface environment"
    )
    _soilFloodplainMapper = StringPairedCategoryMapper(
        "Microbiology>Soil", "floodplain", "Subaerial terrestrial biome"
    )
    _soilMapper = StringOrderedCategoryMapper(
        # Order matters here, the generic one needs to be last
        [_soilFloodplainMapper, _endsWithSoilMapper]
    )
    _seaSedimentMapper = StringPairedCategoryMapper(
        "Sediment", "sea", "Marine water body bottom"
    )
    _lakeSedimentMapper = StringPairedCategoryMapper(
        "Sediment", "lake", "Lake, river or stream bottom"
    )
    _sedimentMapper = StringOrderedCategoryMapper(
        [_seaSedimentMapper, _lakeSedimentMapper]
    )
    _lakeMapper = StringPairedCategoryMapper("", "lake", "Terrestrial water body")
    _mountainLiquidMapper = StringPairedCategoryMapper(
        "Liquid>aqueous", "Mountain", "Terrestrial water body"
    )
    _seaMapper = StringPairedCategoryMapper(
        "Liquid>aqueous", "Sea", "Marine water body"
    )
    _ventBiologyMapper = StringPairedCategoryMapper("Biology", "Vent", "Marine biome")
    _ventLiquidMapper = StringPairedCategoryMapper(
        "Liquid>aqueous", "Vent", "Subsurface fluid reservoir"
    )
    _floodplainAquiferMapper = StringPairedCategoryMapper(
        "Liquid>aqueous", "floodplain\, aquifer", "Subsurface fluid reservoir"
    )
    _creekBankMapper = StringPairedCategoryMapper(
        "Sedimentary>GlacialAndOrPaleosol>Rock",
        "Creek bank",
        "Subaerial surface environment",
    )
    # Note that this represents the combos down to row 109 of
    # https://docs.google.com/spreadsheets/d/1QitBRkWH6YySZnNO-uR7D2rTaQ826WPT_xow9lPdJDM/edit#gid=1251732948
    # Need to continue on from there…

    @classmethod
    def categories_mappers(cls) -> typing.List[AbstractCategoryMapper]:
        return [
            cls._endsWithRockMapper,
            cls._endsWithMineralMapper,
            cls._equalsGasMapper,
            cls._soilMapper,
            cls._sedimentMapper,
            cls._lakeMapper,
            cls._mountainLiquidMapper,
            cls._seaMapper,
            cls._ventBiologyMapper,
            cls._ventLiquidMapper,
            cls._floodplainAquiferMapper,
            cls._creekBankMapper,
        ]


class SESARTransformer(Transformer):
    """Concrete transformer class for going from a SESAR record to an iSamples record"""

    def _source_record_description(self) -> typing.Dict:
        return self.source_record["description"]

    def _supplement_metadata(self) -> typing.Dict:
        description = self._source_record_description()
        if description is not None:
            return self._source_record_description()["supplementMetadata"]
        return {}

    def _primary_location_type(self) -> typing.Optional[typing.AnyStr]:
        supplement_metadata = self._supplement_metadata()
        if (
            supplement_metadata is not None
            and "primaryLocationType" in supplement_metadata
        ):
            return supplement_metadata["primaryLocationType"]
        return None

    def _material_type(self) -> typing.AnyStr:
        return self._source_record_description().get("material", None)

    @staticmethod
    def _logger():
        return logging.getLogger("isamples_metadata.SESARTransformer")

    def id_string(self):
        return "https://data.isamples.org/digitalsample/{0}/{1}".format(
            self.sample_identifier_scheme(), self.sample_identifier_value()
        )

    def sample_identifier_string(self) -> typing.AnyStr:
        return f"{self.sample_identifier_scheme().upper()}:{self.sample_identifier_value()}"

    def sample_identifier_scheme(self) -> typing.AnyStr:
        return "igsn"

    def sample_identifier_value(self) -> typing.AnyStr:
        return self.source_record["igsn"]

    def sample_label(self) -> typing.AnyStr:
        return self._source_record_description()["sampleName"]

    def sample_description(self) -> typing.AnyStr:
        # TODO: implement
        return Transformer.NOT_PROVIDED

    def has_context_categories(self) -> typing.List[typing.AnyStr]:
        material_type = self._material_type()
        primary_location_type = self._primary_location_type()
        return ContextCategoryMetaMapper.categories(
            material_type, primary_location_type
        )

    def has_material_categories(self) -> typing.List[typing.AnyStr]:
        material = self._material_type()
        return MaterialCategoryMetaMapper.categories(material)

    def has_specimen_categories(self) -> typing.List[typing.AnyStr]:
        sample_type = self._source_record_description()["sampleType"]
        return SpecimenCategoryMetaMapper.categories(sample_type)

    def keywords(self) -> typing.List:
        # TODO: implement
        return [self._source_record_description()["sampleType"]]

    def produced_by_id_string(self) -> typing.AnyStr:
        # TODO: this is present for GEOME, does anything make sense for SESAR?
        return ""

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
        if "collectionMethod" in self._source_record_description():
            return self._source_record_description()["collectionMethod"]
        else:
            return Transformer.NOT_PROVIDED

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
        primary_location_type = self._primary_location_type()
        if primary_location_type is not None:
            return primary_location_type
        return Transformer.NOT_PROVIDED

    def produced_by_responsibilities(self) -> typing.List[typing.AnyStr]:
        responsibilities = list()
        description_dict = self._source_record_description()
        if "collector" in description_dict:
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

    def elevation_str(
        self, elevation_value: typing.AnyStr, elevation_unit: typing.AnyStr
    ) -> typing.AnyStr:
        elevation_unit_abbreviation = ""
        if elevation_unit is not None:
            elevation_unit = elevation_unit.lower().strip()
            if elevation_unit == "feet":
                # target elevation for core metadata will always be meters, so convert here
                elevation_value = elevation_value / Transformer.FEET_PER_METER
                elevation_unit_abbreviation = "m"
            elif elevation_unit == "meters":
                elevation_unit_abbreviation = "m"
            else:
                self._logger().error(
                    "Received elevation in unexpected unit: ", elevation_unit
                )
        elevation_str = str(elevation_value)
        if len(elevation_unit_abbreviation) > 0:
            elevation_str += " " + elevation_unit_abbreviation
        return elevation_str

    def sampling_site_elevation(self) -> typing.AnyStr:
        supplement_metadata = self._supplement_metadata()
        if supplement_metadata is not None and "elevation" in supplement_metadata:
            elevation_value = supplement_metadata["elevation"]
            elevation_unit = supplement_metadata.get("elevationUnit", "meters")
            return self.elevation_str(elevation_value, elevation_unit)
        return Transformer.NOT_PROVIDED

    def _geo_location_float_value(self, key_name: typing.AnyStr) -> typing.Optional[typing.SupportsFloat]:
        if "geoLocation" in self._source_record_description():
            geo_location = self._source_record_description()["geoLocation"]
            if geo_location is not None:
                first_geo = geo_location["geo"][0]
                # Ignore things that aren't lat/long for now, e.g.
                # https://github.com/isamplesorg/metadata/issues/20
                if key_name in first_geo:
                    string_val = first_geo[key_name]
                    if string_val is not None:
                        return float(string_val)
        return None

    def sampling_site_latitude(self) -> typing.Optional[typing.SupportsFloat]:
        return self._geo_location_float_value("latitude")

    def sampling_site_longitude(self) -> typing.Optional[typing.SupportsFloat]:
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

    def informal_classification(self) -> typing.List[typing.AnyStr]:
         """Not currently used for SESAR"""
         return Transformer.NOT_PROVIDED

    def last_updated_time(self) -> typing.Optional[typing.AnyStr]:
        # Loop through the log and find the "lastUpdated" record
        description = self._source_record_description()
        log = description.get("log")
        if log is not None:
            for record in log:
                if "lastUpdated" == record.get("type"):
                    return record["timestamp"]
        return None

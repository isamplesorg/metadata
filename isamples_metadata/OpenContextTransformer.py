import typing

from isamples_metadata.Transformer import (
    Transformer,
    AbstractCategoryMetaMapper,
    StringEqualityCategoryMapper,
    AbstractCategoryMapper,
)


class MaterialCategoryMetaMapper(AbstractCategoryMetaMapper):
    _anthropogenicMaterialMapper = StringEqualityCategoryMapper(
        [
            "Architectural Element",
            "Bulk Ceramic",
            "Glass",
            "Object",
            "Pottery",
            "Sample",
            "Sample, Collection, or Aggregation",
            "Sculpture",
            "Stela",
        ],
        "Anthropogenic material",
    )

    _anthropogenicMetalMapper = StringEqualityCategoryMapper(
        [
            "Coin",
        ],
        "Anthropogenic metal",
    )

    _biogenicMapper = StringEqualityCategoryMapper(
        ["Animal Bone", "Human Bone", "Non Diagnostic Bone", "Shell"],
        "Biogenic non organic material",
    )

    _organicMapper = StringEqualityCategoryMapper(
        [
            "Biological subject, Ecofact",
            "Plant remains",
        ],
        "Organic material",
    )

    _rockMapper = StringEqualityCategoryMapper(["Groundstone"], "Rock")

    @classmethod
    def categories_mappers(cls) -> typing.List[AbstractCategoryMapper]:
        return [
            cls._anthropogenicMaterialMapper,
            cls._anthropogenicMetalMapper,
            cls._biogenicMapper,
            cls._organicMapper,
            cls._rockMapper,
        ]


class SpecimenCategoryMetaMapper(AbstractCategoryMetaMapper):
    _organismPartMapper = StringEqualityCategoryMapper(
        [
            "Animal Bone",
            "Human Bone",
            "Non Diagnostic Bone",
        ],
        "Organism part",
    )
    _anthropogenicAggregationMapper = StringEqualityCategoryMapper(
        ["Architectural Element", "Basket", "Bulk Ceramic", "Lot"],
        "Anthropogenic aggregation",
    )
    _biomeAggregationMapper = StringEqualityCategoryMapper(
        ["Biological subject, Ecofact", "Plant remains"], "Biome aggregation"
    )
    _artifactMapper = StringEqualityCategoryMapper(
        ["Coin", "Glass", "Groundstone", "Object", "Pottery", "Sculpture", "Stela"],
        "Artifact",
    )
    _otherSolidObjectMapper = StringEqualityCategoryMapper(
        ["Sample", "Sample, Collection, or Aggregation"], "Other solid object"
    )
    _organismProductMapper = StringEqualityCategoryMapper(
        [
            "Shell",
        ],
        "Organism product",
    )

    @classmethod
    def categories_mappers(cls) -> typing.List[AbstractCategoryMapper]:
        return [
            cls._organismPartMapper,
            cls._anthropogenicAggregationMapper,
            cls._biomeAggregationMapper,
            cls._artifactMapper,
            cls._otherSolidObjectMapper,
            cls._organismProductMapper,
        ]


class OpenContextTransformer(Transformer):

    def _citation_uri(self) -> typing.AnyStr:
        return self.source_record.get("citation uri")

    def id_string(self) -> typing.AnyStr:
        citation_uri = self._citation_uri()
        return f"metadata/{citation_uri.removeprefix(Transformer.N2T_ARK_PREFIX)}"

    def sample_identifier_string(self) -> typing.AnyStr:
        return self._citation_uri().removeprefix(Transformer.N2T_PREFIX)

    def sample_label(self) -> typing.AnyStr:
        return self.source_record.get("label", Transformer.NOT_PROVIDED)

    def sample_description(self) -> typing.AnyStr:
        description_pieces = []
        self._transform_key_to_label(
            "early bce/ce", self.source_record, description_pieces
        )
        self._transform_key_to_label(
            "late bce/ce", self.source_record, description_pieces
        )
        self._transform_key_to_label("updated", self.source_record, description_pieces)
        for consists_of_dict in self.source_record.get("Consists of", []):
            self._transform_key_to_label(
                "label", consists_of_dict, description_pieces, "Consists of"
            )
        for has_type_dict in self.source_record.get("Has type", []):
            self._transform_key_to_label(
                "label", has_type_dict, description_pieces, "Has type"
            )
        for has_anatomical_dict in self.source_record.get(
            "Has anatomical identification", []
        ):
            self._transform_key_to_label(
                "label",
                has_anatomical_dict,
                description_pieces,
                "Has anatomical identification",
            )
        for temporal_coverage_dict in self.source_record.get("Temporal Coverage", []):
            self._transform_key_to_label(
                "label",
                temporal_coverage_dict,
                description_pieces,
                "Temporal coverage",
            )
        return Transformer.DESCRIPTION_SEPARATOR.join(description_pieces)

    def sample_registrant(self) -> typing.AnyStr:
        pass

    def sample_sampling_purpose(self) -> typing.AnyStr:
        pass

    def has_context_categories(self) -> typing.List[typing.AnyStr]:
        return ["Site of past human activities"]

    def has_material_categories(self) -> typing.List[typing.AnyStr]:
        item_category = self.source_record.get("item category")
        return MaterialCategoryMetaMapper.categories(item_category)

    def has_specimen_categories(self) -> typing.List[typing.AnyStr]:
        item_category = self.source_record.get("item category")
        return SpecimenCategoryMetaMapper.categories(item_category)

    def _context_label_pieces(self) -> typing.List[typing.AnyStr]:
        context_label = self.source_record.get("context label")
        if len(context_label) > 0:
            return context_label.split("/")
        else:
            return []

    def keywords(self) -> typing.List[typing.AnyStr]:
        return self._context_label_pieces()

    def produced_by_id_string(self) -> typing.AnyStr:
        return Transformer.NOT_PROVIDED

    def produced_by_label(self) -> typing.AnyStr:
        return self.source_record.get("project label", Transformer.NOT_PROVIDED)

    def produced_by_description(self) -> typing.AnyStr:
        return self.source_record.get("project uri", Transformer.NOT_PROVIDED)

    def produced_by_feature_of_interest(self) -> typing.AnyStr:
        return Transformer.NOT_PROVIDED

    def produced_by_responsibilities(self) -> typing.List[typing.AnyStr]:
        # from ekansa:
        # "Creator" is typically a project PI (Principle Investigator). They may or may not be the person that
        # collected the sample. If given, a "Contributor" is the person that originally collected or first
        # described the specimen.
        responsibilities = []
        creators = self.source_record.get("Creator")
        if creators is not None:
            for creator in creators:
                responsibilities.append(f"creator: {creator.get('label')}")
        contributors = self.source_record.get("Contributor")
        if contributors is not None:
            for contributor in contributors:
                responsibilities.append(f"collector: {contributor.get('label')}")
        return responsibilities

    def produced_by_result_time(self) -> typing.AnyStr:
        return self.source_record.get("published", Transformer.NOT_PROVIDED)

    def sampling_site_description(self) -> typing.AnyStr:
        return Transformer.NOT_PROVIDED

    def sampling_site_label(self) -> typing.AnyStr:
        return self.source_record.get("context label", Transformer.NOT_PROVIDED)

    def sampling_site_elevation(self) -> typing.AnyStr:
        Transformer.NOT_PROVIDED

    def sampling_site_latitude(self) -> typing.Optional[typing.SupportsFloat]:
        return self.source_record.get("latitude", None)

    def sampling_site_longitude(self) -> typing.Optional[typing.SupportsFloat]:
        return self.source_record.get("longitude", None)

    def sampling_site_place_names(self) -> typing.List:
        return self._context_label_pieces()

    def informal_classification(self) -> typing.List[typing.AnyStr]:
        classifications = []
        for consists_of_dict in self.source_record.get("Has taxonomic identifier", []):
            classifications.append(consists_of_dict.get("label"))
        return classifications

    def last_updated_time(self) -> typing.Optional[typing.AnyStr]:
        return self.source_record.get("updated", None)
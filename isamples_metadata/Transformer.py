from abc import ABC, abstractmethod
import typing


class Transformer(ABC):
    """Abstract base class for various iSamples provider transformers"""

    NOT_PROVIDED = "Not Provided"

    FEET_PER_METER = 3.28084

    DESCRIPTION_SEPARATOR = " | "

    N2T_PREFIX = "https://n2t.net/"

    N2T_ARK_PREFIX = f"{N2T_PREFIX}ark:/"

    N2T_NO_HTTPS_PREFIX = "http://n2t.net/"

    N2T_ARK_NO_HTTPS_PREFIX = f"{N2T_NO_HTTPS_PREFIX}ark:/"

    @staticmethod
    def _transform_key_to_label(
        key: typing.AnyStr,
        source_dict: typing.Dict,
        dest_list: typing.List[typing.AnyStr],
        label: typing.AnyStr = None,
    ):
        if label is None:
            label = key
        value = source_dict.get(key)
        if value is not None and len(str(value)) > 0:
            dest_list.append(f"{label}: {value}")

    @staticmethod
    def _formatted_date(
        year: typing.AnyStr, month: typing.AnyStr, day: typing.AnyStr
    ) -> typing.AnyStr:
        result_time_pieces = []
        if year is not None and len(year) > 0:
            result_time_pieces.append(year)
        if month is not None and len(month) > 0:
            result_time_pieces.append(month.zfill(2))
        if day is not None and len(day) > 0:
            result_time_pieces.append(day.zfill(2))
        return "-".join(result_time_pieces)

    def __init__(self, source_record: typing.Dict):
        self.source_record = source_record

    def transform(self) -> typing.Dict:
        """Do the actual work of transforming a provider record into an iSamples record.

        Arguments:
            source_record -- The provider record to be transformed
        Return value:
            The provider record transformed into an iSamples record
        """
        transformed_record = {
            "$schema": "../../iSamplesSchemaBasic0.2.json",
            "@id": self.id_string(),
            "label": self.sample_label(),
            "sampleidentifier": self.sample_identifier_string(),
            "description": self.sample_description(),
            "hasContextCategory": self.has_context_categories(),
            "hasMaterialCategory": self.has_material_categories(),
            "hasSpecimenCategory": self.has_specimen_categories(),
            "informalClassification": self.informal_classification(),
            "keywords": self.keywords(),
            "producedBy": {
                "@id": self.produced_by_id_string(),
                "label": self.produced_by_label(),
                "description": self.produced_by_description(),
                "hasFeatureOfInterest": self.produced_by_feature_of_interest(),
                "responsibility": self.produced_by_responsibilities(),
                "resultTime": self.produced_by_result_time(),
                "samplingSite": {
                    "description": self.sampling_site_description(),
                    "label": self.sampling_site_label(),
                    "location": {
                        "elevation": self.sampling_site_elevation(),
                        "latitude": self.sampling_site_latitude(),
                        "longitude": self.sampling_site_longitude(),
                    },
                    "placeName": self.sampling_site_place_names(),
                },
            },
            "registrant": self.sample_registrant(),
            "samplingPurpose": self.sample_sampling_purpose(),
            "curation": {
                "label": self.curation_label(),
                "description": self.curation_description(),
                "accessConstraints": self.curation_access_constraints(),
                "curationLocation": self.curation_location(),
                "responsibility": self.curation_responsibility(),
            },
            "relatedResource": self.related_resources(),
        }
        return transformed_record

    @abstractmethod
    def id_string(self) -> typing.AnyStr:
        """The value for the @id key in the iSamples record"""
        pass

    @abstractmethod
    def sample_identifier_string(self) -> typing.AnyStr:
        pass

    @abstractmethod
    def sample_label(self) -> typing.AnyStr:
        """A label for the sample in source_record"""
        pass

    @abstractmethod
    def sample_description(self) -> typing.AnyStr:
        """A textual description of the sample in source_record"""
        pass

    @abstractmethod
    def sample_registrant(self) -> typing.AnyStr:
        """The name of the sample registrant in source_record"""
        pass

    @abstractmethod
    def sample_sampling_purpose(self) -> typing.AnyStr:
        """The samplingPurpose of the sample registrant in source_record"""
        pass

    @abstractmethod
    def has_context_categories(self) -> typing.List[typing.AnyStr]:
        """Map from the source record into an iSamples context category"""
        pass

    @abstractmethod
    def has_material_categories(self) -> typing.List[typing.AnyStr]:
        """Map from the source record into an iSamples material category"""
        pass

    @abstractmethod
    def has_specimen_categories(self) -> typing.List[typing.AnyStr]:
        """Map from the source record into an iSamples specimen category"""
        pass

    @abstractmethod
    def informal_classification(self) -> typing.List[typing.AnyStr]:
        """An informal scientificName"""
        pass

    @abstractmethod
    def keywords(self) -> typing.List[typing.AnyStr]:
        """The keywords for the sample in source record"""
        pass

    @abstractmethod
    def produced_by_id_string(self) -> typing.AnyStr:
        """The id for the producedBy dictionary, likely used for parent identifiers"""
        pass

    @abstractmethod
    def produced_by_label(self) -> typing.AnyStr:
        """The label for the producedBy dictionary"""
        pass

    @abstractmethod
    def produced_by_description(self) -> typing.AnyStr:
        """The description for the producedBy dictionary"""
        pass

    @abstractmethod
    def produced_by_feature_of_interest(self) -> typing.AnyStr:
        """The feature of interest for the producedBy dictionary"""
        pass

    @abstractmethod
    def produced_by_responsibilities(self) -> typing.List[typing.AnyStr]:
        """The responsibility list for the producedBy dictionary"""
        pass

    @abstractmethod
    def produced_by_result_time(self) -> typing.AnyStr:
        """The result time for the producedBy dictionary"""
        pass

    @abstractmethod
    def sampling_site_description(self) -> typing.AnyStr:
        """The sampling site description"""
        pass

    @abstractmethod
    def sampling_site_label(self) -> typing.AnyStr:
        """The sampling site label"""
        pass

    @abstractmethod
    def sampling_site_elevation(self) -> typing.AnyStr:
        """The sampling site elevation"""
        pass

    @abstractmethod
    def sampling_site_latitude(self) -> typing.Optional[typing.SupportsFloat]:
        """The sampling site latitude"""
        pass

    @abstractmethod
    def sampling_site_longitude(self) -> typing.Optional[typing.SupportsFloat]:
        """The sampling site longitude"""
        pass

    @abstractmethod
    def sampling_site_place_names(self) -> typing.List:
        """The sampling site longitude"""
        pass

    # region Curation information

    # For the curation fields, not all of the collections have them, so provide stubs returning the empty sentinel
    def curation_label(self) -> typing.AnyStr:
        return Transformer.NOT_PROVIDED

    def curation_description(self) -> typing.AnyStr:
        return Transformer.NOT_PROVIDED

    def curation_access_constraints(self) -> typing.AnyStr:
        return Transformer.NOT_PROVIDED

    def curation_location(self) -> typing.AnyStr:
        return Transformer.NOT_PROVIDED

    def curation_responsibility(self) -> typing.AnyStr:
        return Transformer.NOT_PROVIDED

    # endregion

    def related_resources(self) -> typing.List[typing.Dict]:
        return []

    @abstractmethod
    def last_updated_time(self) -> typing.Optional[typing.AnyStr]:
        """Return the time the record was last modified in the source collection"""
        pass


class AbstractCategoryMapper(ABC):
    _destination: typing.AnyStr

    @abstractmethod
    def matches(
        self,
        potential_match: typing.AnyStr,
        auxiliary_match: typing.Optional[typing.AnyStr] = None,
    ) -> bool:
        """Whether a particular String input matches this category mapper"""
        pass

    def append_if_matched(
        self,
        potential_match: typing.AnyStr,
        auxiliary_match: typing.Optional[typing.AnyStr] = None,
        categories_list: typing.List[typing.AnyStr] = (),
    ):
        if self.matches(potential_match, auxiliary_match):
            categories_list.append(self._destination)

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, destination):
        self._destination = destination


class AbstractCategoryMetaMapper(ABC):
    _categoriesMappers = []

    @classmethod
    def categories(
        cls,
        source_category: typing.AnyStr,
        auxiliary_source_category: typing.Optional[typing.AnyStr] = None,
    ):
        categories = []
        if source_category is not None:
            for mapper in cls._categoriesMappers:
                mapper.append_if_matched(
                    source_category, auxiliary_source_category, categories
                )
        if len(categories) == 0:
            categories.append(Transformer.NOT_PROVIDED)
        return categories

    @classmethod
    def categories_mappers(cls) -> typing.List[AbstractCategoryMapper]:
        return []

    def __init_subclass__(cls, **kwargs):
        cls._categoriesMappers = cls.categories_mappers()


class StringConstantCategoryMapper(AbstractCategoryMapper):
    """A mapper that always matches.  Use this as the end of the road."""

    def __init__(
        self,
        destination_category: typing.AnyStr,
    ):
        self._destination = destination_category

    def matches(
        self,
        potential_match: typing.AnyStr,
        auxiliary_match: typing.Optional[typing.AnyStr] = None,
    ) -> bool:
        return True


class StringEqualityCategoryMapper(AbstractCategoryMapper):
    """A mapper that matches iff the potentialMatch exactly matches one of the list of predefined categories"""

    def __init__(
        self,
        categories: typing.List[typing.AnyStr],
        destination_category: typing.AnyStr,
    ):
        categories = [keyword.lower() for keyword in categories]
        categories = [keyword.strip() for keyword in categories]
        self._categories = categories
        self._destination = destination_category

    def matches(
        self,
        potential_match: typing.AnyStr,
        auxiliary_match: typing.Optional[typing.AnyStr] = None,
    ) -> bool:
        return potential_match.lower().strip() in self._categories


class StringEndsWithCategoryMapper(AbstractCategoryMapper):
    """A mapper that matches if the potentialMatch ends with the specified string"""

    def __init__(self, ends_with: typing.AnyStr, destination_category: typing.AnyStr):
        self._endsWith = ends_with.lower().strip()
        self._destination = destination_category

    def matches(
        self,
        potential_match: typing.AnyStr,
        auxiliary_match: typing.Optional[typing.AnyStr] = None,
    ) -> bool:
        return potential_match.lower().strip().endswith(self._endsWith)


class StringOrderedCategoryMapper(AbstractCategoryMapper):
    """A mapper that runs through a list of mappers and chooses the first one that matches"""

    def __init__(self, submappers: typing.List[AbstractCategoryMapper]):
        self._submappers = submappers

    def matches(
        self,
        potential_match: typing.AnyStr,
        auxiliary_match: typing.Optional[typing.AnyStr] = None,
    ) -> bool:
        for mapper in self._submappers:
            if mapper.matches(potential_match, auxiliary_match):
                # Note that this isn't thread-safe -- we expect one of these objects per thread
                self.destination = mapper.destination
                return True
        return False


class StringPairedCategoryMapper(AbstractCategoryMapper):
    """A mapper that matches iff the potentialMatch matches both the primaryMatch and secondaryMatch"""

    def __init__(
        self,
        primary_match: typing.AnyStr,
        auxiliary_match: typing.AnyStr,
        destination_category: typing.AnyStr,
    ):
        self._primaryMatch = primary_match.lower().strip()
        self._auxiliaryMatch = auxiliary_match.lower().strip()
        self._destination = destination_category

    def matches(
        self,
        potential_match: typing.AnyStr,
        auxiliary_match: typing.Optional[typing.AnyStr] = None,
    ) -> bool:
        return (
            potential_match is not None
            and auxiliary_match is not None
            and potential_match.lower().strip() == self._primaryMatch
            and auxiliary_match.lower().strip() == self._auxiliaryMatch
        )

from abc import ABC, abstractmethod
import typing
from enum import Enum, auto


class _ControlledVocabularyCategory(Enum):
    """Enum subclass for controlled vocbularies -- __repr__ overridden to print the quoted value"""

    def __repr__(self):
        return "'%s'" % (self.value)


class ContextCategory(_ControlledVocabularyCategory):
    """Top level context, based on the kind of feature sampled, from the SampledFeature vocabulary.  Specific identification of the sampled feature of interest is done through the SamplingEvent/Feature of Interest property."""

    ATMOSPHERE = "Atmosphere"
    BIOLOGICAL_ENVIRONMENT = "Biological environment"
    BUILDING = "Building"
    EARTH_ENVIRONMENT = ("Earth environment",)
    EARTH_SURFACE = ("Earth Surface",)
    EXPERIMENT_SETTING = ("Experiment setting",)
    EXTRATERRESTRIAL_ENVIRONMENT = ("Extraterrestrial environment",)
    HUMAN_OCCUPATION_SITE = ("Human occupation site",)
    LAB_ENVIRONMENT = ("Lab environment",)
    LABORATORY_ENVIRONMENT = ("Laboratory environment",)
    LAKE_RIVER_STREAM_BED = ("Lake, River, or Stream bed",)
    MARINE_BIOME = ("Marine biome",)
    MARINE_ENVIRONMENT = ("Marine environment",)
    MARINE_WATER_BODY_BOTTOM = ("Marine water body bottom",)
    REGOLITH_SEDIMENT_SOIL_HORIZON = ("Regolith, sediment or soil horizon",)
    ROCK_BODY = ("Rock Body",)
    ROCK_SAMPLE = ("Rock sample",)
    SOLID_EARTH = ("Solid Earth",)
    SUBAERIAL_SURFACE_ENVIRONMENT = ("Subaerial Surface Environment",)
    SUBAERIAL_TERRESTRIAL_ENVIRONMENT = ("Subaerial terrestrial environment",)
    SUBAQUEOUS_TERRESTRIAL_ENVIRONMENT = ("Subaqueous terrestrial environment",)
    SUBSURFACE_FLUID_RESERVOIR = ("Subsurface fluid reservoir",)
    TERRESTRIAL_WATER_BODY = ("Terrestrial water body",)
    WATER_BODY = "Water body"


class MaterialCategory(_ControlledVocabularyCategory):
    """The kind of material that constitutes the sample"""

    ANTHROPOGENIC_MATERIAL = ("Anthropogenic material",)
    ANTHROPOGENIC_METAL_MATERIAL = ("Anthropogenic metal material",)
    BIOGENIC_NON_ORGANIC_MATERIAL = ("Biogenic non-organic material",)
    DISPERSED_MEDIA = ("Dispersed media",)
    FLUID_MATERIAL = ("Fluid material",)
    GASEOUS_MATERIAL = ("Gaseous material",)
    LIQUID_WATER = ("Liquid water",)
    MINERAL = ("Mineral",)
    MIXED_SOIL_SEDIMENT_ROCK = ("Mixed soil, sediment or rock",)
    NATURAL_SOLID_MATERIAL = ("Natural Solid Material",)
    NON_AQUEOUS_LIQUID_MATERIAL = ("Non-aqueous liquid material",)
    ORGANIC_MATERIAL = ("Organic material",)
    OTHER_ANTHROPOGENIC_MATERIAL = ("Other anthropogenic material",)
    PATRICULATE = ("Particulate",)
    ROCK = ("Rock",)
    SEDIMENT = ("Sediment",)
    SOIL = "Soil"


class SpecimenCategory(_ControlledVocabularyCategory):
    """The kind of object that the specimen is"""

    AGGREGATION = ("Aggregation",)
    ANTHROPOGENIC_AGGREGATION = ("Anthropogenic aggregation",)
    ANY_AGGREGATION_SPECIMEN = ("Any aggregation specimen",)
    ANY_BIOLOGICAL_SPECIMEN = ("Any biological specimen",)
    ANY_SOLID_OBJECT = ("Any solid object",)
    ARTIFACT = ("Artifact",)
    BIOME_AGGREGATION_SPECIMEN = ("Biome aggregation specimen",)
    CONTAINER_WITH_FLUID = ("Container with fluid",)
    FOSSIL = ("Fossil",)
    ORGANISM_PART = ("Organism part",)
    ORGANISM_PRODUCT = ("Organism product",)
    OTHER_SOLID_OBJECT = ("Other solid object",)
    RESEARCH_PRODUCT = ("Research product",)
    WHOLE_ORGANISM_SPECIMEN = "Whole organism specimen"


class Transformer(ABC):
    """Abstract base class for various iSamples provider transformers"""

    NOT_PROVIDED = "Not Provided"

    def __init__(self, source_record: typing.Dict):
        self.source_record = source_record

    @abstractmethod
    def transform(self) -> typing.Dict:
        """Do the actual work of transforming a provider record into an iSamples record.

        Arguments:
            source_record -- The provider record to be transformed
        Return value:
            The provider record transformed into an iSamples record
        """
        transformed_record = {
            "$schema": "../iSamplesSchemaBasicSMR.json",
            "@id": "https://data.isamples.org/digitalsample/{0}/{1}".format(
                self.sample_identifier_scheme(), self.sample_identifier_value()
            ),
            "label": self.sample_label(),
            "sampleidentifier": "{0}:{1}".format(
                self.sample_identifier_scheme(), self.sample_identifier_value()
            ),
            "description": self.sample_description(),
            "hasContextCategory": self.has_context_categories(),
            "hasMaterialCategory": self.has_material_categories(),
            "hasSpecimenCategory": self.has_specimen_categories(),
            "keywords": self.keywords(),
            "producedBy": {
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
        }
        return transformed_record

    @abstractmethod
    def sample_identifier_scheme(self) -> typing.AnyStr:
        """The identifier scheme for the sample in source_record"""
        pass

    @abstractmethod
    def sample_identifier_value(self) -> typing.AnyStr:
        """An identifier value for the sample in source_record, this doesn't include the identifier scheme"""
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
    def has_context_categories(self) -> typing.List[ContextCategory]:
        """Map from the source record into an iSamples context category"""
        pass

    @abstractmethod
    def has_material_categories(self) -> typing.List[MaterialCategory]:
        """Map from the source record into an iSamples material category"""
        pass

    @abstractmethod
    def has_specimen_categories(self) -> typing.List[SpecimenCategory]:
        """Map from the source record into an iSamples specimen category"""
        pass

    @abstractmethod
    def keywords(self) -> typing.List:
        """The keywords for the sample in source record"""
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
    def produced_by_responsibilities(self) -> typing.List:
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
    def sampling_site_latitude(self) -> typing.SupportsFloat:
        """The sampling site latitude"""
        pass

    @abstractmethod
    def sampling_site_longitude(self) -> typing.SupportsFloat:
        """The sampling site longitude"""
        pass

    @abstractmethod
    def sampling_site_place_names(self) -> typing.List:
        """The sampling site longitude"""
        pass

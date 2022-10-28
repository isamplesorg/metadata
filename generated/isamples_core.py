# Auto generated from isamples_core.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-10-28T08:40:36
# Schema: physicalSample
#
# id: http://resource.isamples.org/schema/0.2.1
# description: Startup schema for iSamples sample registry integration. updated from 0.2 by synchronizing the
#              vocabulary enumerations, change 'id' to '@id' and 'schema' to '$schema'. Schema name is
#              iSamplesSchemaBasic0.2.1.json. Target JSON schema version is
#              http://json-schema.org/draft-07/schema# SMR 2022-10-07
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.metamodelcore import Decimal

metamodel_version = "1.7.0"
version = "20221007"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
DCT = CurieNamespace('dct', 'http://purl.org/dc/terms/')
ISAM = CurieNamespace('isam', 'http://resource.isamples.org/schema/')
MAT = CurieNamespace('mat', 'https://w3id.org/isample/vocabulary/material/0.9/')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SDO = CurieNamespace('sdo', 'http://schema.org/')
SF = CurieNamespace('sf', 'https://w3id.org/isample/vocabulary/sampledfeature/0.9/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
SPEC = CurieNamespace('spec', 'https://w3id.org/isample/vocabulary/specimentype/0.9/')
W3CPOS = CurieNamespace('w3cpos', 'http://www.w3.org/2003/01/geo/wgs84_pos#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = ISAM


# Types
class Date(str):
    type_class_uri = XSD.date
    type_class_curie = "xsd:date"
    type_name = "date"
    type_model_uri = ISAM.Date


class String(str):
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "string"
    type_model_uri = ISAM.String


class Decimal(Decimal):
    type_class_uri = XSD.decimal
    type_class_curie = "xsd:decimal"
    type_name = "decimal"
    type_model_uri = ISAM.Decimal


# Class references



@dataclass
class PhysicalSampleRecord(YAMLRoot):
    """
    This is a data object that is a digital representation of a physical sample, and thus shares the same identifier
    as the physical object. It provides descriptive properties for any iSamples physical sample, URI for the metadata
    record is same as URI for physical sample-- digital object is considered twin of physical object, a
    representation. IGSN is recommended. Must be a URI that can be dereferenced on the web.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ISAM.PhysicalSampleRecord
    class_class_curie: ClassVar[str] = "isam:PhysicalSampleRecord"
    class_name: ClassVar[str] = "PhysicalSampleRecord"
    class_model_uri: ClassVar[URIRef] = ISAM.PhysicalSampleRecord

    label: str = None
    sample_identifier: str = None
    authorized_by: Optional[str] = None
    complies_with: Optional[str] = None
    curation: Optional[Union[dict, "SpecimenCuration"]] = None
    description: Optional[str] = None
    has_context_category: Optional[Union[str, List[str]]] = empty_list()
    has_material_category: Optional[Union[Union[str, "Materialtype"], List[Union[str, "Materialtype"]]]] = empty_list()
    has_specimen_category: Optional[Union[str, List[str]]] = empty_list()
    informal_classification: Optional[Union[str, List[str]]] = empty_list()
    keywords: Optional[Union[str, List[str]]] = empty_list()
    produced_by: Optional[Union[dict, "SamplingEvent"]] = None
    related_resource: Optional[Union[dict, "SampleRelation"]] = None
    registrant: Optional[str] = None
    sampling_purpose: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.label):
            self.MissingRequiredField("label")
        if not isinstance(self.label, str):
            self.label = str(self.label)

        if self._is_empty(self.sample_identifier):
            self.MissingRequiredField("sample_identifier")
        if not isinstance(self.sample_identifier, str):
            self.sample_identifier = str(self.sample_identifier)

        if self.authorized_by is not None and not isinstance(self.authorized_by, str):
            self.authorized_by = str(self.authorized_by)

        if self.complies_with is not None and not isinstance(self.complies_with, str):
            self.complies_with = str(self.complies_with)

        if self.curation is not None and not isinstance(self.curation, SpecimenCuration):
            self.curation = SpecimenCuration(**as_dict(self.curation))

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.has_context_category, list):
            self.has_context_category = [self.has_context_category] if self.has_context_category is not None else []
        self.has_context_category = [v if isinstance(v, str) else str(v) for v in self.has_context_category]

        if not isinstance(self.has_material_category, list):
            self.has_material_category = [self.has_material_category] if self.has_material_category is not None else []
        self.has_material_category = [v if isinstance(v, Materialtype) else Materialtype(v) for v in self.has_material_category]

        if not isinstance(self.has_specimen_category, list):
            self.has_specimen_category = [self.has_specimen_category] if self.has_specimen_category is not None else []
        self.has_specimen_category = [v if isinstance(v, str) else str(v) for v in self.has_specimen_category]

        if not isinstance(self.informal_classification, list):
            self.informal_classification = [self.informal_classification] if self.informal_classification is not None else []
        self.informal_classification = [v if isinstance(v, str) else str(v) for v in self.informal_classification]

        if not isinstance(self.keywords, list):
            self.keywords = [self.keywords] if self.keywords is not None else []
        self.keywords = [v if isinstance(v, str) else str(v) for v in self.keywords]

        if self.produced_by is not None and not isinstance(self.produced_by, SamplingEvent):
            self.produced_by = SamplingEvent(**as_dict(self.produced_by))

        if self.related_resource is not None and not isinstance(self.related_resource, SampleRelation):
            self.related_resource = SampleRelation(**as_dict(self.related_resource))

        if self.registrant is not None and not isinstance(self.registrant, str):
            self.registrant = str(self.registrant)

        if self.sampling_purpose is not None and not isinstance(self.sampling_purpose, str):
            self.sampling_purpose = str(self.sampling_purpose)

        super().__post_init__(**kwargs)


@dataclass
class SamplingSite(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ISAM.SamplingSite
    class_class_curie: ClassVar[str] = "isam:SamplingSite"
    class_name: ClassVar[str] = "SamplingSite"
    class_model_uri: ClassVar[URIRef] = ISAM.SamplingSite

    description: Optional[str] = None
    label: Optional[str] = None
    location: Optional[Union[dict, "GeospatialDDCoordLocation"]] = None
    place_name: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        if self.location is not None and not isinstance(self.location, GeospatialDDCoordLocation):
            self.location = GeospatialDDCoordLocation(**as_dict(self.location))

        if not isinstance(self.place_name, list):
            self.place_name = [self.place_name] if self.place_name is not None else []
        self.place_name = [v if isinstance(v, str) else str(v) for v in self.place_name]

        super().__post_init__(**kwargs)


@dataclass
class SamplingEvent(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ISAM.SamplingEvent
    class_class_curie: ClassVar[str] = "isam:SamplingEvent"
    class_name: ClassVar[str] = "SamplingEvent"
    class_model_uri: ClassVar[URIRef] = ISAM.SamplingEvent

    description: Optional[str] = None
    has_feature_of_interest: Optional[str] = None
    label: Optional[str] = None
    responsibility: Optional[Union[str, List[str]]] = empty_list()
    result_time: Optional[str] = None
    sampling_site: Optional[Union[dict, SamplingSite]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.has_feature_of_interest is not None and not isinstance(self.has_feature_of_interest, str):
            self.has_feature_of_interest = str(self.has_feature_of_interest)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        if not isinstance(self.responsibility, list):
            self.responsibility = [self.responsibility] if self.responsibility is not None else []
        self.responsibility = [v if isinstance(v, str) else str(v) for v in self.responsibility]

        if self.result_time is not None and not isinstance(self.result_time, str):
            self.result_time = str(self.result_time)

        if self.sampling_site is not None and not isinstance(self.sampling_site, SamplingSite):
            self.sampling_site = SamplingSite(**as_dict(self.sampling_site))

        super().__post_init__(**kwargs)


@dataclass
class GeospatialDDCoordLocation(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ISAM.GeospatialDDCoordLocation
    class_class_curie: ClassVar[str] = "isam:GeospatialDDCoordLocation"
    class_name: ClassVar[str] = "GeospatialDDCoordLocation"
    class_model_uri: ClassVar[URIRef] = ISAM.GeospatialDDCoordLocation

    elevation: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.elevation is not None and not isinstance(self.elevation, str):
            self.elevation = str(self.elevation)

        if self.latitude is not None and not isinstance(self.latitude, Decimal):
            self.latitude = Decimal(self.latitude)

        if self.longitude is not None and not isinstance(self.longitude, Decimal):
            self.longitude = Decimal(self.longitude)

        super().__post_init__(**kwargs)


@dataclass
class SpecimenCuration(YAMLRoot):
    """
    object contains information about current storage of sample, access to sample, and events in curation history.
    Curation as used here starts when the sample is removed from its original context, and might include various
    processing steps for preservation. Processing related to analysis preparation such as crushing, dissolution,
    evaporation, filtering are considered part of the sampling method for the derived child sample.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ISAM.SpecimenCuration
    class_class_curie: ClassVar[str] = "isam:SpecimenCuration"
    class_name: ClassVar[str] = "SpecimenCuration"
    class_model_uri: ClassVar[URIRef] = ISAM.SpecimenCuration

    access_constraints: Optional[Union[str, List[str]]] = empty_list()
    curation_location: Optional[str] = None
    description: Optional[str] = None
    label: Optional[str] = None
    responsibility: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.access_constraints, list):
            self.access_constraints = [self.access_constraints] if self.access_constraints is not None else []
        self.access_constraints = [v if isinstance(v, str) else str(v) for v in self.access_constraints]

        if self.curation_location is not None and not isinstance(self.curation_location, str):
            self.curation_location = str(self.curation_location)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        if not isinstance(self.responsibility, list):
            self.responsibility = [self.responsibility] if self.responsibility is not None else []
        self.responsibility = [v if isinstance(v, str) else str(v) for v in self.responsibility]

        super().__post_init__(**kwargs)


@dataclass
class SampleRelation(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ISAM.SampleRelation
    class_class_curie: ClassVar[str] = "isam:SampleRelation"
    class_name: ClassVar[str] = "SampleRelation"
    class_model_uri: ClassVar[URIRef] = ISAM.SampleRelation

    description: Optional[str] = None
    label: Optional[str] = None
    relationship: Optional[str] = None
    target: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        if self.relationship is not None and not isinstance(self.relationship, str):
            self.relationship = str(self.relationship)

        if self.target is not None and not isinstance(self.target, str):
            self.target = str(self.target)

        super().__post_init__(**kwargs)


# Enumerations
class Materialtype(EnumDefinitionImpl):
    """
    categories for kinds of material that constitute the sample
    """
    Material = PermissibleValue(text="Material",
                                       description="Any material. Top Concept in iSamples Material Category scheme",
                                       meaning=MAT.material)
    Mineral = PermissibleValue(text="Mineral",
                                     description="Material consists of a single mineral or mineraloid phase. 'A mineral is an element or chemical compound that is normally crystalline and that has been formed as a result of geological processes.' (Nickel, Ernest H. (1995), The definition of a mineral, The Canadian Mineralogist. 33(3):689–90). Include mineraloids. ... A material primarily composed of some substance that is naturally occurring, solid and stable at room temperature, representable by a chemical formula, usually abiogenic, and that has an ordered atomic structure. The identity of a mineral species is defined by a crystal structure and a chemical composition that might include various specific elemental substitutions in that structure. Mineraloid--A naturally occurring mineral-like substance that does not demonstrate crystallinity. Mineraloids (https://en.wikipedia.org/wiki/Mineraloid) possess chemical compositions that vary beyond the generally accepted ranges for specific minerals. Examples-obsidian, Opal.",
                                     meaning=MAT.mineral)
    Particulate = PermissibleValue(text="Particulate",
                                             description="Material consists of microscopic particulate material derived by precipitation, filtering, or settling from suspension in a fluid, e.g. filtrate from water, deposition from atmosphere, astro material particles. Might include mineral, organic, or biological material. ENVO definition (ENVO_01000060) has \"composed of microscopic portions of solid or liquid material suspended in another environmental material.\", refine here to define as the solid particles, distinct from a material in which they are suspended. A material that includes solid or liquid particles suspended in another material would be a dispersed_media in this scheme, not defined in ENVO. Human manufactured particulates (e.g. rock powder) should be categorized as 'anthropogenic material' as well as 'Particulate'",
                                             meaning=MAT.particulate)
    Rock = PermissibleValue(text="Rock",
                               description="Consolidated aggregate of particles (grains) of rock, mineral (including native elements), mineraloid, or solid organic material. Includes mineral aggregates such as granite, shale, marble; natural glass such as obsidian; organic material formed by geologic processes such a coal;  extraterrestrial material in meteorites; and  crushed rock fragments like drill cuttings from rock.",
                               meaning=MAT.rock)
    Sediment = PermissibleValue(text="Sediment",
                                       description="Solid granular material transported by wind, water, or gravity, not modified by interaction with biosphere or atmosphere (to differentiate from soil). Particles derived by erosion of pre-existing rock, from shell or other body parts from organisms, or precipitated chemically in the surficial environment (http://resource.geosciml.org/classifier/cgi/lithology/sediment). Sediment is not consolidated, i.e. Particulate constituents of a compound material do not adhere to each other strongly enough that the aggregate can be considered a solid material in its own right. NOTE that some chemical sediments crystallize directly as solid material or aggregates when deposited, but are considered sediment because of their origin.",
                                       meaning=MAT.sediment)
    Soil = PermissibleValue(text="Soil",
                               description="Mixed granular mineral and organic matter modified by interaction between earth material, biosphere, and atmosphere, consisting mostly of varying proportions of sand, silt, and clay, organic material such as humus, gases, liquids, and a broad range of resident micro- and macroorganisms. Soil consists of horizons near the Earth's surface that, in contrast to the underlying parent material, have been altered by the interactions of climate, relief, and living organisms over time.",
                               meaning=MAT.soil)

    _defn = EnumDefinition(
        name="Materialtype",
        description="categories for kinds of material that constitute the sample",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "Any anthropogenic material",
                PermissibleValue(text="Any anthropogenic material",
                                 description="Material produced by human activity. Intention is for materials that would not be found in nature without human intervention. Thus clay would be a 'Mineral' material, but fired clay in a brick or ceramic would be an 'Anthropogenic material'.   Native copper would be a Mineral, but smelted copper, extracted from ore that might include native copper (among other sulfide and oxide minerals) would be 'Anthropogenic metal material'. This is a general class for undifferentiated metal or non-metal anthropogenic material.",
                                 meaning=MAT.anyanthropogenicmaterial) )
        setattr(cls, "Anthropogenic material",
                PermissibleValue(text="Anthropogenic material",
                                 description="Non-metallic material produced by human activity. Organic products of agricultural activity are both anthropogenic and organic. Include lab preparations like XRF pellet and rock powders. Examples-- ceramics, brick, concrete, slag, (anthropogenic) glass, mine tailing, plaster, waste.",
                                 meaning=MAT.otheranthropogenicmaterial) )
        setattr(cls, "Anthropogenic metal material",
                PermissibleValue(text="Anthropogenic metal material",
                                 description="Specimen is dominantly composed of metal that has been produced or used by humans; subclass of anthropogenic material. Samples of naturally occuring metallic material (e.g. native copper, gold nuggets) should be considered mineral material. Metallic material is material that when polished or fractured, shows a lustrous appearance, and conducts electricity and heat relatively well. Metals are typically malleable (they can be hammered into thin sheets) or ductile (can be drawn into wires). The boundaries between metals, nonmetals, and metalloids fluctuate slightly due to a lack of universally accepted definitions of the categories involved.",
                                 meaning=MAT.anthropogenicmetal) )
        setattr(cls, "Any Ice",
                PermissibleValue(text="Any Ice",
                                 description="a solid material that is normally a liquid or gas at Standard Temperature and Pressre (STP)  that is in a solid state under the observed temperature and pressure conditions. Samples of non-aqueous ice should be classified as 'Any ice'. This is considered enough of an edge case that distinguishing 'ice that might or might not be aqueous' from 'non-aqueous ice' does not merit adding another class to the scheme.",
                                 meaning=MAT.anyice) )
        setattr(cls, "Biogenic non-organic material",
                PermissibleValue(text="Biogenic non-organic material",
                                 description="Material produced by an organism but not composed of 'very large molecules of biological origin.' E.g. bone, tooth, shell, coral skeleton",
                                 meaning=MAT.biogenicnonorganicmaterial) )
        setattr(cls, "Dispersed media",
                PermissibleValue(text="Dispersed media",
                                 description="A material contains discrete elements of one medium that are dispersed in a continuous fluid medium.  The dispersed component can be a gas, a liquid or a solid (based on https //en.wikipedia.org/wiki/Dispersed_media). Does not include mixtures of granular material like soil, sediment, particulate, or solids that would be considered a rock. E.g. aerosol ENVO_00010505, foam ENVO_00005738, emulsion ENVO_00010506, colloidal suspension ENVO_01001560, scum(?)ENVO:00003930, clathrate?",
                                 meaning=MAT.dispersedmedia) )
        setattr(cls, "Fluid material",
                PermissibleValue(text="Fluid material",
                                 description="a substance that continually deforms (flows) under an applied shear stress, or external force. Fluids are a phase of matter and include liquids, gases and plasmas. They are substances with zero shear modulus, or, in simpler terms, substances that cannot resist any shear force applied to them.",
                                 meaning=MAT.fluid) )
        setattr(cls, "Gaseous material",
                PermissibleValue(text="Gaseous material",
                                 description="Material composed of one or more chemical entities that has neither independent shape nor volume but tends to expand indefinitely",
                                 meaning=MAT.gas) )
        setattr(cls, "Frozen water",
                PermissibleValue(text="Frozen water",
                                 description="Water that is in a solid state.",
                                 meaning=MAT.waterice) )
        setattr(cls, "Liquid water",
                PermissibleValue(text="Liquid water",
                                 description="A material primarily composed of dihydrogen oxide in its liquid form; infer that the sample is curated in some kind of container.",
                                 meaning=MAT.liquidwater) )
        setattr(cls, "Mixed soil sediment or rock",
                PermissibleValue(text="Mixed soil sediment or rock",
                                 description="Material is mixed aggregation of fragments of undifferentiated soil, sediment or  rock origin. e.g. cuttings from some boreholes (rock fragments and caved soil or sediment). This class is for samples that are solid Earth materials but known not to be mineral or particulate samples. This class is for samples that are solid Earth materials but known not to be mineral or particulate samples.",
                                 meaning=MAT.mixedsoilsedimentrock) )
        setattr(cls, "Natural Solid Material",
                PermissibleValue(text="Natural Solid Material",
                                 description="Undifferentiated, mineral, soil, sediment, rock, or natural particulates. Typically (nessarily?) a granular aggregate that might include any of the previous constiturents. Use for Earth Material aggregates of uncertain origin",
                                 meaning=MAT.earthmaterial) )
        setattr(cls, "Non-aqueous liquid material",
                PermissibleValue(text="Non-aqueous liquid material",
                                 description="Liquid composed dominantly of material other than water. Includes liquids that do not fit in any other category. E.g. alcohol, petroleum. Fluids like blood, urine, mucus are problematic. Suggest categorizing as 'Non-aqueous liquid material' and 'Organic material' or 'Biogenic non-organic material'.",
                                 meaning=MAT.nonaqueousliquid) )
        setattr(cls, "Not Provided",
                PermissibleValue(text="Not Provided",
                                 description="use for missing values, explicit null. This is not a term from the iSamples materials vocabulary, but included for software implementation.") )
        setattr(cls, "Organic material",
                PermissibleValue(text="Organic material",
                                 description="Environmental material derived from living organisms and composed primarily of one or more very large molecules of biological origin. Examples--body (animal or plant), body part, fecal matter, seeds, wood, tissue, biological fluids, biological waste, algal material, biofilm, necromass, plankton.  Distinction from 'Biogenic non-organic material' is fuzzy. Biogenic non-organic material is intended to cover biogenic products consisting of mineral or mineraloid substance, e.g. apatite (or other Ca phosphates), aragonite (or other Ca carbonate) typical of shells, bone, teeth. Also note potential overlap with organic compounds that occur as naturally formed minerals ('Organic mineral', in geo materials mineral group extension vocabulary).",
                                 meaning=MAT.organicmaterial) )
        setattr(cls, "Rock or sediment",
                PermissibleValue(text="Rock or sediment",
                                 description="Material is rock or sediment.  E.g. for samples from subsurface cores that are not well described, from drill holes that likely penetrate sediment near the surface an might be sampling rock at greater depth, or sea floor dredge haul consisting of mixed sediment and rock. Distinct from 'Mixed soil, sediment or rock' that represents samples known to have components of all these materials.",
                                 meaning=MAT.rockorsediment) )

class Specimencategory(EnumDefinitionImpl):
    """
    specify the kind of object that the specimen is
    """
    Aggregation = PermissibleValue(text="Aggregation",
                                             description="An aggregate specimen that is not biogenic or composed of anthropogenic material fragments.  Examples-- loose soil or sediment (e.g. in a bag), rock chips, particulate filtrate or precipitate; rock powders.",
                                             meaning=SPEC.genericaggregation)
    Artifact = PermissibleValue(text="Artifact",
                                       description="An object made (manufactured, shaped, modified) by a human being, or precursor hominid. Include a set of pieces belonging originally to a single object and treated as a single specimen.",
                                       meaning=SPEC.artifact)
    Fossil = PermissibleValue(text="Fossil",
                                   description="Specimen is the remains of one or more organisms preserved in rock; includes whole body, body parts (usually bone or shell), and trace fossils. An organism or organism part becomes a fossil when it has undergone some fossilization process that generally entails physical and chemical changes akin to diagenesis in a sedimentary rock. Trace fossils are manifestations of biologic activity preserved in a rock body (typically sedimentary), without included preserved body parts.  There are many processes that lead to fossilization, including permineralization, casts and molds, authigenic mineralization, replacement and recrystallization, adpression, carbonization, and bioimmuration.",
                                   meaning=SPEC.fossil)

    _defn = EnumDefinition(
        name="Specimencategory",
        description="specify the kind of object that the specimen is",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "Any aggregation sample",
                PermissibleValue(text="Any aggregation sample",
                                 description="Sample consists of a bunch of material fragments, not related to the same object (e.g. not a bunch of broken pot sherds that might be reassembled), but taken together representative of the sampled feature. Examples--loose soil, sediment, crushed rock,  particulate, bunches of unrelated pot sherd, human production waste, filtrates and residues. The sample requires some kind of container to keep it together. Cores of loosely consolidated material are considered 'piece of solid material' because the internal parts have spatial relationships (e.g. upper part, lower part).",
                                 meaning=SPEC.anyaggregation) )
        setattr(cls, "Analytical preparation",
                PermissibleValue(text="Analytical preparation",
                                 description="Specimen is a product of processing required for some observation procedure, e.g. thin section, XRF bead, SEM stub, rock powder. If identified separately, this should have a ‘parent’ link to the original sample",
                                 meaning=SPEC.analyticalpreparation) )
        setattr(cls, "Anthropogenic aggregation",
                PermissibleValue(text="Anthropogenic aggregation",
                                 description="Aggregation consists of fragments of material produced by human activity,  not described individually, and generally not all originating from the same object.  Includes pottery in an excavation unit that gets an aggregate description, production waste, production raw-materials, or other residues (broken bits of plaster from an destroyed wall), synthetic powders.",
                                 meaning=SPEC.anthropogenicaggregation) )
        setattr(cls, "Any biological sample",
                PermissibleValue(text="Any biological sample",
                                 description="Specimen that represents one or more living or once-living organisms.",
                                 meaning=SPEC.biologicalspecimen) )
        setattr(cls, "Biome aggregation sample",
                PermissibleValue(text="Biome aggregation sample",
                                 description="Specimen is an aggregation of whole or fragmentary parts of multiple organisms, microscopic or megascopic, representative of some site.",
                                 meaning=SPEC.biomeaggregation) )
        setattr(cls, "Bundle biome aggregation",
                PermissibleValue(text="Bundle biome aggregation",
                                 description="An aggregation of whole organisms representative of some biome",
                                 meaning=SPEC.bundlebiomeaggregation) )
        setattr(cls, "Experiment product",
                PermissibleValue(text="Experiment product",
                                 description="Specimen is product of an experimental procedure (e.g. synthetic material)",
                                 meaning=SPEC.experimentalproduct) )
        setattr(cls, "Fluid in container",
                PermissibleValue(text="Fluid in container",
                                 description="Specimen is a container whose contents are liquid, gas, or mixed dominantly fluid phases, that is the actual sample material. Fluid might include minor solid particles. Container typically human made, but also includes natural fluid container, e.g. fluid inclusion in a mineral grain.  Includes colloids, foams, gels, suspensions. The sample is the fluid substance; fluid samples collected to analyze the contained biome should be considered 'Biome Aggregation'",
                                 meaning=SPEC.fluidincontainer) )
        setattr(cls, "Organism part",
                PermissibleValue(text="Organism part",
                                 description="Part of an organism, e.g. a tissue sample, plant leaf, flower, bird feather. Include internal parts not composed of organic material (e.g. teeth, bone), and hard body parts that are not shed (hoof, horn, tusk, claw).  Hair is tricky, include here for now.  Does not necessarily imply existance of parent sample. Not fossilized; generally includes organism parts native to deposits of Holocene to Recent age.",
                                 meaning=SPEC.organismpart) )
        setattr(cls, "Organism product",
                PermissibleValue(text="Organism product",
                                 description="Specimen is a thing produced by some organism, generally not composed of organic material or including biological tissue, e.g. Shell, antler, egg shell, coral skeleton (organic tissue not included), fecal matter, cocoon, web, gut content.  Consider internal parts not composed of organic material (e.g. teeth, bone) and hard body parts that are not shed (hoof, horn, tusk) to be organism parts.",
                                 meaning=SPEC.organismproduct) )
        setattr(cls, "Other solid object",
                PermissibleValue(text="Other solid object",
                                 description="Single piece of material not one of the other types, e.g. rock specimen, mineral specimen, core. Ice and permafrost are considered solid materials.",
                                 meaning=SPEC.othersolidobject) )
        setattr(cls, "Material sample",
                PermissibleValue(text="Material sample",
                                 description="top concept in specimen type hierarchy.  Represents any physical specimen.",
                                 meaning=SPEC.physicalspecimen) )
        setattr(cls, "Research product",
                PermissibleValue(text="Research product",
                                 description="Specimen is a product of some research workflow, e.g. a thin section, an XRF pellet, a grain mount, SEM stub, synthetic rock or mineral ...  In general there should be a link to a parent specimen from which this was derived.  Might be aggregation (e.g. a synthetic material powder) or a solid object.",
                                 meaning=SPEC.researchproduct) )
        setattr(cls, "Slurry biome aggregation",
                PermissibleValue(text="Slurry biome aggregation",
                                 description="a material that consists of mixed organic and inorganic material, including whole organisms and organism fragments.",
                                 meaning=SPEC.slurrybiomeaggregation) )
        setattr(cls, "Whole organism sample",
                PermissibleValue(text="Whole organism sample",
                                 description="Specimen consists of the bodies of one or more entire organisms of the same species, from any kingdom. Note that these are also inherently 'solid object’",
                                 meaning=SPEC.wholeorganism) )
        setattr(cls, "Not Provided",
                PermissibleValue(text="Not Provided",
                                 description="term to use for explicit missing values in required fields. The term is not part of the MaterialSampleType vocabulary.") )

class Contextcategory(EnumDefinitionImpl):
    """
    top level context, based on the kind of feature sampled,from the SampledFeature vocabulary. Specific
    identification of the sampled feature of interest is done through the SamplingEvent/Feature of Interest property.
    """
    Atmosphere = PermissibleValue(text="Atmosphere",
                                           description="specimen samples the Earth's atmosphere",
                                           meaning=SF.atmosphere)

    _defn = EnumDefinition(
        name="Contextcategory",
        description="top level context, based on the kind of feature sampled,from the SampledFeature vocabulary.  Specific identification of the sampled feature of interest is done through the SamplingEvent/Feature of Interest property.",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "Active human occupation site",
                PermissibleValue(text="Active human occupation site",
                                 description="Specimen samples materials or objects produced by current or ongoing human activity",
                                 meaning=SF.activehumanoccupationsite) )
        setattr(cls, "Anthropogenic environment",
                PermissibleValue(text="Anthropogenic environment",
                                 description="Sampled feature is produced by or related to human activity past or present.",
                                 meaning=SF.anthropogenicenvironment) )
        setattr(cls, "Any sampled feature",
                PermissibleValue(text="Any sampled feature",
                                 description="Top concept in sampled feature type vocabulary.",
                                 meaning=SF.anysampledfeature) )
        setattr(cls, "Biological entity",
                PermissibleValue(text="Biological entity",
                                 description="Sampled feature is an organism. Use for samples that represent some species of organism as the proximate sampled feature for which the focus is not the environment that the organism inhabits. Domain specific vocabulary extension will be useful to distinguish samples from different phyla/order/class...",
                                 meaning=SF.biologicalentity) )
        setattr(cls, "Earth environment",
                PermissibleValue(text="Earth environment",
                                 description="specimen samples the natural earth environment",
                                 meaning=SF.earthenvironment) )
        setattr(cls, "Earth interior",
                PermissibleValue(text="Earth interior",
                                 description="Specimen samples solid material within the earth (fluids in pore space in earth interior sample 'subsurface fluid reservoir')",
                                 meaning=SF.earthinterior) )
        setattr(cls, "Earth surface",
                PermissibleValue(text="Earth surface",
                                 description="Specimen samples the interface between solid earth and hydrosphere or atmosphere. Includes samples representing things collected on the surface, or in the uppermost part of the material below the surface. Not including recently deposited sediment that has not been modified by interaction with the surface environment.",
                                 meaning=SF.earthsurface) )
        setattr(cls, "Experiment setting",
                PermissibleValue(text="Experiment setting",
                                 description="Sampled feature is the expermental set up that produced the sample.",
                                 meaning=SF.experimentsetting) )
        setattr(cls, "Extraterrestrial environment",
                PermissibleValue(text="Extraterrestrial environment",
                                 description="specimen samples environment outside of solid earth, hydrosphere, or atmosphere.",
                                 meaning=SF.extraterrestrialenvironment) )
        setattr(cls, "Glacier environment",
                PermissibleValue(text="Glacier environment",
                                 description="Sample of ice or water from a glacier, ice sheet, ice shelf, iceberg. Does not include various environments adjacent to glacier.",
                                 meaning=SF.glacierenvironment) )
        setattr(cls, "Laboratory or curatorial environment",
                PermissibleValue(text="Laboratory or curatorial environment",
                                 description="specimen samples environment in a laboratory; e.g. lab blank measurements.",
                                 meaning=SF.laboratorycuratorialenvironment) )
        setattr(cls, "Lake river or stream bottom",
                PermissibleValue(text="Lake river or stream bottom",
                                 description="Specimen samples the solid Earth interface with a lake or flowing water body",
                                 meaning=SF.lakeriverstreambottom) )
        setattr(cls, "Marine environment",
                PermissibleValue(text="Marine environment",
                                 description="specimen samples marine hydrosphere",
                                 meaning=SF.marinewaterbody) )
        setattr(cls, "Marine water body bottom",
                PermissibleValue(text="Marine water body bottom",
                                 description="Specimen samples the solid Earth interface with marine or brackish water body. Includes benthic boundary layer--the bottom layer of water and the uppermost layer of sediment directly influenced by the overlying water",
                                 meaning=SF.marinewaterbodybottom) )
        setattr(cls, "Site of past human activities",
                PermissibleValue(text="Site of past human activities",
                                 description="specimen samples a place where humans have been and left evidence of their activity. Includes prehistoric and paleo hominid sites",
                                 meaning=SF.pasthumanoccupationsite) )
        setattr(cls, "Subaerial surface environment",
                PermissibleValue(text="Subaerial surface environment",
                                 description="Specimen samples the  interface between solid Earth and atmosphere.  Sample is collected on the surface, or immediately below surface (zone of bioturbation). Include soil ‘O’ horizon and ‘biomantle’. Soil horizons below surface, or sediment in active deposition (no soil development) is considered part of solid Earth.",
                                 meaning=SF.subaerialsurfaceenvironment) )
        setattr(cls, "Subsurface fluid reservoir",
                PermissibleValue(text="Subsurface fluid reservoir",
                                 description="Specimen samples fluid that resides in fractures or intergranular porosity in the solid earth.",
                                 meaning=SF.subsurfacefluidreservoir) )
        setattr(cls, "Terrestrial water body",
                PermissibleValue(text="Terrestrial water body",
                                 description="specimen samples terrestrial hydrosphere-- lake, other standing water, or a flowing water body (river, stream..) Include saline water in terrestrial evaporite environments.",
                                 meaning=SF.terrestrialwaterbody) )
        setattr(cls, "Water body",
                PermissibleValue(text="Water body",
                                 description="specimen samples the hydrosphere",
                                 meaning=SF.waterbody) )
        setattr(cls, "Not Provided",
                PermissibleValue(text="Not Provided",
                                 description="term to use for explicit missing values in required fields. The term is not part of the MaterialSampleType vocabulary.") )

# Slots


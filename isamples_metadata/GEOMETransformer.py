import datetime
import logging
import typing

from isamples_metadata.Transformer import (
    Transformer,
)

TISSUE_ENTITY = "Tissue"
JSON_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


# Forward declarations appear to be the cleanest way to manage the circular dependency between these two classes
class GEOMETransformer(Transformer):
    pass


class GEOMEChildTransformer(GEOMETransformer):
    pass


class GEOMETransformer(Transformer):
    """Concrete transformer class for going from a GEOME record to an iSamples record"""

    def __init__(
        self, source_record: typing.Dict, last_updated_time: datetime.datetime
    ):
        super().__init__(source_record)
        self._child_transformers = []
        self._last_updated_time = last_updated_time
        children = self._get_children()
        for child_record in children:
            entity = child_record.get("entity")
            if entity == TISSUE_ENTITY:
                self._child_transformers.append(
                    GEOMEChildTransformer(
                        source_record, child_record, last_updated_time
                    )
                )

    ARK_PREFIX = "ark:/"

    def _source_record_main_record(self) -> typing.Dict:
        # The sub-record for the main record, as opposed to the parent or children records
        return self.source_record["record"]

    def _source_record_parent_record(self) -> typing.Dict:
        # The sub-record for the parent record
        return self.source_record["parent"]

    def _id_minus_prefix(self) -> typing.AnyStr:
        return self._source_record_main_record()["bcid"].removeprefix(self.ARK_PREFIX)

    def id_string(self) -> typing.AnyStr:
        return f"metadata/{self._id_minus_prefix()}"

    def sample_label(self) -> typing.AnyStr:
        main_record = self._source_record_main_record()
        label_components = []
        scientific_name = main_record.get("scientificName")
        if scientific_name is not None:
            label_components.append(scientific_name)
        sample_id = main_record.get("materialSampleID")
        if sample_id is not None:
            label_components.append(sample_id)
        return " ".join(label_components)

    def sample_identifier_string(self) -> typing.AnyStr:
        return self._source_record_main_record()["bcid"]

    def sample_description(self) -> typing.AnyStr:
        description_pieces = []
        main_record = self._source_record_main_record()

        self._transform_key_to_label(
            "minimumChronometricAgeReferenceSystem", main_record, description_pieces
        )
        self._transform_key_to_label(
            "maximumChronometricAgeReferenceSystem", main_record, description_pieces
        )
        self._transform_key_to_label(
            "verbatimAgeValue", main_record, description_pieces
        )
        self._transform_key_to_label("ageValue", main_record, description_pieces)
        self._transform_key_to_label("basisOfRecord", main_record, description_pieces)
        self._transform_key_to_label(
            "dynamicProperties", main_record, description_pieces
        )
        self._transform_key_to_label(
            "establishmentMeans", main_record, description_pieces
        )
        self._transform_key_to_label(
            "genbankSpecimenVoucher", main_record, description_pieces
        )
        self._transform_key_to_label(
            "identificationRemarks", main_record, description_pieces
        )
        self._transform_key_to_label(
            "identificationVerificationStatus", main_record, description_pieces
        )
        self._transform_key_to_label("individualCount", main_record, description_pieces)
        self._transform_key_to_label(
            "morphospeciesDescription", main_record, description_pieces
        )
        self._transform_key_to_label(
            "nomenclaturalCode", main_record, description_pieces
        )
        self._transform_key_to_label(
            "occurrenceRemarks", main_record, description_pieces
        )
        self._transform_key_to_label("organismID", main_record, description_pieces)
        self._transform_key_to_label(
            "organismQuantity", main_record, description_pieces
        )
        self._transform_key_to_label(
            "organismQuantityType", main_record, description_pieces
        )
        self._transform_key_to_label("organismRemarks", main_record, description_pieces)
        self._transform_key_to_label(
            "otherCatalogNumbers", main_record, description_pieces
        )
        self._transform_key_to_label(
            "previousIdentifications", main_record, description_pieces
        )
        self._transform_key_to_label("taxonRemarks", main_record, description_pieces)
        self._transform_key_to_label("typeStatus", main_record, description_pieces)
        self._transform_key_to_label(
            "verbatimLifeStage", main_record, description_pieces
        )
        self._transform_key_to_label("weight", main_record, description_pieces)
        self._transform_key_to_label("weightUnits", main_record, description_pieces)
        self._transform_key_to_label("lengthUnits", main_record, description_pieces)
        self._transform_key_to_label("length", main_record, description_pieces)
        self._transform_key_to_label("sex", main_record, description_pieces)

        return Transformer.DESCRIPTION_SEPARATOR.join(description_pieces)

    def has_context_categories(self) -> typing.List[typing.AnyStr]:
        # TODO: implement
        # ["[infer from locality and taxon names]"]
        return []

    def has_material_categories(self) -> typing.List[typing.AnyStr]:
        # TODO: implement
        # ["'Organic material' unless record/entity, record/basisOfRecord, or record/collectionCode indicate otherwise"]
        return ["Organic material"]

    def has_specimen_categories(self) -> typing.List[typing.AnyStr]:
        # TODO: implement
        # ["'Whole organism'  unless record/entity, record/basisOfRecord, or record/collectionCode indicate otherwise"]
        return ["Whole organism"]

    def informal_classification(self) -> typing.List[typing.AnyStr]:
        main_record = self._source_record_main_record()
        scientific_name = main_record.get("scientificName")
        if scientific_name is None:
            informal_classification_pieces = []
            genus = main_record.get("genus")
            if genus is not None:
                informal_classification_pieces.append(genus)
            epithet = main_record.get("specificEpithet")
            if epithet is not None:
                informal_classification_pieces.append(epithet)
            return informal_classification_pieces
        else:
            return [scientific_name]

    def _place_names(self, only_general: bool) -> typing.List[typing.AnyStr]:
        parent_record = self._source_record_parent_record()
        if parent_record is not None:
            place_names = []
            if not only_general:
                if "locality" in parent_record:
                    place_names.append(parent_record["locality"])
            if "county" in parent_record:
                place_names.append(parent_record["county"])
            if "stateProvince" in parent_record:
                place_names.append(parent_record["stateProvince"])
            if "island" in parent_record:
                place_names.append(parent_record["island"])
            if "islandGroup" in parent_record:
                place_names.append(parent_record["islandGroup"])
            if "country" in parent_record:
                place_names.append(parent_record["country"])
            if "continentOcean" in parent_record:
                place_names.append(parent_record["continentOcean"])
            return place_names
        return []

    def keywords(self) -> typing.List[typing.AnyStr]:
        # "JSON array of values from record/ -order, -phylum, -family, -class, and parent/ -country, -county,
        # -stateProvince, -continentOcean... (place names more general that the locality or most specific
        # rank place name) "
        keywords = self._place_names(True)
        parent_record = self._source_record_parent_record()
        microhabitat = parent_record.get("microHabitat")
        if microhabitat is not None:
            keywords.append(microhabitat)
        order = self._source_record_main_record().get("order")
        if order is not None:
            keywords.append(order)
        phylum = self._source_record_main_record().get("phylum")
        if phylum is not None:
            keywords.append(phylum)
        family = self._source_record_main_record().get("family")
        if family is not None:
            keywords.append(family)
        classname = self._source_record_main_record().get("class")
        if classname is not None:
            keywords.append(classname)
        return keywords

    def produced_by_id_string(self) -> typing.AnyStr:
        parent_record = self._source_record_parent_record()
        if parent_record is not None:
            return parent_record["bcid"]
        return Transformer.NOT_PROVIDED

    def produced_by_label(self) -> typing.AnyStr:
        parent_record = self._source_record_parent_record()
        if parent_record is not None:
            label_pieces = []
            event_id = parent_record.get("eventID")
            if event_id is not None:
                label_pieces.append(event_id)
            expedition_code = parent_record.get("expeditionCode")
            if expedition_code is not None:
                label_pieces.append(expedition_code)
            return " ".join(label_pieces)
        return Transformer.NOT_PROVIDED

    def produced_by_description(self) -> typing.AnyStr:
        parent_record = self._source_record_parent_record()
        if parent_record is not None:
            description_pieces = []
            event_remarks = parent_record.get("eventRemarks")
            if event_remarks is not None:
                description_pieces.append(event_remarks)
            self._transform_key_to_label(
                "samplingProtocol", parent_record, description_pieces
            )
            self._transform_key_to_label(
                "permitInformation", parent_record, description_pieces
            )
            self._transform_key_to_label(
                "expeditionCode", parent_record, description_pieces
            )
            self._transform_key_to_label(
                "taxTeam", parent_record, description_pieces, "taxonomy team"
            )
            self._transform_key_to_label("projectId", parent_record, description_pieces)
            return Transformer.DESCRIPTION_SEPARATOR.join(description_pieces)
        return Transformer.NOT_PROVIDED

    def produced_by_feature_of_interest(self) -> typing.AnyStr:
        # TODO: implement
        # "[infer from specimen category, locality; need to so some unique values analysis]"
        parent_record = self._source_record_parent_record()
        if parent_record is not None:
            microhabitat = parent_record.get("microhabitat")
            if microhabitat is not None:
                return f"microhabitat: {microhabitat}"
        return Transformer.NOT_PROVIDED

    def produced_by_responsibilities(self) -> typing.List[typing.AnyStr]:
        parent_record = self._source_record_parent_record()
        if parent_record is not None:
            responsibilities_pieces = []
            collector_list = parent_record.get("collectorList")
            if collector_list is not None:
                # Have to do some goofy checking here because this string-delimited field can either be a singleton
                # or have different delimiters
                if "," in collector_list:
                    for collector in collector_list.split(", "):
                        responsibilities_pieces.append(f"collector: {collector}")
                elif "|" in collector_list:
                    for collector in collector_list.split("|"):
                        responsibilities_pieces.append(f"collector: {collector}")
                else:
                    responsibilities_pieces.append(f"collector :{collector_list}")
            self._transform_key_to_label(
                "principalInvestigator", parent_record, responsibilities_pieces
            )
            self._transform_key_to_label(
                "identifiedBy", parent_record, responsibilities_pieces
            )
            self._transform_key_to_label(
                "taxTeam", parent_record, responsibilities_pieces, "taxonomy team"
            )
            self._transform_key_to_label(
                "eventEnteredBy",
                parent_record,
                responsibilities_pieces,
                "event registrant",
            )
            return responsibilities_pieces
        return []

    def produced_by_result_time(self) -> typing.AnyStr:
        parent_record = self._source_record_parent_record()
        if parent_record is not None:
            return self._formatted_date(
                parent_record.get("yearCollected"),
                parent_record.get("monthCollected"),
                parent_record.get("dayCollected"),
            )
        return Transformer.NOT_PROVIDED

    def sampling_site_description(self) -> typing.AnyStr:
        parent_record = self._source_record_parent_record()
        if parent_record is not None:
            habitat = parent_record.get("habitat")
            if habitat is not None:
                return habitat
            else:
                depth_to_bottom = parent_record.get("depthOfBottomInMeters")
                if depth_to_bottom is not None:
                    return f"Depth to bottom {depth_to_bottom} m"
        return Transformer.NOT_PROVIDED

    def sampling_site_label(self) -> typing.AnyStr:
        parent_record = self._source_record_parent_record()
        if parent_record is not None:
            return parent_record.get("locality", Transformer.NOT_PROVIDED)
        return Transformer.NOT_PROVIDED

    def sampling_site_elevation(self) -> typing.AnyStr:
        # Note that this is subject to revision based on the outcome of
        # https://github.com/isamplesorg/metadata/issues/35
        parent_record = self._source_record_parent_record()
        if parent_record is not None:
            depth = parent_record.get("maximumDepthInMeters")
            if depth is not None:
                return f"{depth} m"
        return Transformer.NOT_PROVIDED

    def _geo_location_float_value(
        self, key: typing.AnyStr
    ) -> typing.Optional[typing.SupportsFloat]:
        parent_record = self._source_record_parent_record()
        if parent_record is not None:
            geo_location_str = parent_record.get(key)
            if geo_location_str is not None:
                return float(geo_location_str)
        return None

    def sampling_site_latitude(self) -> typing.Optional[typing.SupportsFloat]:
        return self._geo_location_float_value("decimalLatitude")

    def sampling_site_longitude(self) -> typing.Optional[typing.SupportsFloat]:
        return self._geo_location_float_value("decimalLongitude")

    def sampling_site_place_names(self) -> typing.List:
        return self._place_names(False)

    def sample_registrant(self) -> typing.AnyStr:
        return self._source_record_main_record().get(
            "sampleEnteredBy", Transformer.NOT_PROVIDED
        )

    def sample_sampling_purpose(self) -> typing.AnyStr:
        # TODO: implement
        return Transformer.NOT_PROVIDED

    # region Curation

    def curation_label(self) -> typing.AnyStr:
        return Transformer.NOT_PROVIDED

    def curation_description(self) -> typing.AnyStr:
        curation_description_pieces = []
        main_record = self._source_record_main_record()
        self._transform_key_to_label(
            "fixative", main_record, curation_description_pieces
        )
        self._transform_key_to_label(
            "preservative", main_record, curation_description_pieces
        )
        self._transform_key_to_label(
            "modifiedBy", main_record, curation_description_pieces, "record modifiedBy"
        )
        self._transform_key_to_label(
            "modifiedReason", main_record, curation_description_pieces, "modifiedReason"
        )

        sample_identified_pieces = []
        year_identified = main_record.get("yearIdentified")
        if year_identified is not None:
            sample_identified_pieces.append(year_identified)
        month_identified = main_record.get("monthIdentified")
        if month_identified is not None:
            sample_identified_pieces.append(month_identified.zfill(2))
        day_identified = main_record.get("dayIdentified")
        if day_identified is not None:
            sample_identified_pieces.append(day_identified.zfill(2))
        if len(sample_identified_pieces) > 0:
            curation_description_pieces.append(
                f"sample identified: {'-'.join(sample_identified_pieces)}"
            )
        if len(curation_description_pieces) > 0:
            return "; ".join(curation_description_pieces)
        return Transformer.NOT_PROVIDED

    def curation_access_constraints(self) -> typing.AnyStr:
        return Transformer.NOT_PROVIDED

    def curation_location(self) -> typing.AnyStr:
        return self._source_record_main_record().get(
            "institutionCode", Transformer.NOT_PROVIDED
        )

    def curation_responsibility(self) -> typing.AnyStr:
        if "institutionCode" in self._source_record_main_record():
            institution_code = self._source_record_main_record()["institutionCode"]
            return f"curator:{institution_code}"
        return Transformer.NOT_PROVIDED

    # endregion

    def _get_children(self) -> typing.List[typing.Dict]:
        children = []
        if "children" in self.source_record:
            children = self.source_record["children"]
        return children

    def related_resources(self) -> typing.List[typing.Dict]:
        related_resources = []
        for child in self._get_children():
            child_resource = {}
            entity = child["entity"]
            if entity == TISSUE_ENTITY:
                child_resource["label"] = "subsample tissue"
                child_resource["relationship"] = "subsample"
                child_resource["target"] = child["bcid"]
                related_resources.append(child_resource)
        return related_resources

    @property
    def child_transformers(self) -> typing.List[GEOMEChildTransformer]:
        return self._child_transformers

    def last_updated_time(self) -> typing.Optional[typing.AnyStr]:
        if self._last_updated_time is not None:
            return self._last_updated_time.strftime(JSON_TIME_FORMAT)
        else:
            return None


class GEOMEChildTransformer(GEOMETransformer):
    """GEOME child record subclass transformer -- uses some fields from the parent and some from the child"""

    def __init__(
        self,
        source_record: typing.Dict,
        child_record: typing.Dict,
        last_updated_time: datetime.datetime,
    ):
        self.source_record = source_record
        self.child_record = child_record
        self._last_updated_time = last_updated_time

    def _id_minus_prefix(self) -> typing.AnyStr:
        return self.child_record["bcid"].removeprefix(self.ARK_PREFIX)

    def sample_label(self) -> typing.AnyStr:
        return self.child_record["tissueID"]

    def sample_identifier_string(self) -> typing.AnyStr:
        return self.child_record["bcid"]

    def sample_description(self) -> typing.AnyStr:
        # TODO
        return ""

    def has_specimen_categories(self) -> typing.List[typing.AnyStr]:
        return ["Organism part"]

    def produced_by_label(self) -> typing.AnyStr:
        return f"tissue subsample from {self._source_record_main_record()['materialSampleID']}"

    def produced_by_description(self) -> typing.AnyStr:
        description_pieces = []
        self._transform_key_to_label(
            "tissueCatalogNumber", self.child_record, description_pieces
        )
        return Transformer.DESCRIPTION_SEPARATOR.join(description_pieces)

    def produced_by_feature_of_interest(self) -> typing.AnyStr:
        return ""

    def produced_by_responsibilities(self) -> typing.List[typing.AnyStr]:
        # TODO: who did the tissue extract, if available -- where does this live, if anywhere?
        return []

    def produced_by_result_time(self) -> typing.AnyStr:
        # TODO: time the tissue extract was done, if available -- where does this live?
        return ""

    def sample_sampling_purpose(self) -> typing.AnyStr:
        return "genomic analysis"

    def curation_location(self) -> typing.AnyStr:
        curation_pieces = []
        tissue_well = self.child_record.get("tissueWell")
        if tissue_well is not None:
            curation_pieces.append(f"tissueWell: {tissue_well}")
        tissue_plate = self.child_record.get("tissuePlate")
        if tissue_plate is not None:
            curation_pieces.append(f"tissuePlate: {tissue_plate}")
        if len(curation_pieces) > 0:
            return ", ".join(curation_pieces)
        return Transformer.NOT_PROVIDED

    def related_resources(self) -> typing.List[typing.Dict]:
        parent_dict = {}
        main_record = self._source_record_main_record()
        parent_dict["label"] = f"parent sample {main_record.get('materialSampleID')}"
        parent_dict["target"] = main_record.get("bcid")
        parent_dict["relationshipType"] = "derived_from"
        return [parent_dict]


# Function to iterate through the identifiers and instantiate the proper GEOME Transformer based on the identifier used for lookup
def geome_transformer_for_identifier(
    identifier: str, source_record: typing.Dict
) -> GEOMETransformer:
    # Two possibilities:
    # (1) It's the sample, so instantiate the main one
    # (2) It's one of the children, so grab the child transformer
    transformer = GEOMETransformer(source_record, None)
    # Sample identifier string for GEOM is the ARK
    if identifier == transformer.sample_identifier_string():
        return transformer
    else:
        for child_transformer in transformer.child_transformers:
            if identifier == child_transformer.sample_identifier_string():
                return child_transformer
    logging.error(
        "Unable to find transformer for identifier %s in GEOME record %s",
        identifier,
        str(source_record),
    )
    return None

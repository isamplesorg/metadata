import typing

from isamples_metadata.Transformer import (
    Transformer,
)


class GEOMETransformer(Transformer):
    """Concrete transformer class for going from a GEOME record to an iSamples record"""

    def transform(self) -> typing.Dict:
        transformed_record = super(GEOMETransformer, self).transform()
        return transformed_record

    ARK_PREFIX = "ark:/"

    def _source_record_main_record(self):
        # The sub-record for the main record, as opposed to the parent or children records
        return self.source_record["record"]

    def _source_record_parent_record(self):
        # The sub-record for the parent record
        return self.source_record["parent"]

    def _id_minus_prefix(self):
        return self._source_record_main_record()["bcid"].removeprefix(self.ARK_PREFIX)

    def id_string(self):
        return f"metadata/{self._id_minus_prefix()}"

    def sample_label(self) -> typing.AnyStr:
        main_record = self._source_record_main_record()
        label_components = []
        scientific_name = main_record.get("scientificName", None)
        if scientific_name is not None:
            label_components.append(scientific_name)
        sample_id = main_record.get("materialSampleID", None)
        if sample_id is not None:
            label_components.append(sample_id)
        return " ".join(label_components)

    def sample_identifier_string(self) -> typing.AnyStr:
        return self._source_record_main_record()["bcid"]

    def sample_identifier_scheme(self) -> typing.AnyStr:
        return "ark"

    def sample_identifier_value(self) -> typing.AnyStr:
        return "/"

    def sample_description(self) -> typing.AnyStr:
        # TODO: implement
        # [concatenate key:value pairs from other content in record/ that is not mapped, e.g.
        # 'voucherCatalogNumber:USNM:Fish:433156'; record/preservative, ]
        return ""

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

    def informal_classification(self) -> typing.AnyStr:
        main_record = self._source_record_main_record()
        informal_classification = main_record.get("scientificName", None)
        if informal_classification is None:
            pieces = []
            genus = main_record.get("genus")
            if genus is not None:
                pieces.append(genus)
            epithet = main_record.get("specificEpithet")
            if epithet is not None:
                pieces.append(epithet)
            informal_classification = " ".join(pieces)
        return informal_classification

    def _place_names(self, only_general: bool):
        parent_record = self._source_record_parent_record()
        if parent_record is not None:
            place_names = []
            if not only_general:
                if "county" in parent_record:
                    place_names.append(parent_record["county"])
                if "locality" in parent_record:
                    place_names.append(parent_record["locality"])
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
        if "order" in self._source_record_main_record():
            keywords.append(self._source_record_main_record()["order"])
        if "phylum" in self._source_record_main_record():
            keywords.append(self._source_record_main_record()["phylum"])
        if "family" in self._source_record_main_record():
            keywords.append(self._source_record_main_record()["family"])
        if "class" in self._source_record_main_record():
            keywords.append(self._source_record_main_record()["class"])
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
            expedition_code = parent_record.get("expeditionCode")
            if expedition_code is not None:
                description_pieces.append(f"expeditionCode: {expedition_code}")
            sampling_protocol = parent_record.get("samplingProtocol")
            if sampling_protocol is not None:
                description_pieces.append(f"samplingProtocol: {sampling_protocol}")
            taxonomy_team = parent_record.get("taxTeam")
            if taxonomy_team is not None:
                description_pieces.append(f"taxonomy team: {taxonomy_team}")
            project_id = parent_record.get("projectId")
            if project_id is not None:
                description_pieces.append(f"projectId: {project_id}")
            return " | ".join(description_pieces)
        return Transformer.NOT_PROVIDED

    def produced_by_feature_of_interest(self) -> typing.AnyStr:
        # TODO: implement
        # "[infer from specimen category, locality; need to so some unique values analysis]"
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
                        responsibilities_pieces.append(f"collector:{collector}")
                elif "|" in collector_list:
                    for collector in collector_list.split("|"):
                        responsibilities_pieces.append(f"collector:{collector}")
                else:
                    responsibilities_pieces.append(f"collector:{collector_list}")
            principal_investigator = parent_record.get("principalInvestigator")
            if principal_investigator is not None:
                responsibilities_pieces.append(
                    f"principalInvestigator:{principal_investigator}"
                )
            identified_by = parent_record.get("identifiedBy")
            if identified_by is not None:
                responsibilities_pieces.append(f"identifiedBy:{identified_by}")
            tax_team = parent_record.get("taxTeam")
            if tax_team is not None:
                responsibilities_pieces.append(f"taxonomy team:{tax_team}")
            entered_by = parent_record.get("eventEnteredBy")
            if entered_by is not None:
                responsibilities_pieces.append(f"event registrant:{entered_by}")
            return responsibilities_pieces
        return []

    def produced_by_result_time(self) -> typing.AnyStr:
        parent_record = self._source_record_parent_record()
        if parent_record is not None:
            result_time_pieces = []
            year = parent_record.get("yearCollected")
            if year is not None:
                result_time_pieces.append(year)
            month = parent_record.get("monthCollected")
            if month is not None:
                month = month.zfill(2)
                result_time_pieces.append(month)
            day = parent_record.get("dayCollected")
            if day is not None:
                day = day.zfill(2)
                result_time_pieces.append(day)
            return "-".join(result_time_pieces)
        return Transformer.NOT_PROVIDED

    def sampling_site_description(self) -> typing.AnyStr:
        parent_record = self._source_record_parent_record()
        if parent_record is not None:
            return parent_record.get("habitat", Transformer.NOT_PROVIDED)
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
            depth = parent_record.get("maximumDepthInMeters", None)
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

    def sampling_site_latitude(self) -> typing.SupportsFloat:
        return self._geo_location_float_value("decimalLatitude")

    def sampling_site_longitude(self) -> typing.SupportsFloat:
        return self._geo_location_float_value("decimalLongitude")

    def sampling_site_place_names(self) -> typing.List:
        return self._place_names(False)

    def sample_registrant(self) -> typing.AnyStr:
        return self._source_record_main_record().get("sampleEnteredBy", Transformer.NOT_PROVIDED)

    def sample_sampling_purpose(self) -> typing.AnyStr:
        # TODO: implement
        return Transformer.NOT_PROVIDED

    # region Curation

    def curation_label(self) -> typing.AnyStr:
        return Transformer.NOT_PROVIDED

    def curation_description(self) -> typing.AnyStr:
        return Transformer.NOT_PROVIDED

    def curation_access_constraints(self) -> typing.AnyStr:
        return Transformer.NOT_PROVIDED

    def curation_location(self) -> typing.AnyStr:
        curation_pieces = []
        tissue_well = self.source_record.get("tissue_well", None)
        if tissue_well is not None:
            curation_pieces.append(f"tissueWell: {tissue_well}")
        tissue_plate = self.source_record.get("tissue_plate", None)
        if tissue_plate is not None:
            curation_pieces.append(f"tissuePlate: {tissue_plate}")
        if len(curation_pieces) > 0:
            return ", ".join(curation_pieces)
        return Transformer.NOT_PROVIDED

    def curation_responsibility(self) -> typing.AnyStr:
        if "institutionCode" in self._source_record_main_record():
            institution_code = self._source_record_main_record()["institutionCode"]
            return f"curator:{institution_code}"
        return Transformer.NOT_PROVIDED

    # endregion

    def related_resources(self) -> typing.List[typing.Dict]:
        if "children" in self.source_record:
            related_resources = []
            children = self.source_record["children"]
            for child in children:
                child_resource = {}
                entity = child["entity"]
                if entity == "Tissue":
                    child_resource["label"] = "subsample tissue"
                    child_resource["relationship"] = "subsample"
                    child_resource["target"] = child["bcid"]
                    related_resources.append(child_resource)
            return related_resources
        return []

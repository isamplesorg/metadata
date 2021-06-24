import typing

from isamples_metadata.Transformer import (
    Transformer,
)


class GEOMETransformer(Transformer):
    """Concrete transformer class for going from a GEOME record to an iSamples record"""

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

    def keywords(self) -> typing.List[typing.AnyStr]:
        # TODO: implement
        # "JSON array of values from record/ -order, -phylum, -family, -class, and parent/ -country, -county,
        # -stateProvince, -continentOcean... (place names more general that the locality or most specific
        # rank place name) "
        return []

    def produced_by_id_string(self) -> typing.AnyStr:
        parent_record = self._source_record_parent_record()
        if parent_record is not None:
            return parent_record["bcid"]
        return Transformer.NOT_PROVIDED

    def produced_by_label(self) -> typing.AnyStr:
        parent_record = self._source_record_parent_record()
        if parent_record is not None:
            label_pieces = []
            event_id = parent_record.get("eventId")
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
                for collector in collector_list.split(", "):
                    responsibilities_pieces.append(f"collector:{collector}")
                for collector in collector_list.split("|"):
                    responsibilities_pieces.append(f"collector:{collector}")
            principal_investigator = parent_record.get("principalInvestigator")
            if principal_investigator is not None:
                responsibilities_pieces.append(f"principalInvestigator:{principal_investigator}")
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
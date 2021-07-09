import typing

from isamples_metadata.Transformer import (
    Transformer,
)

class OpenContextTransformer(Transformer):

    N2T_PREFIX = "https://n2t.net/"
    N2T_ARK_PREFIX = f"{N2T_PREFIX}ark:/"

    def transform(self) -> typing.Dict:
        transformed_record = super().transform()
        return transformed_record

    def _citation_uri(self) -> typing.AnyStr:
        return self.source_record.get("citation uri")

    def id_string(self) -> typing.AnyStr:
        citation_uri = self._citation_uri()
        return f"metadata/{citation_uri.removeprefix(self.N2T_ARK_PREFIX)}"

    def sample_identifier_scheme(self) -> typing.AnyStr:
        pass

    def sample_identifier_string(self) -> typing.AnyStr:
        return self._citation_uri().removeprefix(self.N2T_PREFIX)

    def sample_identifier_value(self) -> typing.AnyStr:
        # TODO is this even used?
        return self._citation_uri().removeprefix(self.N2T_PREFIX)

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
        self._transform_key_to_label(
            "updated", self.source_record, description_pieces
        )
        self._transform_key_to_label(
            "updated", self.source_record, description_pieces
        )
        for consistsOfDict in self.source_record.get("Consists of", []):
            self._transform_key_to_label("label", consistsOfDict, description_pieces, "Consists of")
        for hasTypeDict in self.source_record.get("Has type", []):
            self._transform_key_to_label("label", hasTypeDict, description_pieces, "Has type")
        return Transformer.DESCRIPTION_SEPARATOR.join(description_pieces)

    def sample_registrant(self) -> typing.AnyStr:
        pass

    def sample_sampling_purpose(self) -> typing.AnyStr:
        pass

    def has_context_categories(self) -> typing.List[typing.AnyStr]:
        pass

    def has_material_categories(self) -> typing.List[typing.AnyStr]:
        pass

    def has_specimen_categories(self) -> typing.List[typing.AnyStr]:
        pass

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
        # TODO: maybe this should go under registrant?
        responsibilities = []
        creators = self.source_record.get("Creator")
        if creators is not None:
            for creator in creators:
                responsibilities.append(f"collector: {creator.get('label')}")
        return responsibilities

    def produced_by_result_time(self) -> typing.AnyStr:
        return self.source_record.get("published", Transformer.NOT_PROVIDED)

    def sampling_site_description(self) -> typing.AnyStr:
        Transformer.NOT_PROVIDED

    def sampling_site_label(self) -> typing.AnyStr:
        Transformer.NOT_PROVIDED

    def sampling_site_elevation(self) -> typing.AnyStr:
        Transformer.NOT_PROVIDED

    def sampling_site_latitude(self) -> typing.SupportsFloat:
        return self.source_record.get("latitude", None)

    def sampling_site_longitude(self) -> typing.SupportsFloat:
        return self.source_record.get("longitude", None)

    def sampling_site_place_names(self) -> typing.List:
        return self._context_label_pieces()
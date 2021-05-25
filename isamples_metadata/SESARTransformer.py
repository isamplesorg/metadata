import typing

from isamples_metadata.Transformer import Transformer


class SESARTransformer(Transformer):
    """Concrete transformer class for going from a SESAR record to an iSamples record"""


    def transform(self, source_record: typing.Dict) -> typing.Dict:
        igsn = source_record['igsn']
        transformed_record = super(SESARTransformer, self).transform(source_record)
        return transformed_record


    def sample_identifier_scheme(self, source_record: typing.Dict) -> typing.AnyStr:
        return 'igsn'

    def sample_identifier_value(self, source_record: typing.Dict) -> typing.AnyStr:
        return source_record['igsn']

    def sample_label(self, source_record: typing.Dict) -> typing.AnyStr:
        return source_record['description']['sampleName']

    def description_string(self, source_record: typing.Dict) -> typing.AnyStr:
        return ""

    def has_context_category(self, source_record: typing.Dict) -> typing.List:
        return ['Subsurface fluid reservoir']

    def has_material_category(self, source_record: typing.Dict) -> typing.List:
        return ['Gaseous material']

    def has_specimen_category(self, source_record: typing.Dict) -> typing.List:
        return ['Container with fluid']

    def keywords(self, source_record: typing.Dict) -> typing.List:
        return [source_record['description']['sampleType']]

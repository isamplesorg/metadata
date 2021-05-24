import typing

from isamples_metadata.Transformer import Transformer


class SESARTransformer(Transformer):
    """Concrete transformer class for going from a SESAR record to an iSamples record"""

    def transform(self, source_record: typing.Dict) -> typing.Dict:
        return source_record

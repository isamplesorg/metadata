from abc import ABC, abstractmethod
import typing


class Transformer(ABC):
    """Abstract base class for various iSamples provider transformers"""

    @abstractmethod
    def transform(self, source_record: typing.Dict) -> typing.Dict:
        """Do the actual work of transforming a provider record into an iSamples record.

        Arguments:
            source_record -- The provider record to be transformed
        Return value:
            The provider record transformed into an iSamples record
        """
        transformed_record = {'$schema': '../iSamplesSchemaBasicSMR.json',
                              '@id': 'https://data.isamples.org/digitalsample/{0}/{1}'.format(self.sample_identifier_scheme(source_record), self.sample_identifier_value(source_record)),
                              'label': self.sample_label(source_record),
                              'sampleidentifier': '{0}:{1}'.format(self.sample_identifier_scheme(source_record), self.sample_identifier_value(source_record)),
                              'description': self.description_string(source_record),
                              'hasContextCategory': self.has_context_category(source_record),
                              'hasMaterialCategory': self.has_material_category(source_record),
                              'hasSpecimenCategory': self.has_specimen_category(source_record),
                              'keywords': self.keywords(source_record)}
        return transformed_record

    @abstractmethod
    def sample_identifier_scheme(self, source_record: typing.Dict) -> typing.AnyStr:
        """The identifier scheme for the sample in source_record"""
        pass

    @abstractmethod
    def sample_identifier_value(self, source_record: typing.Dict) -> typing.AnyStr:
        """An identifier value for the sample in source_record, this doesn't include the identifier scheme"""
        pass

    @abstractmethod
    def sample_label(self, source_record: typing.Dict) -> typing.AnyStr:
        """A label for the sample in source_record"""
        pass

    @abstractmethod
    def description_string(self, source_record: typing.Dict) -> typing.AnyStr:
        """A textual description of the sample in source_record"""
        pass

    @abstractmethod
    def has_context_category(self, source_record: typing.Dict) -> typing.List:
        """Map from the source record into an iSamples context category"""
        pass

    @abstractmethod
    def has_material_category(self, source_record: typing.Dict) -> typing.List:
        """Map from the source record into an iSamples material category"""
        pass

    @abstractmethod
    def has_specimen_category(self, source_record: typing.Dict) -> typing.List:
        """Map from the source record into an iSamples specimen category"""
        pass

    @abstractmethod
    def keywords(self, source_record: typing.Dict) -> typing.List:
        """The keywords for the sample in source record"""
        pass

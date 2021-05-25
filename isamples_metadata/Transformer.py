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
                              'description': self.sample_description(source_record),
                              'hasContextCategory': self.has_context_categories(source_record),
                              'hasMaterialCategory': self.has_material_categories(source_record),
                              'hasSpecimenCategory': self.has_specimen_categories(source_record),
                              'keywords': self.keywords(source_record),
                              'producedBy': {
                                  'label': self.produced_by_label(source_record),
                                  'description': self.produced_by_description(source_record),
                                  'hasFeatureOfInterest': self.produced_by_feature_of_interest(source_record),
                                  'responsibility': self.produced_by_responsibilities(source_record),
                                  'resultTime': self.produced_by_result_time(source_record),
                                  'samplingSite': {
                                      'description': self.sampling_site_description(source_record),
                                      'label': self.sampling_site_label(source_record),
                                      'location': {
                                          'elevation': self.sampling_site_elevation(source_record),
                                          'latitude': self.sampling_site_latitude(source_record),
                                          'longitude': self.sampling_site_longitude(source_record)
                                      },
                                      'placeName': self.sampling_site_place_names(source_record)
                                  }
                              },
                              'registrant': self.sample_registrant(source_record),
                              'samplingPurpose': self.sample_sampling_purpose(source_record)
                              }
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
    def sample_description(self, source_record: typing.Dict) -> typing.AnyStr:
        """A textual description of the sample in source_record"""
        pass

    @abstractmethod
    def sample_registrant(self, source_record: typing.Dict) -> typing.AnyStr:
        """The name of the sample registrant in source_record"""
        pass

    @abstractmethod
    def sample_sampling_purpose(self, source_record: typing.Dict) -> typing.AnyStr:
        """The samplingPurpose of the sample registrant in source_record"""
        pass

    @abstractmethod
    def has_context_categories(self, source_record: typing.Dict) -> typing.List:
        """Map from the source record into an iSamples context category"""
        pass

    @abstractmethod
    def has_material_categories(self, source_record: typing.Dict) -> typing.List:
        """Map from the source record into an iSamples material category"""
        pass

    @abstractmethod
    def has_specimen_categories(self, source_record: typing.Dict) -> typing.List:
        """Map from the source record into an iSamples specimen category"""
        pass

    @abstractmethod
    def keywords(self, source_record: typing.Dict) -> typing.List:
        """The keywords for the sample in source record"""
        pass

    @abstractmethod
    def produced_by_label(self, source_record: typing.Dict) -> typing.AnyStr:
        """The label for the producedBy dictionary"""
        pass

    @abstractmethod
    def produced_by_description(self, source_record: typing.Dict) -> typing.AnyStr:
        """The description for the producedBy dictionary"""
        pass

    @abstractmethod
    def produced_by_feature_of_interest(self, source_record: typing.Dict) -> typing.AnyStr:
        """The feature of interest for the producedBy dictionary"""
        pass

    @abstractmethod
    def produced_by_responsibilities(self, source_record: typing.Dict) -> typing.List:
        """The responsibility list for the producedBy dictionary"""
        pass

    @abstractmethod
    def produced_by_result_time(self, source_record: typing.Dict) -> typing.AnyStr:
        """The result time for the producedBy dictionary"""
        pass

    @abstractmethod
    def sampling_site_description(self, source_record: typing.Dict) -> typing.AnyStr:
        """The sampling site description"""
        pass

    @abstractmethod
    def sampling_site_label(self, source_record: typing.Dict) -> typing.AnyStr:
        """The sampling site label"""
        pass

    @abstractmethod
    def sampling_site_elevation(self, source_record: typing.Dict) -> typing.AnyStr:
        """The sampling site elevation"""
        pass

    @abstractmethod
    def sampling_site_latitude(self, source_record: typing.Dict) -> typing.SupportsFloat:
        """The sampling site latitude"""
        pass

    @abstractmethod
    def sampling_site_longitude(self, source_record: typing.Dict) -> typing.SupportsFloat:
        """The sampling site longitude"""
        pass

    @abstractmethod
    def sampling_site_place_names(self, source_record: typing.Dict) -> typing.List:
        """The sampling site longitude"""
        pass

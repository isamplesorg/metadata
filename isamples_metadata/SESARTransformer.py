import typing
import logging
from isamples_metadata.Transformer import Transformer


class SESARTransformer(Transformer):
    """Concrete transformer class for going from a SESAR record to an iSamples record"""


    def transform(self, source_record: typing.Dict) -> typing.Dict:
        transformed_record = super(SESARTransformer, self).transform(source_record)
        return transformed_record

    def _source_record_description(self, source_record: typing.Dict) -> typing.Dict:
        return source_record['description']

    def _supplement_metadata(self, source_record: typing.Dict) -> typing.Dict:
        description = self._source_record_description(source_record)
        if description is not None:
            return self._source_record_description(source_record)['supplementMetadata']
        return None
    
    def _logger(self):
        return logging.getLogger('isamples_metadata.SESARTransformer')

    def sample_identifier_scheme(self, source_record: typing.Dict) -> typing.AnyStr:
        return 'igsn'

    def sample_identifier_value(self, source_record: typing.Dict) -> typing.AnyStr:
        return source_record['igsn']

    def sample_label(self, source_record: typing.Dict) -> typing.AnyStr:
        return self._source_record_description(source_record)['sampleName']

    def sample_description(self, source_record: typing.Dict) -> typing.AnyStr:
        # TODO: implement
        return ""

    def has_context_categories(self, source_record: typing.Dict) -> typing.List:
        return ['Subsurface fluid reservoir']

    def has_material_categories(self, source_record: typing.Dict) -> typing.List:
        return ['Gaseous material']

    def has_specimen_categories(self, source_record: typing.Dict) -> typing.List:
        return ['Container with fluid']

    def keywords(self, source_record: typing.Dict) -> typing.List:
        return [self._source_record_description(source_record)['sampleType']]

    def _contributor_name_with_role(self, source_record: typing.Dict, role_name: typing.AnyStr):
        contributor_name = ""
        contributors = self._source_record_description(source_record)['contributors']
        if contributors is not None and len(contributors) > 0:
            role_lambda = lambda contributor_dict: contributor_dict['roleName'] == role_name
            contributors_with_role = list(filter(role_lambda, contributors))
            if len(contributors_with_role) > 0:
                contributor_name = contributors_with_role[0]['contributor'][0]['name']
        return contributor_name

    def sample_registrant(self, source_record: typing.Dict) -> typing.AnyStr:
        return self._contributor_name_with_role(source_record, 'Sample Registrant')

    def sample_sampling_purpose(self, source_record: typing.Dict) -> typing.AnyStr:
        # TODO: implement
        return ""

    def produced_by_label(self, source_record: typing.Dict) -> typing.AnyStr:
        return self._source_record_description(source_record)['collectionMethod']

    def produced_by_description(self, source_record: typing.Dict) -> typing.AnyStr:
        description_str = ''
        description_dict = self._source_record_description(source_record)
        if description_dict is not None:
            supplement_metadata = self._supplement_metadata(source_record)
            if supplement_metadata is not None:
                if 'cruiseFieldPrgrm' in supplement_metadata:
                    description_str += 'cruiseFieldPrgrm:{0}. '.format(supplement_metadata['cruiseFieldPrgrm'])
                if 'launchPlatformName' in supplement_metadata:
                    description_str += 'launchPlatformName:{0}. '.format(supplement_metadata['launchPlatformName'])

            if 'collectionMethod' in description_dict:
                description_str += '{0}. '.format(description_dict['collectionMethod'])
            if 'description' in description_dict:
                description_str += '{0}. '.format(description_dict['description'])

            if supplement_metadata is not None:
                if 'launchTypeName' in supplement_metadata:
                    description_str += 'launch type:{0}, '.format(supplement_metadata['launchTypeName'])
                if 'navigationType' in supplement_metadata:
                    description_str += 'navigation type:{0}'.format(supplement_metadata['navigationType'])
        return description_str

    def produced_by_feature_of_interest(self, source_record: typing.Dict) -> typing.AnyStr:
        supplement_metadata = self._supplement_metadata(source_record)
        if supplement_metadata is not None and 'primaryLocationType' in supplement_metadata:
            return supplement_metadata['primaryLocationType']
        return ""

    def produced_by_responsibilities(self, source_record: typing.Dict) -> typing.List:
        responsibilities = list()
        description_dict = self._source_record_description(source_record)
        collector = description_dict['collector']
        if collector is not None:
            responsibilities.append('{},,Collector'.format(collector))

        owner = self._contributor_name_with_role(source_record, 'Sample Owner')
        if len(owner) > 0:
            responsibilities.append('{},,Sample Owner'.format(owner))

        return responsibilities

    def produced_by_result_time(self, source_record: typing.Dict) -> typing.AnyStr:
        return self._source_record_description(source_record)['collectionStartDate']

    def sampling_site_description(self, source_record: typing.Dict) -> typing.AnyStr:
        description_dict = self._source_record_description(source_record)
        if description_dict is not None:
            supplement_metadata = self._supplement_metadata(source_record)
            if supplement_metadata is not None and 'locationDescription' in supplement_metadata:
                return supplement_metadata['locationDescription']
        return ""

    def sampling_site_label(self, source_record: typing.Dict) -> typing.AnyStr:
        # TODO: implement
        return ""

    def sampling_site_elevation(self, source_record: typing.Dict) -> typing.AnyStr:
        supplement_metadata = self._supplement_metadata(source_record)
        if supplement_metadata is not None and 'elevation' in supplement_metadata:
            elevation_value = supplement_metadata['elevation']
            elevation_unit = supplement_metadata['elevationUnit']
            elevation_unit_abbreviation = ""
            if elevation_unit is not None:
                if elevation_unit == 'meters':
                    elevation_unit_abbreviation = 'm'
                else:
                    self._logger().error('Received elevation in unexpected unit: ', elevation_unit)
            elevation_str = str(elevation_value)
            if len(elevation_unit_abbreviation) > 0:
                elevation_str += ' ' + elevation_unit_abbreviation
            return elevation_str
        return ""

    def _geo_location_float_value(self, source_record: typing.Dict, key_name: typing.AnyStr):
        geo_location = self._source_record_description(source_record)['geoLocation']
        if geo_location is not None:
            string_val = geo_location['geo'][0][key_name]
            if string_val is not None:
                return float(string_val)
        return 0.0

    def sampling_site_latitude(self, source_record: typing.Dict) -> typing.SupportsFloat:
        return self._geo_location_float_value(source_record, 'latitude')

    def sampling_site_longitude(self, source_record: typing.Dict) -> typing.SupportsFloat:
        return self._geo_location_float_value(source_record, 'longitude')

    def sampling_site_place_names(self, source_record: typing.Dict) -> typing.List:
        return [self._supplement_metadata(source_record)['primaryLocationName']]


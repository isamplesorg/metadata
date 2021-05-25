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
        return [source_record['description']['sampleType']]

    def sample_registrant(self, source_record: typing.Dict) -> typing.AnyStr:
        contributors = source_record['description']['contributors']
        registrants = list(filter(lambda contributor_dict: contributor_dict['roleName'] == 'Sample Registrant', contributors))
        if len(registrants) > 0:
            return registrants[0]['contributor'][0]['name']
        else:
            return ""

    def sample_sampling_purpose(self, source_record: typing.Dict) -> typing.AnyStr:
        # TODO: implement
        return ""

    def produced_by_label(self, source_record: typing.Dict) -> typing.AnyStr:
        return source_record['description']['collectionMethod']

    def produced_by_description(self, source_record: typing.Dict) -> typing.AnyStr:
        description_str = ''
        description_dict = source_record['description']
        if description_dict != None:
            supplement_metadata = description_dict['supplementMetadata']
            if supplement_metadata != None:
                if 'cruiseFieldPrgrm' in supplement_metadata:
                    description_str += 'cruiseFieldPrgrm:{0}. '.format(supplement_metadata['cruiseFieldPrgrm'])
                if 'launchPlatformName' in supplement_metadata:
                    description_str += 'launchPlatformName:{0}. '.format(supplement_metadata['launchPlatformName'])

            if 'collectionMethod' in description_dict:
                description_str += '{0}. '.format(description_dict['collectionMethod'])
            if 'description' in description_dict:
                description_str += '{0}. '.format(description_dict['description'])

            if supplement_metadata != None:
                if 'launchTypeName' in supplement_metadata:
                    description_str += 'launch type:{0}, '.format(supplement_metadata['launchTypeName'])
                if 'navigationType' in supplement_metadata:
                    description_str += 'navigation type:{0}'.format(supplement_metadata['navigationType'])
        return description_str

    def produced_by_feature_of_interest(self, source_record: typing.Dict) -> typing.AnyStr:
        description_dict = source_record['description']
        if description_dict != None:
            supplement_metadata = description_dict['supplementMetadata']
            if supplement_metadata != None and 'primaryLocationType' in supplement_metadata:
                return supplement_metadata['primaryLocationType']
        return ""

    def produced_by_responsibilities(self, source_record: typing.Dict) -> typing.List:
        # TODO: implement
        return []

    def produced_by_result_time(self, source_record: typing.Dict) -> typing.AnyStr:
        # TODO: implement
        return ""

    def sampling_site_description(self, source_record: typing.Dict) -> typing.AnyStr:
        # TODO: implement
        return ""

    def sampling_site_label(self, source_record: typing.Dict) -> typing.AnyStr:
        # TODO: implement
        return ""

    def sampling_site_elevation(self, source_record: typing.Dict) -> typing.AnyStr:
        # TODO: implement
        return ""

    def sampling_site_latitude(self, source_record: typing.Dict) -> typing.SupportsFloat:
        # TODO: implement
        return 0.0

    def sampling_site_longitude(self, source_record: typing.Dict) -> typing.SupportsFloat:
        # TODO: implement
        return 0.0

    def sampling_site_place_names(self, source_record: typing.Dict) -> typing.List:
        # TODO: implement
        return []


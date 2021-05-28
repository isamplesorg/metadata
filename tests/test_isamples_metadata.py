import json

import pytest

from isamples_metadata.SESARTransformer import SESARTransformer

SESAR_test_values = [
    ('../examples/SESAR/raw/EOI00002Hjson-ld.json', '../examples/SESAR/test/iSamplesEOI00002HBasic.json'),
    ('../examples/SESAR/raw/IEEJR000Mjson-ld.json', '../examples/SESAR/test/iSamplesIEEJR000MBasic.json')
]


@pytest.mark.parametrize("sesar_source_path,isamples_path", SESAR_test_values)
def test_dicts_equal(sesar_source_path, isamples_path):
    with open(sesar_source_path) as sesar_source_file:
        sesar_record = json.load(sesar_source_file)
        transformer = SESARTransformer(sesar_record)
        transformed_to_isamples_record = transformer.transform()
        with open(isamples_path) as isamples_file:
            isamples_record = json.load(isamples_file)
            assert transformed_to_isamples_record == isamples_record

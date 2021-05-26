import json

import pytest

from isamples_metadata.SESARTransformer import SESARTransformer

SESAR_test_values = [
    ('../examples/SESAR/raw/EOI00002Hjson-ld.json', '../examples/SESAR/test/iSamplesEOI00002HBasic.json'),
    ('../examples/SESAR/raw/IEEJR000Mjson-ld.json', '../examples/SESAR/test/iSamplesIEEJR000MBasic.json')
]

@pytest.mark.parametrize("SESAR_source_path,iSamples_path", SESAR_test_values)
def test_dicts_equal(SESAR_source_path, iSamples_path):
    with open(SESAR_source_path) as SESAR_source_file:
        SESAR_record = json.load(SESAR_source_file)
        transformer = SESARTransformer(SESAR_record)
        transformed_to_iSamples_record = transformer.transform()
        with open(iSamples_path) as iSamples_file:
            iSamples_record = json.load(iSamples_file)
            assert transformed_to_iSamples_record == iSamples_record

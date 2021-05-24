import pytest
import json
import isamples_metadata
from isamples_metadata import __version__
from isamples_metadata.SESARTransformer import SESARTransformer


def test_version():
    assert __version__ == '0.1.0'
    print("Test passed")

def test_dicts_equal():
    transformer = SESARTransformer()
    with open('../examples/SESAR/raw/EOI00002Hjson-ld.json') as SESAR_source_file:
        SESAR_record = json.load(SESAR_source_file)
        transformed_to_iSamples_record = transformer.transform(SESAR_record)
        with open('../examples/SESAR/test/iSamplesEOI00002HBasic.json') as iSamples_file:
            iSamples_record = json.load(iSamples_file)
            assert iSamples_record == transformed_to_iSamples_record
    print("Done running.")

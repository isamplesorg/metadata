import json

import pytest

from isamples_metadata.SESARTransformer import SESARTransformer
from isamples_metadata.GEOMETransformer import GEOMETransformer


def _run_transformer(isamples_path, source_path, transformer_class):
    with open(source_path) as source_file:
        source_record = json.load(source_file)
        transformer = transformer_class(source_record)
        transformed_to_isamples_record = transformer.transform()
        with open(isamples_path) as isamples_file:
            isamples_record = json.load(isamples_file)
            assert transformed_to_isamples_record == isamples_record


SESAR_test_values = [
    (
        "../examples/SESAR/raw/EOI00002Hjson-ld.json",
        "../examples/SESAR/test/iSamplesEOI00002HBasic.json",
    ),
    (
        "../examples/SESAR/raw/IEEJR000Mjson-ld.json",
        "../examples/SESAR/test/iSamplesIEEJR000MBasic.json",
    ),
]


@pytest.mark.parametrize("sesar_source_path,isamples_path", SESAR_test_values)
def test_dicts_equal(sesar_source_path, isamples_path):
    _run_transformer(isamples_path, sesar_source_path, SESARTransformer)


GEOME_test_values = [
    (
        "../examples/GEOME/raw/ark-21547-Car2PIRE_0334.json",
        "../examples/GEOME/test/ark-21547-Car2PIRE_0334-test.json",
    ),
    (
        "../examples/GEOME/raw/ark-21547-CgZ2PEER_7055.json",
        "../examples/GEOME/test/ark-21547-CgZ2PEER_7055-test.json",
    ),
    (
        "../examples/GEOME/raw/ark-21547-DRW2LACM-DISCO-16924.json",
        "../examples/GEOME/test/ark-21547-DRW2LACM-DISCO-16924-test.json",
    ),
]


@pytest.mark.parametrize("geome_source_path,isamples_path", GEOME_test_values)
def test_geome_dicts_equal(geome_source_path, isamples_path):
    _run_transformer(isamples_path, geome_source_path, GEOMETransformer)

import json
import csv
import pytest
import typing
import re

from isamples_metadata.SESARTransformer import SESARTransformer
from isamples_metadata.GEOMETransformer import GEOMETransformer
from isamples_metadata.OpenContextTransformer import OpenContextTransformer
from isamples_metadata.SmithsonianTransformer import SmithsonianTransformer


def _run_transformer(isamples_path, source_path, transformer_class):
    with open(source_path) as source_file:
        source_record = json.load(source_file)
        transformer = transformer_class(source_record)
        transformed_to_isamples_record = transformer.transform()
        _assert_transformed_dictionary(isamples_path, transformed_to_isamples_record)


def _assert_transformed_dictionary(isamples_path, transformed_to_isamples_record):
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


GEOME_child_test_values = [
    (
        "../examples/GEOME/raw/ark-21547-Car2PIRE_0334.json",
        "../examples/GEOME/test/ark-21547-Car2PIRE_0334-child-test.json",
    )
]


@pytest.mark.parametrize("geome_source_path,isamples_path", GEOME_child_test_values)
def test_geome_child_dicts_equal(geome_source_path, isamples_path):
    with open(geome_source_path) as source_file:
        source_record = json.load(source_file)
        transformer = GEOMETransformer(source_record)
        child_transformer = transformer.child_transformers[0]
        transformed_to_isamples_record = child_transformer.transform()
        _assert_transformed_dictionary(isamples_path, transformed_to_isamples_record)


OPENCONTEXT_test_values = [
    (
        "../examples/OpenContext/raw/ark-28722-k2b570022.json",
        "../examples/OpenContext/test/ark-28722-k2b570022-test.json",
    ),
    (
        "../examples/OpenContext/raw/ark-28722-k2m61xj9b.json",
        "../examples/OpenContext/test/ark-28722-k2m61xj9b-test.json"
    ),
    (
        "../examples/OpenContext/raw/ark-28722-k2qj7np9g.json",
        "../examples/OpenContext/test/ark-28722-k2m61xj9b-test.json"
    )
]


@pytest.mark.parametrize(
    "open_context_source_path,isamples_path", OPENCONTEXT_test_values
)
def test_open_context_dicts_equal(open_context_source_path, isamples_path):
    _run_transformer(isamples_path, open_context_source_path, OpenContextTransformer)


def _get_record_with_id(record_id: typing.AnyStr) -> typing.Dict:
    raw_csv = "../examples/smithonsonian/DwC raw/DwC_occurrence_10.csv"
    with open(raw_csv, newline="") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t")
        column_headers = []
        i = 0
        for i, current_values in enumerate(csv_reader):
            if i == 0:
                column_headers = current_values
                continue
            # Otherwise iterate over the keys and make source JSON
            current_record = {}
            for index, key in enumerate(column_headers):
                if key == "id":
                    if record_id not in current_values[index]:
                        current_record = None
                        break
                if len(key) > 0:
                    current_record[key] = current_values[index]
            if current_record is not None:
                return current_record
        print("Error, didn't find record with id: %s", record_id)
    return {}

SMITHSONIAN_test_values = [
    "../examples/smithonsonian/DwC test/ark-65665-30000cb27-702b-4d34-ac24-3e46e14d5519-test.json",
    "../examples/smithonsonian/DwC test/ark-65665-30000d403-f44f-498c-b7e3-ca1df52a2391-test.json",
    "../examples/smithonsonian/DwC test/ark-65665-30002e5e4-91a3-4343-9519-2aab489dfbfd-test.json",
    "../examples/smithonsonian/DwC test/ark-65665-30003a155-444f-4add-9ec0-48bd2631237e-test.json",
    "../examples/smithonsonian/DwC test/ark-65665-30004d383-9b25-4cfd-840d-a720361ec77e-test.json"
]

@pytest.mark.parametrize(
    "isamples_path", SMITHSONIAN_test_values
)
def test_smithsonian_dicts_equal(isamples_path):
    id_piece = re.search(r"-([^-]+)-test", isamples_path).group(1)
    source_dict = _get_record_with_id(id_piece)
    # create the transformer from the specified row in the source .csv
    transformer = SmithsonianTransformer(source_dict)
    transformed_to_isamples_record = transformer.transform()
    _assert_transformed_dictionary(isamples_path, transformed_to_isamples_record)
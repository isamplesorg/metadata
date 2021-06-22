import pytest

from isamples_metadata.SESARTransformer import SESARTransformer


@pytest.fixture
def sesar_transformer():
    return SESARTransformer({})


def test_elevation_in_meters(sesar_transformer):
    elevation_str = sesar_transformer.elevation_str(12345, "meters")
    assert elevation_str == "12345 m"


def test_elevation_in_meters_capitalized(sesar_transformer):
    elevation_str = sesar_transformer.elevation_str(12345, "Meters ")
    assert elevation_str == "12345 m"


def test_elevation_in_feet(sesar_transformer):
    elevation_str = sesar_transformer.elevation_str(3.28084, "feet")
    assert elevation_str == "1.0 m"


def test_elevation_in_feet_capitalized(sesar_transformer):
    elevation_str = sesar_transformer.elevation_str(3.28084, "Feet ")
    assert elevation_str == "1.0 m"

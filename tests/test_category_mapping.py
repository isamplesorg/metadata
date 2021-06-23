import pytest

from isamples_metadata.Transformer import (
    StringPairedCategoryMapper,
    StringOrderedCategoryMapper,
    StringEndsWithCategoryMapper,
)

@pytest.fixture
def soil_mapper():
    endsWithSoilMapper = StringEndsWithCategoryMapper(
        "Soil", "Subaerial surface environment"
    )
    soilFloodplainMapper = StringPairedCategoryMapper(
        "Microbiology>Soil", "floodplain", "Subaerial terrestrial biome"
    )
    soilMapper = StringOrderedCategoryMapper(
        # Order matters here, the generic one needs to be last
        [soilFloodplainMapper, endsWithSoilMapper]
    )
    return soilMapper

def test_compound_categories(soil_mapper):
    # For the case of the specific pair, we should get the specific match
    categories = []
    soil_mapper.append_if_matched("Microbiology>Soil", "floodplain", categories)
    assert categories[0] == "Subaerial terrestrial biome"

def test_plain_soil(soil_mapper):
    # location doesn't match the specific one we care about, get generic
    categories = []
    soil_mapper.append_if_matched("Soil", "boreal forest", categories)
    assert categories[0] == "Subaerial surface environment"

def test_ends_with_soil(soil_mapper):
    # no location, get generic
    categories = []
    soil_mapper.append_if_matched("Metamorphic>Soil", "", categories)
    assert categories[0] == "Subaerial surface environment"

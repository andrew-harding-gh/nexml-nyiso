import pytest

from nexml_nyiso import utility


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (0/8, "CLR"),
        (2/8, "FEW"),
        (8/8, "OVC"),
        (5.5/8, "BKN")
    ]
)
def test_convert_cld_cover(test_input, expected):
    assert utility.convert_cld_cover(test_input) == expected


@pytest.mark.parametrize(
    "in_temp, in_wspd, expected",
    [
        (0, 50, -31),
        (50, 10, 46),
        (-10, 0, -10)
    ]
)
def test_calc_wind_chill(in_temp, in_wspd, expected):
    assert utility.calc_wind_chill(in_temp, in_wspd) == expected


@pytest.mark.parametrize(
    "in_temp, in_rh, expected",
    [
        (100, 50, 118),
        (80, 0, 78),
        (60, 10, 56)
    ]
)
def test_calc_heat_index(in_temp, in_rh, expected):
    assert utility.calc_heat_index(in_temp, in_rh) == expected



import pytest

from water import ocean as mod

CASES = [
    ('normalize_spectrum', [[1, 1, 2]], [0.25, 0.25, 0.5], True),
    ('normalize_spectrum', [[0, 0, 0]], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333], True),
    ('dispersion_wavelength', [8], 99.92383947081558, True),
    ('dispersion_wavelength', [4], 24.980959867703895, True),
    ('align_lod_seam', [[1, 2], [4, 8]], ([1, 3.0], [3.0, 8]), False),
    ('foam_amount', [0.5, 2.0, 1.0], 0.0, True),
    ('foam_amount', [1.0, 2.0, 1.0], 1.0, True),
    ('wave_normal', [[0, 1, 2], 1], [1.0, 1.0, 0.0], True),
    ('reflect_direction', [[1, -1, 0], [0, 1, 0]], [1.0, 1.0, 0.0], True),
    ('depth_fog', [10, 0.1], 0.6321205588285577, True),
    ('caustic_falloff', [2, 0.5], 0.5, True),
    ('buoyancy_samples', [10, 2], 6, False),
    ('commit_chunks', [[True, True]], True, False),
    ('foam_amount', [0.2, 1.0, 1.0], 0.0, True),
    ('dispersion_wavelength', [6], 56.207159702333755, True),
]


@pytest.mark.parametrize("func_name,args,expected,approx", CASES)
def test_ocean_contract(func_name, args, expected, approx):
    func = getattr(mod, func_name)
    result = func(*args)
    if approx:
        assert result == pytest.approx(expected)
    else:
        assert result == expected

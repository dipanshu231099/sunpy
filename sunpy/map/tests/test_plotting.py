"""
Test Generic Map
"""
import os

import matplotlib.pyplot as plt
import numpy as np
import pytest

import astropy.units as u
from astropy.coordinates import SkyCoord

import sunpy
import sunpy.coordinates
import sunpy.data.test
import sunpy.map
from sunpy.coordinates.utils import get_rectangle_coordinates
from sunpy.tests.helpers import figure_test
from sunpy.util.exceptions import SunpyUserWarning

testpath = sunpy.data.test.rootdir
pytestmark = pytest.mark.filterwarnings('ignore:Missing metadata')


@pytest.fixture
def aia171_test_map():
    return sunpy.map.Map(os.path.join(testpath, 'aia_171_level1.fits'))


@pytest.fixture
def heliographic_test_map():
    return sunpy.map.Map(os.path.join(testpath, 'heliographic_phase_map.fits.gz'))


@pytest.fixture
def aia171_test_map_with_mask(aia171_test_map):
    shape = aia171_test_map.data.shape
    mask = np.zeros_like(aia171_test_map.data, dtype=bool)
    mask[0:shape[0] // 2, 0:shape[1] // 2] = True
    return sunpy.map.Map(np.ma.array(
        aia171_test_map.data, mask=mask),
        aia171_test_map.meta)


@figure_test
def test_plot_aia171(aia171_test_map):
    aia171_test_map.plot()


@figure_test
def test_plot_aia171_clip(aia171_test_map):
    aia171_test_map.plot(clip_interval=(5., 99.)*u.percent)


@figure_test
def test_peek_aia171(aia171_test_map):
    aia171_test_map.peek()


@figure_test
def test_peek_grid_aia171(aia171_test_map):
    aia171_test_map.peek(draw_grid=True)


@figure_test
def test_peek_grid_spacing_aia171(aia171_test_map):
    aia171_test_map.peek(draw_grid=(5, 5) * u.deg)


@figure_test
def test_peek_limb_aia171(aia171_test_map):
    aia171_test_map.peek(draw_limb=True)


@figure_test
def test_draw_grid_aia171(aia171_test_map):
    aia171_test_map.plot()
    aia171_test_map.draw_grid(grid_spacing=(30, 40) * u.deg)


@figure_test
def test_peek_grid_limb_aia171(aia171_test_map):
    aia171_test_map.peek(draw_grid=True, draw_limb=True)


@figure_test
def test_plot_aia171_nowcsaxes(aia171_test_map):
    ax = plt.gca()
    with pytest.warns(SunpyUserWarning, match='WCSAxes not being used as the axes'):
        aia171_test_map.plot(axes=ax)


@figure_test
def test_rectangle_aia171_width_height(aia171_test_map):
    aia171_test_map.plot()
    bottom_left = SkyCoord(
        0 * u.arcsec, 0 * u.arcsec, frame=aia171_test_map.coordinate_frame)
    w = 100 * u.arcsec
    h = 100 * u.arcsec
    aia171_test_map.draw_rectangle(bottom_left, width=w, height=h)


@figure_test
def test_rectangle_aia171_top_right(aia171_test_map):
    aia171_test_map.plot()
    bottom_left = SkyCoord(
        0 * u.arcsec, 0 * u.arcsec, frame=aia171_test_map.coordinate_frame)
    w = 100 * u.arcsec
    h = 100 * u.arcsec
    bottom_left, top_right = get_rectangle_coordinates(bottom_left, width=w, height=h)
    aia171_test_map.draw_rectangle(bottom_left, top_right=top_right)


@figure_test
def test_plot_masked_aia171(aia171_test_map_with_mask):
    aia171_test_map_with_mask.plot()


@figure_test
def test_plot_masked_aia171_nowcsaxes(aia171_test_map_with_mask):
    ax = plt.gca()
    with pytest.warns(SunpyUserWarning, match='WCSAxes not being used as the axes'):
        aia171_test_map_with_mask.plot(axes=ax)


@figure_test
def test_plot_aia171_superpixel(aia171_test_map):
    aia171_test_map.superpixel((9, 7) * u.pix, offset=(4, 4) * u.pix).plot()


@figure_test
def test_plot_aia171_superpixel_nowcsaxes(aia171_test_map):
    ax = plt.gca()
    with pytest.warns(SunpyUserWarning, match='WCSAxes not being used as the axes'):
        aia171_test_map.superpixel(
            (9, 7) * u.pix, offset=(4, 4) * u.pix).plot(axes=ax)


@figure_test
def test_plot_masked_aia171_superpixel(aia171_test_map_with_mask):
    aia171_test_map_with_mask.superpixel(
        (9, 7) * u.pix, offset=(4, 4) * u.pix).plot()


@figure_test
def test_plot_masked_aia171_superpixel_nowcsaxes(aia171_test_map_with_mask):
    ax = plt.gca()
    with pytest.warns(SunpyUserWarning, match='WCSAxes not being used as the axes'):
        aia171_test_map_with_mask.superpixel(
            (9, 7) * u.pix, offset=(4, 4) * u.pix).plot(axes=ax)


@figure_test
def test_draw_contours_aia(aia171_test_map):
    aia171_test_map.plot()
    aia171_test_map.draw_contours(u.Quantity(np.arange(1, 100, 10), 'percent'))


@figure_test
def test_heliographic_peek(heliographic_test_map):
    heliographic_test_map.peek()


@figure_test
def test_heliographic_rectangle_width_height(heliographic_test_map):
    heliographic_test_map.plot()
    bottom_left = SkyCoord(
        60 * u.deg, 50 * u.deg, frame=heliographic_test_map.coordinate_frame)
    w = 13 * u.deg
    h = 13 * u.deg
    heliographic_test_map.draw_rectangle(bottom_left, width=w, height=h, color='cyan')


@figure_test
def test_heliographic_rectangle_top_right(heliographic_test_map):
    heliographic_test_map.plot()
    bottom_left = SkyCoord(
        60 * u.deg, 50 * u.deg, frame=heliographic_test_map.coordinate_frame)
    w = 13 * u.deg
    h = 13 * u.deg
    bottom_left, top_right = get_rectangle_coordinates(bottom_left, width=w, height=h)
    heliographic_test_map.draw_rectangle(bottom_left, width=w, height=h, color='cyan')


@figure_test
def test_heliographic_grid_annotations(heliographic_test_map):
    heliographic_test_map.plot()
    heliographic_test_map.draw_grid(annotate=False)

import os
import pandas
import pytest
import pygeneactiv
import simplejson as json

__DIR__ = os.path.dirname(__file__)

def test_headers():
    geneactiv_file = os.path.join(__DIR__, 'right_wrist.csv')
    headers_file = os.path.join(__DIR__, 'headers.json')
    ds = pygeneactiv.read(geneactiv_file)
    # squash nans in dataset headers
    headers = json.loads(json.dumps(ds.headers, ignore_nan=True))
    # load cached headers
    with open(headers_file) as fo:
        cache = json.load(fo)
    # assertions
    assert headers == cache

def test_get_data():
    geneactiv_file = os.path.join(__DIR__, 'right_wrist.csv')
    stats_file = os.path.join(__DIR__, 'stats.json')
    ds = pygeneactiv.read(geneactiv_file)
    samples = 0
    sums = pandas.DataFrame()
    # build stats
    for chunk in ds.get_data(chunksize=100):
        if sums.empty:
            sums = chunk.sum(axis=0)
        else:
            sums = sums.add(chunk.sum(axis=0))
        samples += chunk.shape[0]
    # read cached stats
    with open(stats_file, 'r') as fo:
        cache = json.load(fo)
    assert pytest.approx(sums['x'] / samples, cache['mean']['x'])
    assert pytest.approx(sums['y'] / samples, cache['mean']['y'])
    assert pytest.approx(sums['z'] / samples, cache['mean']['z'])
    assert pytest.approx(sums['lux'] / samples, cache['mean']['lux'])
    assert pytest.approx(sums['button'] / samples, cache['mean']['button'])
    assert pytest.approx(sums['thermistor'] / samples, cache['mean']['thermistor'])
    assert samples == cache['samples']

import pytest
from time import time
from producer.noise_simulator import NoNoise, UniformProbabilityNoise

@pytest.mark.parametrize("element", [1, -1, "some-value"])
def test_no_noise_doesnt_drop_elements(element):
    noise = NoNoise()
    assert noise.pipe(element) == element

@pytest.mark.parametrize("element", [1, -1, "some-value"])
def test_uniform_probability_noise_drops_element(element):
    noise = UniformProbabilityNoise(0, 0)
    noise.next_drop_time = 0
    assert noise.pipe(element) == None

@pytest.mark.parametrize("element", [1, -1, "some-value"])
def test_uniform_probability_noise_doesnt_drop_element(element):
    noise = UniformProbabilityNoise(0, 0)
    noise.next_drop_time = time() + 1000
    assert noise.pipe(element) == element

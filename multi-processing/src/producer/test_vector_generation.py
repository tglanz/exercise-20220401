import pytest
import itertools
from producer.vector_generation import create_random_vector_generator, get_supported_distributions

@pytest.mark.parametrize("size", [ 0, -1, -123 ])
def test_create_random_vector_generator_with_negative_size(size):
    with pytest.raises(ValueError):
        create_random_vector_generator(size, "normal")

@pytest.mark.parametrize("distribution", [ None, "", "some-distribution" ])
def test_create_random_vector_generator_with_unsupported_distribution(distribution):
    with pytest.raises(ValueError):
        create_random_vector_generator(1, distribution)

@pytest.mark.parametrize("arguments", [*itertools.product(
    [1, 100],
    get_supported_distributions()
)])
def test_create_random_vector_generator_with_valid_arguments(arguments):
    size, distribution = arguments
    _ = create_random_vector_generator(size, distribution)

@pytest.mark.parametrize("arguments", [*itertools.product(
    [1, 3],
    get_supported_distributions()
)])
def test_generate_random_vector_has_correct_size(arguments):
    size, distribution = arguments
    generate_vector = create_random_vector_generator(size, distribution)
    vector = generate_vector()
    assert vector.size == size
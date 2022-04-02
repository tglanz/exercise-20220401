from typing import Callable, Sequence
from functools import partial
import numpy as np
from numpy.typing import NDArray

GenerateVectorFunction = Callable[[], NDArray]

# We can easily add new distributions such as binomial etc...
# This is not limited to a numpy function, rather we can provide our own
# as long as it accept size and returns an np.array
DISTRIBUTION_PROVIDERS = {
    "normal": np.random.normal,
    "uniform": np.random.uniform
}

def get_supported_distributions() -> Sequence[str]:
    '''Get a list of all of the supported distributions'''
    return DISTRIBUTION_PROVIDERS.keys()

def create_random_vector_generator(size: int, distribution: str) -> GenerateVectorFunction:
    '''
    Creates a function that generates a vector according to the provided size and distribution.

    The approach here is a functional approach rather than an object one. This decision is probably subjective,
    but I believe in this case it leads to a conciser solution.

    Parameters
        size (int): the size of the vector to generate
        distribution (str): the distribution to sample
    
    Returns
        a function which randomly generates a vector
    '''
    if not size > 0:
        raise ValueError(f"size '{size}' is invalid, it must be a positive integer")

    if distribution not in DISTRIBUTION_PROVIDERS:
        raise ValueError(f"'{distribution}' is not a supported distribution")

    return partial(DISTRIBUTION_PROVIDERS[distribution], size=size)
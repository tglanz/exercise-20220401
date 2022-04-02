from abc import ABC, abstractmethod
from random import random
from time import time
from typing import Optional, TypeVar

T = TypeVar('T')

'''
A NoiseSimulator is defined as a pipe that can drop elements.

Concrete impementations can vary and added in the future, for now, only required ones
are implemented.
'''
class NoiseSimulator(ABC):
    @abstractmethod
    def pipe(self, element: T) -> Optional[T]:
        pass

class NoNoise(NoiseSimulator):
    def pipe(self, element: T) -> Optional[T]:
        return element

class UniformProbabilityNoise(NoiseSimulator):
    low: float
    high: float

    next_drop_time: int

    def __init__(self, low: float, high: float):
        self.low = low
        self.high = high

        self.adjust_next_drop_time()

    def adjust_next_drop_time(self):
        self.next_drop_time = time() + (random() * (self.high - self.low)) + self.low
    
    def pipe(self, element: T) -> Optional[T]:
        if time() >= self.next_drop_time:
            self.adjust_next_drop_time()
            return None
        return element
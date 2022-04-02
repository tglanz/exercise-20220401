'''
Calculate the rate of occurences
'''
from dataclasses import dataclass
from time import time
from typing import List

import numpy

@dataclass
class RateStatistics:
    rate: float
    mean: float
    std: float

class RateCalculator:

    previous_occurence_time: int    

    rates_window_size: int
    rates_window: List[float] 

    def __init__(self, rates_window_size: int):
        self.previous_occurence_time = 0
        self.rates_window_size = rates_window_size
        self.rates_window = []

    def on_occurence(self):
        now = time()
        delta = now - self.previous_occurence_time
        rate = 1 / delta

        self.rates_window.insert(0, rate)
        while len(self.rates_window) > self.rates_window_size:
            self.rates_window.pop()

        self.previous_occurence_time = now

    def get_rate(self):
        return self.rates_window[0]

    def calculate_statistics(self):
        return RateStatistics(
            rate=self.rates_window[0],
            mean=numpy.mean(self.rates_window),
            std=numpy.std(self.rates_window)
        )
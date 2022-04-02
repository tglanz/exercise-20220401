from abc import ABC, abstractmethod
from typing import TextIO
import numpy as np
from numpy.typing import NDArray

from consumer.rate_calculator import RateStatistics

class Output(ABC):
    @abstractmethod
    def write_header(self, header: str):
        pass

    @abstractmethod
    def write_data(self, matrix: NDArray):
        pass

    @abstractmethod
    def write_rate_statistics(self, rate_statistics: RateStatistics):
        pass

    @abstractmethod
    def __enter__(self):
        return self.open()
  
    @abstractmethod
    def __exit__(self, *rest):
        self.close()

class FileOutput:

    file_path: str
    file: TextIO

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file = None

    def __enter__(self):
        return self.open()
  
    def __exit__(self, *rest):
        self.close()
  
    def open(self):
        self.file = open(self.file_path, 'w')
        return self
    
    def close(self):
        self.file.close()

    @abstractmethod
    def write_header(self, header: str):
        self.file.write(f"\n*** {header} ***\n")

    @abstractmethod
    def write_data(self, matrix: NDArray):
        self.file.write("\nData\n")
        np.savetxt(self.file, matrix)

        stats = np.array([ matrix.mean(0), matrix.std(0) ])
        self.file.write("\nMean, Std (X[0, i] is the Mean of Data[*, i] and X[1, i] is the Std of Data[*, i]\n")
        np.savetxt(self.file, X=stats.transpose())

        self.file.flush()

    @abstractmethod
    def write_rate_statistics(self, rate_statistics: RateStatistics):
        self.file.writelines([
            "\nRate Statistics\n",
            f"  - Mean: {rate_statistics.mean}\n",
            f"  - Std : {rate_statistics.std}\n",
        ])

        self.file.flush()
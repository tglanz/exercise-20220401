import logging
from time import sleep, time
from typing import Callable
from numpy.typing import NDArray
from producer.vector_generation import GenerateVectorFunction

TransmitVectorFunction = Callable[[NDArray], None]

class FixedIntervalVectorTransmitter:
    logger: logging.Logger
    frequency: int
    generate_vector: GenerateVectorFunction

    def __init__(self,
        frequency: int,
        generate_vector: GenerateVectorFunction,
        transmit_vector: TransmitVectorFunction):
        '''
        Create a VectorTransmitter.

        The VectorTransmitter handles the logic of transmitting generated vectors on a fixed interval  

        Parameters
            frequency (int): Indicates the frequency of transmittion (Hz)
            generate_vector (GenerateVectorFunction): A function that provides the transmitter with vectors
            transmit (TransmitVectorFunction): A function that receives a vector and transmits it
        '''
        self.logger = logging.getLogger(self.__class__.__name__)
        self.frequency = frequency
        self.generate_vector = generate_vector
        self.transmit_vector = transmit_vector
    
    def start(self):
        '''
            Begins an infinite loop which uses the transmition and vector generation functions
            to transmit generated vectors on a fixed interval
        '''
        self.logger.debug("Starting transmition at a frequency of %sHz", self.frequency)

        interval = 1 / self.frequency
        last_timestamp = time()

        while True:
            vector = self.generate_vector()

            # The reason for such approach instead of just "sleep(interval)"
            # is to support the fact that perhaps (and realistically) the generate_vector
            # duration might not be negligible. Hence, we need to cut the time spent on
            # the vector generation from the time we delay for the fixed interval
            passed = time() - last_timestamp
            remaining = interval - passed
            sleep(max(remaining, 0))

            self.transmit_vector(vector)
            last_timestamp = time()
        
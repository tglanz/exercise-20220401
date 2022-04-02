import logging
from arguments import parse_args, Arguments

from producer.vector_transmition import FixedIntervalVectorTransmitter
from producer.vector_generation import create_random_vector_generator
from producer.noise_simulator import NoNoise, UniformProbabilityNoise

def setup_logging(log_level: str):
    logging.basicConfig(
        format='%(asctime)s %(threadName)s %(name)s [%(levelname)s] %(message)s',
        level=logging.getLevelName(log_level.upper())
    )

def create_noise(args: Arguments):
    if not args.noise:
        return NoNoise()
    return UniformProbabilityNoise(args.noise_low, args.noise_high)

def start_producing(args: Arguments):

    noise = create_noise(args)
    def transmitter(vector):
        vector = noise.pipe(vector)
        if vector is not None:
            logging.debug("Transmitting %s", vector)
        else:
            logging.debug("Dropped")

    generate_vector = create_random_vector_generator(
        args.generated_vector_size, args.generated_distribution)
    vector_transmitter = FixedIntervalVectorTransmitter(
        args.transmition_frequency, generate_vector, transmitter)
    vector_transmitter.start()

def main(args: Arguments):
    setup_logging(args.log_level)
    logging.debug("Application start")

    start_producing(args)

    logging.debug("Application finished")

if __name__ == '__main__':
    arguments = parse_args()
    main(arguments)
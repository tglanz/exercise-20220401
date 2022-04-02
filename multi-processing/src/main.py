import logging
from multiprocessing import Pipe
from multiprocessing.connection import Connection
from multiprocessing.dummy import Process
from multiprocessing.sharedctypes import Value
from signal import SIGINT, SIGTERM, signal
from time import sleep, time

from arguments import parse_args, Arguments

from producer.vector_generation import create_random_vector_generator
from producer.noise_simulator import NoNoise, UniformProbabilityNoise

def setup_logging(log_level: str):
    logging.basicConfig(
        format='%(asctime)s %(threadName)s %(name)s [%(levelname)s] %(message)s',
        level=logging.getLevelName(log_level.upper())
    )

def start_producing(args: Arguments, tx: Connection, termination_token):
    logging.debug("Starting production")

    noise = UniformProbabilityNoise(args.noise_low, args.noise_high) if args.noise else NoNoise()

    generate_vector = create_random_vector_generator(
        args.generated_vector_size,
        args.generated_distribution)
    
    interval = 1 / args.transmition_frequency
    last_timestamp = time()

    while not bool(termination_token.value):
        vector = generate_vector()

        # The reason for such approach instead of just "sleep(interval)"
        # is to support the fact that perhaps (and realistically) the generate_vector
        # duration might not be negligible. Hence, we need to cut the time spent on
        # the vector generation from the time we delay for the fixed interval
        passed = time() - last_timestamp
        remaining = interval - passed
        sleep(max(remaining, 0))

        vector = noise.pipe(vector)
        if vector is None:
            logging.debug("Dropped")
        else:
            logging.debug("Transmitting %s", vector)
            tx.send(vector)
            
        last_timestamp = time()

    logging.debug("Ending production")

def start_consuming(args: Arguments, rx: Connection, termination_token):
    logging.debug("Starting consumption")

    interval = 1 / args.transmition_frequency
    while not bool(termination_token.value):

        # I am not sure this is the most accurate approach. I assume all solutions are
        # statistically based but there are probably tighter solutions. 
        if not rx.poll(interval):
            logging.warning("Vector drop detected")
        else:
            vector = rx.recv()
            logging.debug("Received %s", vector)

    logging.debug("Ending consumption")

def main(args: Arguments):
    setup_logging(args.log_level)
    logging.debug("Application start")

    termination_token = Value('i', False)
    for signum in (SIGTERM, SIGINT):
        signal(signum, lambda *_: setattr(termination_token, 'value', True))

    rx, tx = Pipe(duplex=False)
    consumer_process = Process(target=start_consuming, args=(args, rx, termination_token))
    producer_process = Process(target=start_producing, args=(args, tx, termination_token))

    consumer_process.start()
    producer_process.start()

    consumer_process.join()
    producer_process.join()

    logging.debug("Application finished successfuly")

if __name__ == '__main__':
    arguments = parse_args()
    main(arguments)
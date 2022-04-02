import logging
from multiprocessing import Pipe
from multiprocessing.connection import Connection
from multiprocessing.dummy import Process
from multiprocessing.sharedctypes import Value
from signal import SIGINT, SIGTERM, signal
from time import sleep, time

from arguments import parse_args, Arguments
from consumer.output import FileOutput
from consumer.rate_calculator import RateCalculator
from consumer.vectors_collector import VectorsCollector

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
            logging.info("A vector has been dropped")
        else:
            tx.send(vector)
            logging.debug("Transmitting vector")
            
        last_timestamp = time()

    logging.debug("Ending production")

def start_consuming(args: Arguments, rx: Connection, termination_token):
    logging.debug("Starting consumption")

    if args.output_strategy != "file":
        raise ValueError(f"Unsupported output strategy: {args.output_strategy}")
    output = FileOutput(args.output_file_path)
    vectors_collector = VectorsCollector(args.output_batch_size, args.generated_vector_size)

    batch = 1
    interval = 1 / args.transmition_frequency
    rate_calculator = RateCalculator(args.rate_window_size)
    last_rate_display_time = time()

    output.open()
    while not bool(termination_token.value):

        # I am not sure this is the most accurate approach. I assume all solutions are
        # statistically based but there are probably tighter solutions. 
        if not rx.poll(interval * 1.1):
            logging.warning("Vector drop detected")
        else:
            vector = rx.recv()
            vectors_collector.add_vector(vector)
            logging.debug("Received %s", vector)

        rate_calculator.on_occurence()
        now = time()
        if now > last_rate_display_time + args.rate_display_interval:
            logging.info("Consumption Rate: %d", rate_calculator.get_rate())
            last_rate_display_time = now

        if vectors_collector.is_full():
            output.write_header(f"Batch {batch}")
            output.write_data(vectors_collector.matrix)
            output.write_rate_statistics(rate_calculator.calculate_statistics())
            vectors_collector.reset()
            batch += 1

    output.close()
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
import logging
import pickle
import numpy as np
from socket import socket, socketpair, timeout as SocketTimeoutError


from multiprocessing import Process
from multiprocessing.sharedctypes import Value

from signal import SIGINT, SIGTERM, signal
from time import sleep, time
from arguments import parse_args, Arguments

from consumer.output import FileOutput, Output
from consumer.rate_calculator import RateCalculator
from consumer.vectors_collector import VectorsCollector

from producer.vector_generation import create_random_vector_generator
from producer.noise_simulator import NoNoise, NoiseSimulator, UniformProbabilityNoise

def setup_logging(log_level: str):
    logging.basicConfig(
        format='%(asctime)s %(threadName)s %(name)s [%(levelname)s] %(message)s',
        level=logging.getLevelName(log_level.upper())
    )

def create_output(args: Arguments) -> Output:
    '''
    Create an instance of an Output.
    In the future, we might want to output the data onto databases, middlewares and such,
    to do so we shall implement addition Output implementations accordingly.    
    '''
    if args.output_strategy != "file":
        raise ValueError(f"Unsupported output strategy: {args.output_strategy}")
    return FileOutput(args.output_file_path)

def create_noise_simulator(args: Arguments) -> NoiseSimulator:
    return UniformProbabilityNoise(args.noise_low, args.noise_high) if args.noise else NoNoise()

def produce(args: Arguments, tx: socket, termination_token):
    logging.debug("Starting production")

    noise = create_noise_simulator(args)

    generate_vector = create_random_vector_generator(
        args.generated_vector_size,
        args.generated_distribution)
    
    interval = 1 / args.transmition_frequency
    last_timestamp = time()

    while not bool(termination_token.value):
        vector = generate_vector().astype(np.float32)

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
            buffer = pickle.dumps(vector)
            tx.sendall(buffer)
        last_timestamp = time()
    logging.debug("Ending production")

def consume(args: Arguments, rx: socket, termination_token):
    logging.debug("Starting consumption")

    vectors_collector = VectorsCollector(
        args.output_batch_size,
        args.generated_vector_size)

    interval = 1 / args.transmition_frequency

    rate_calculator = RateCalculator(args.rate_window_size)
    last_rate_display_time = time()
    
    rx.settimeout(interval * 1.5)
    with create_output(args) as output:
        # The batch tracking is used to seperate sections in the output
        output_batch = 1
        while not bool(termination_token.value):
            buffer = None
            try:
                buffer = rx.recv(args.rx_chunk_size)
            except SocketTimeoutError:
                # In case we have timeouted it probably indicates that a packet was dropped.
                # This is a rough heuristic and I assume there are better solutions with
                # tighter probabilty for false positives.
                logging.warning("Detected a vector drop")
                rate_calculator.on_occurence(time() - interval)
                continue

            post_receive = time()

            # Deserialize and accumulate the vector
            try:
                vector = pickle.loads(buffer)
                vectors_collector.add_vector(vector)
            except Exception as exception:
                logging.error("Deserialization error %s", exception)
                continue
            
            # Update and Show rates if needed
            rate_calculator.on_occurence()
            if post_receive > last_rate_display_time + args.rate_display_interval:
                logging.info("Consumption Rate: %d", rate_calculator.get_rate())
                last_rate_display_time = post_receive

            # If a batch has been filled, write to output and reset
            if vectors_collector.is_full():
                output.write_header(f"Batch {output_batch}")
                output.write_data(vectors_collector.matrix)
                output.write_rate_statistics(rate_calculator.calculate_statistics())
                vectors_collector.reset()
                output_batch += 1

    logging.debug("Ending consumption")

def main(args: Arguments):
    setup_logging(args.log_level)
    logging.debug("Application start")

    # Listen on termination signals and notify processes so they will halt as required
    termination_token = Value('i', False)
    for signum in (SIGTERM, SIGINT):
        signal(signum, lambda *_: setattr(termination_token, 'value', True))

    # Create a Unix domain socket if possible, otherwise, a Network socket.
    # An alternative, although only for ipc is using Pipes 
    rx, tx = socketpair()

    # Create and start the relevant processes
    processes = [
        Process(target=consume, args=(args, rx, termination_token)),
        Process(target=produce, args=(args, tx, termination_token))]

    for process in processes:
        process.start()
    
    for process in processes:
        process.join()

    logging.debug("Application finished successfuly")

if __name__ == '__main__':
    arguments = parse_args()
    main(arguments)
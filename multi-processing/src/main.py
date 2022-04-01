import logging
from arguments import parse_args, Arguments

def setup_logging(log_level: str):
    logging.basicConfig(
        format='%(asctime)s %(threadName)s %(name)s [%(levelname)s] %(message)s',
        level=logging.getLevelName(log_level.upper())
    )

def main(args: Arguments):
    setup_logging(args.log_level)
    logging.debug("Application start")

    logging.debug("Application finished")

if __name__ == '__main__':
    arguments = parse_args()
    main(arguments)
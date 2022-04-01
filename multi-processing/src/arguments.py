from ast import parse
from dataclasses import dataclass
from argparse import ArgumentParser
from typing import Optional, Sequence, Union

from vector_generation import VectorGenerator

@dataclass
class Arguments:
    log_level: str
    noisy: bool
    generated_vector_length: int
    generated_distribution: str
    output_strategy: str
    output_file_path: str

def parse_args(args: Optional[Sequence[str]] = None) -> Arguments:
    parser = ArgumentParser(
        prog="Python Multi-Processing",
        description="Transmit auto generated vectors accross processes",
        add_help=True
    )

    parser.add_argument("--log-level",
        choices=["error", "warn", "info", "debug"], default="warn",
        help="Determines the log's verbosity")

    parser.add_argument("--noisy",
        action="store_const", const=True, default=False,
        help="If provided, performs a random dropout during vector transmissions")

    parser.add_argument("--generated-vector-length",
        default=50,
        help="Determines the length of the generated vectors")

    parser.add_argument("--generated-distribution",
        choices=VectorGenerator.get_supported_distributions(), default="normal",
        help="Determines the distribution to generate random values according to")

    parser.add_argument("--output-strategy",
        choices=["file"], default="file",
        help="Determines the output method")

    parser.add_argument("--output-file-path",
        default="output.csv",
        help="If using the \"file\" output strategy, determines the path of that file")

    parsed = parser.parse_known_args(args)[0]

    return Arguments(**vars(parsed))
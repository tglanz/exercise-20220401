from ast import parse
from dataclasses import dataclass
from argparse import ArgumentParser
from typing import Optional, Sequence, Union

from producer.vector_generation import get_supported_distributions

@dataclass
class Arguments:
    log_level: str
    noise: bool
    noise_low: int
    noise_high: int
    generated_vector_size: int
    generated_distribution: str
    transmition_frequency: int
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

    parser.add_argument("--noise",
        action="store_const", const=True, default=False,
        help="If provided, performs a random dropout during vector transmissions")

    parser.add_argument("--noise-low",
        default=2, type=int,
        help="When noise is provided, indicates the start of the interval value for uniform distribution")

    parser.add_argument("--noise-high",
        default=3, type=int,
        help="When noise is provided, indicates the end of the interval value for uniform distribution")

    parser.add_argument("--generated-vector-size",
        default=50, type=int,
        help="Determines the size of the generated vectors")

    parser.add_argument("--generated-distribution",
        choices=get_supported_distributions(), default="normal",
        help="Determines the distribution to generate random values according to")

    parser.add_argument("--transmition-frequency", 
        default=1000, type=int,
        help="Specify the frequency of transmition (Hz)")

    parser.add_argument("--output-strategy",
        choices=["file"], default="file",
        help="Determines the output method")

    parser.add_argument("--output-file-path",
        default="output.csv",
        help="If using the \"file\" output strategy, determines the path of that file")

    parsed = parser.parse_known_args(args)[0]

    return Arguments(**vars(parsed))
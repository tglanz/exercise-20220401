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

    rate_display_interval: int
    rate_window_size: int

    rx_chunk_size: int

    output_strategy: str
    output_batch_size: int
    output_file_path: str

def parse_args(args: Optional[Sequence[str]] = None) -> Arguments:
    parser = ArgumentParser(
        prog="Python Multi-Processing",
        description="Transmit auto generated vectors accross processes",
        add_help=True
    )

    parser.add_argument("--log-level",
        choices=["error", "warning", "info", "debug"], default="info",
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

    parser.add_argument("--rate-display-interval",
        default=1, type=int,
        help="Specify in seconds, the interval on which to display received vectors rate")

    parser.add_argument("--rate-window-size",
        default=100, type=int,
        help="Specify the window size on which to calculate rate statistics such as mean and std")

    parser.add_argument("--output-strategy",
        choices=["file"], default="file",
        help="Determines the output method")

    parser.add_argument("--output-batch-size",
        default=100, type=int,
        help="Determines the number of vectors within an output matrix")

    parser.add_argument("--output-file-path",
        default="output.txt",
        help="If using the \"file\" output strategy, determines the path of that file")

    # Specification of chunk size can be improved with appropriate logic
    # First approach is computing the required size
    # Second approach is to build the packet from small chunks
    parser.add_argument("--rx-chunk-size",
        default=8192, type=int,
        help="Specify the chunk size when receiving packets an the consumer side")

    parsed = parser.parse_args(args)

    return Arguments(**vars(parsed))
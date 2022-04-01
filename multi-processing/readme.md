# multi-processing

Demonstrate multi processing techniques by implementing 2 processes communicating data between.

## Execution

__Virtual Environment__

It is recommended to work from within an isolated python environment to avoid collisions with the system dependencies and/or other projects.

Create a virtual environment located at ```.venv```

    python3 -m venv .venv

Activate the virtual environment located ```.venv```

    source .venv/bin/activate

__Dependencies__

Notable dependencies for this project
- ```numpy``` provides us with tensor computation capabilities
- ```pytest``` used as our testing framework and platform

The project's dependencies are managed using ```pip3``` and are locked in the ```requirements.txt``` file.

To install the dependencies

    pip3 install -r requirements.txt

__Testing__

Tests are found in `test` directory.

To execute the tests

    python3 -m pytest -v test

__Running__

Like any other python program

    python3 src/main.py

The application runs with sensible defaults. To view all of the available arguments run

    python3 src/main.py --help

## Development

__Milestones__

- [x] Initial project
- [x] Main skeleton with logging and arguments
- [x] Vector Generation
- [ ] Transmitter
- [ ] Rate calcuation
- [ ] Dropout extrapolations
- [ ] Analytics
- [ ] Output generation
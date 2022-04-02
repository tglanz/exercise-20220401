# multi-processing

Demonstrate multi processing techniques by implementing 2 processes communicating data between.

## Execution

__Virtual Environment__

It is recommended to work from within an isolated python environment to avoid collisions with the system dependencies and/or other projects.

Create a virtual environment located at ```.venv```

    python -m venv .venv

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

Tests are found near the testees (An alternative is to have their own directory).

To execute the tests

    PYTHONPATH=src python -m pytest -v

__Running__

Like any other python program

    python src/main.py

The application runs with sensible defaults. To view all of the available arguments run

    python src/main.py --help

## Development

__Milestones__

Producer

- [x] Initial project
- [x] Main skeleton with logging and arguments
- [x] Vector Generation
- [x] Transmition
- [x] Noises

Consumer

- [ ] Rate calcuation
- [ ] Dropout extrapolations
- [ ] Analytics
- [ ] Output generation

## Design Considerations

### Noises

We treat noise as a function that receives an element and might not yield it back.

Here, we are interested in a specific kind of noise which randomly drop elements every X seconds where
X is a variable on the [2, 3] interval.

Our first goal is to implement this feature, but we would like to have a design that enables us future changes and enhances. Therefore, we abstract this functionality and concretely implement the requirements. It enable us to add different logics in the future, have more mechanisms for debugging and better testability.

Another benefit is better seperation. Specifically, the Noise is a mean to simuate external forces and it would seem a bit odd to implement such logic in the generation/transmition logic rather than bootstraping it externally.

That said, in a real project and more time there can be lots of improvements to the current mechanism - From arguments, configurability, queryability and more.
# multi-processing

Demonstrate multi processing techniques by implementing 2 processes communicating data between.

## Execution

__tl; dr__

    # Prepare a python virtual environment
    python -m venv .venv
    
    # Enter the virtual environment
    source .venv/bin/activate
    
    # Install the dependencies
    pip install -r requirements.txt
    
    # Run the tests
    PYTHONPATH=src python -m pytest -v
    
    # Run with noise (Exit with Ctrl-C)
    python src/main.py --noise

    # Show help message for the application arguments
    python src/main.py --help

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

Tests are found in ```tests``` directory - Another option is near the testees. 

Really, more tests should have been made. Verifying stastics are correct, rate calculation, output generation etc...

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

- [x] Rate calcuation
- [x] Dropout extrapolations
- [x] Analytics and Output generation

## Design Considerations

### Noises

We treat noise as a function that receives an element and might not yield it back.

Here, we are interested in a specific kind of noise which randomly drop elements every X seconds where
X is a variable on the [2, 3] interval.

Our first goal is to implement this feature, but we would like to have a design that enables us future changes and enhances. Therefore, we abstract this functionality and concretely implement the requirements. It enable us to add different logics in the future, have more mechanisms for debugging and better testability.

Another benefit is better seperation. Specifically, the Noise is a mean to simuate external forces and it would seem a bit odd to implement such logic in the generation/transmition logic rather than bootstraping it externally.

That said, in a real project and more time there can be lots of improvements to the current mechanism - From arguments, configurability, queryability and more.

### Generation and Distribution abstraction

Same concept as the noises

## Known Issues

1. After migrating to socket based communication rather than pipes, on rare occasions there is an issue in deserializing vectors. Currently it is surrounded by a try catch (not a solution of course)

2. Performance is a bit on the low size. Degregaded while moving to the socket API and manually de/serializing. Options to improve
  - Compression
  - Multiple consumers


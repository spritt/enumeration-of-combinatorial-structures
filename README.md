# Enumeration of combinatorial structures
A standalone Python library for enumeration of combinatorial structures. Currently supports labeled and unlabeled atom, union, product, sequence, set and cycle constructions with and without cardinality constraints.

Developed as a thesis project at Princeton University under the advisement of Jérémie Lumbroso (https://github.com/jlumbroso)

### Dependencies
This library is completely standalone - no external libraries are needed to run the examples in `test.py`. To run the regression tests in `maple-test.py`, you will need to have Java 1.6 or higher and Maple 2016 installed.

### Run the tests
Clone the repository. From the root directory, update `PYTHONPATH` to include the current working directory.
```
export PYTHONPATH=$PWD:$PYTHONPATH
```
Run the tests from the command line:
```
python test/test.py
```



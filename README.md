# Enumeration of combinatorial structures
A standalone Python library for enumeration of combinatorial structures. Currently supports labeled and unlabeled atom, union, product, sequence, set and cycle constructions with and without cardinality constraints.

Developed as a thesis project at Princeton University under the advisement of Jérémie Lumbroso (https://github.com/jlumbroso)

### Background

Combinatorial enumeration is the process of counting objects of finite size using analytic methods. For instance, there are 14 different configurations of the binary trees of size 5 if we define the size of a binary tree to be the number of its internal nodes. It is often possible to enumerate such objects through various algebraic methods such as Lagrange inversions and Taylor series expansions, and an entire field of research has been devoted to such method. We took an algorithmic approach with the aim of developing an automated software tool for enumeration of arbitrarily complex combinatorial objects.

To date, there exists no open source, user-friendly tool for combinatorial enumeration. We have developed a fully functional Python library based on the methods discussed in this paper. We have also produced the first paper which fully documents all of the algorithms underlying this method of combinatorial enumeration through a combination of definitions, algorithms and our own observations drawn from building and testing the prototype.

The library has been extensively tested on both labeled and unlabeled grammars composed of union, product, sequence, set and cycle constructions with and without cardinality restrictions. The Online Encyclopedia of Integer Sequences and Maple’s combstruct library were used as references for testing. Next steps will be to extend support to the more mathematically complex undirected sequence and undirected cycle constructions.

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



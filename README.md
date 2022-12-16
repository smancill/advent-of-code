# README

Solutions for [Advent of Code](https://adventofcode.com).

## How to run solutions

Use a _year_ directory as working directory.

```
$ cd <year>
```

Each _day_ has its own `dayXX.py` file with the solution.
Input data is read from `stdin`:

```
$ python dayXX.py < inputXX.txt
```

Examples are tested with [`doctest`](https://docs.python.org/3/library/doctest.html).
Each _day_ has its own `dayXX.txt` file:

```
$ python -m doctest -f -o REPORT_UDIFF dayXX.txt
```

The [helper scripts](bin/README.md) can be used to simplify
editing and running solutions.

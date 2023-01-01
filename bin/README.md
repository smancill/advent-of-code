# Helper scripts

- Login into the [Advent of Code website][aoc] and get the session cookie
  (Firefox: _Web Developer Tools_ > _Storage_ > _Cookies_).

  Use the value to set the `$AOC_SESSION_COOKIE` environment variable.

- Scripts in this directory can be added to `$PATH` using [`direnv`][direnv].

- Create the `<year>` directory if missing, use it as working directory.

- Work on solving the current day puzzle
  (this automatically downloads the user _input data_):

        $ day

- Run the solution using the [`doctest`][doctest] example file:

        $ run -t

- Run the solution with the user _input data_:

        $ run

- Run also accepts input from _stdin_:

        $ echo "input" | run

- All scripts accept a _day_ as argument.


[aoc]: https://adventofcode.com
[direnv]: https://direnv.net/
[doctest]: https://docs.python.org/3/library/doctest.html

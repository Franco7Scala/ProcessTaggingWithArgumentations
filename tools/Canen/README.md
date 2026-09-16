µ-toksia : SAT-based Solver for Argumentation Frameworks
========================================================

Version    : ICCMA'21

Author     : [Andreas Niskanen](mailto:andreas.niskanen@helsinki.fi), University of Helsinki

When using `mu-toksia`, please cite the following paper ([BibTeX](https://dblp.org/rec/conf/kr/NiskanenJ20a.html?view=bibtex)):
Andreas Niskanen and Matti Järvisalo. [µ-toksia: An Efficient Abstract Argumentation Reasoner.](https://doi.org/10.24963/kr.2020/82) Proc. KR'20.

For the version supporting the dynamic track of ICCMA'19, see the [dynamic](https://bitbucket.org/andreasniskanen/mu-toksia/src/dynamic) branch of this repository.

Installation
------------

Before compiling, please make sure that gcc, g++, make, and cmake are installed on your system.

To compile µ-toksia, please run:
```
./build.sh
```

To remove all object files, please run:
```
make clean
```

Usage
-----

```
./mu-toksia -p <task> -f <file> -fo <format> [-a <query>]

  <task>      computational problem
  <file>      input argumentation framework
  <format>    file format for input AF
  <query>     query argument

Options:
  --help      Displays this help message.
  --version   Prints version and author information.
  --formats   Prints available file formats.
  --problems  Prints available computational problems.
```

SAT solver [CryptoMiniSat](https://github.com/msoos/cryptominisat) (version 5.8.0) is included in this release.

Contact
-------

Please direct any questions, comments, bug reports etc. directly to [the author](mailto:andreas.niskanen@helsinki.fi).

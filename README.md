# Basic Exercise System
This rather slim system makes it easier to keep the overview over ever-growing
numbers of created tasks for exercise sheets of a lecture over several
semesters.

The core feature is the `task-catalogue` that collects all exercises and their
solutions for a semester. All tasks in the catalogue get an internal name that
can be referenced in exercise sheets, which makes the exercise sheet files very
slim and modular.

As an example, the `sheet01.tex` file of the `mock-lecture` only contains the
following code:
```
\documentclass[12pt]{article}
\usepackage{mock-lecture-header}

\setcounter{Tcount}{1}
\setcounter{Hcount}{1}

\begin{document}
    \buildheader{October 18th, 2022}{Exercise Sheet}{01}
    \tutortask{hello-world}
    \tutortask{boxexample}
    \homework{reftask}{10 points}
    \homework{figureexample}{5 points}
\end{document}
```

There are also some nice little extra features: The generated catalogue file,
that contains all exercises, automatically tells you if and where a task was
already used and allows you to catalogue and group your files by subsections.

Separate Exercise and Solution files are automatically created.

When a catalogue task is updated, only sheets are rebuilt that include this
task. References to past tasks -- by name in catalogue, by task number in exercise
sheets, also to older sheets! -- are possible by using `\ref{internal-task-name}`.

Some small, hopefully helpful macros are defined in the `misc/header.sty` file.
## Usage
Have a look at the `mock-lecture/task-catalogue/task-catalogue.tex` first. The
`Makefile`s are hierachical, every `Makefile` triggers their childrens
`Makefile`s.

The easiest way to create a new lecture is to copy over the `mock-lecture`
folder. Semester folders are expected to have `20` as a prefix. Sheets are
expected to have `sheet` as a prefix, exams to have `exam` as a prefix. The
latter two can be changed in the `Makefile` on the same level, the first one in
the `misc/snip-catalogue.py`.

Add new tasks in `task-catalogue/task-catalogue.tex`, give them an internal name
and simply reference them in your exercise sheets of the same lecture folder.
Then just use `make` in the semester folder, the catalogue is automatically
built as well.

Change the contents of the `lecture-header.sty` to the content that does not
change over semesters and `mock-lecture-header.sty` the content that does change
every semester. The `misc/header.sty` should not need editing, except if you
would like to add package imports or macros that should be available over all
lectures.

Don't like the page layout or header? Change the `\buildheader` macro and
geometry in the `misc/header.sty`. Add your own group or chair logo in the same
folder.

If anything is unclear or buggy, feel free to open an issue or to contact me.

## Requirements
This project requires `python>=3.6` and access to `make`.

This project uses `pdflatex` to build its sheets since pdfTex should be the most
widely available latex typesetter. If you believe in or need other TeX
typesetters, adjust the calls in the `Makefile`s of the lectures.
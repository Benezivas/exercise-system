#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Decompose a task catalogue (given as first argument) into separate .tex files
for tasks with and without solutions. These so-called snaps are then later used to
modularly build exercise sheets and the like. This decomposition is done such that
only sheets need to be rebuilt that actually saw a change in one of their tasks."""

import re, sys
from pathlib import Path, PurePath

def is_text_and_file_content_identical(text, filename):
    identical = True
    if not Path(filename).exists():
        identical = False
    else:
        old_text = []
        with open(filename, "r") as f:
            old_text = f.readlines()

        for a, b in zip(text, old_text):
            if a.strip() != b.strip():
                print(a.strip())
                print(b.strip())
                identical = False

    return identical

def write_lines_to_file(lines, filename):
    print("Writing file ", filename)
    with open(filename, "w") as f:
        for line in lines:
            f.write(line)
            f.write("\n")

def is_file_relevant(name):
    return name.startswith("sheet") or name.startswith("exam")

if not len(sys.argv) > 1:
    sys.exit("Please provide a task catalogue as an argument!")
if not Path(sys.argv[1]).is_file():
    sys.exit("The given task catalogue does not exist in the file system!")

lines = []
with open(sys.argv[1], "r") as f:
    lines = f.readlines()

Path("snaps").mkdir(exist_ok=True)

changed = set()

in_exercise = False
in_solution = False
text = []
solution = []
for line in lines:
    line = line.strip("\n")
    if line.lstrip().startswith("\\begin{task}"):
        in_exercise = True
        name = re.search('^.begin{task}{(.*)}', line).group(1)
        text = []
        solution = []
    elif line.lstrip().startswith("\\end{task}"):
        #Write out exercise and solution to files
        identical = is_text_and_file_content_identical(text, f"snaps/{name}.tex")
        if not identical:
            write_lines_to_file(text, f"snaps/{name}.tex")
            changed.add(name)
        if solution == []:
            solution = [ "\\textbf{!!!!! No solution found for this task !!!!!}" ]
        identical = is_text_and_file_content_identical(solution, f"snaps/{name}-solution.tex")
        if not identical:
            write_lines_to_file(solution, f"snaps/{name}-solution.tex")
            changed.add(name)
        in_exercise = False
        in_solution = False
    elif line.lstrip().startswith("\\solution"):
        in_solution = True
    elif in_solution:
        solution.append(line)
    elif in_exercise:
        text.append(line)

#list all subdirectories of the top repo levels directories
possibly_relevant_directories = sum([list(dir.iterdir()) for dir in Path("../../").iterdir() if dir.is_dir()], [])

#we are only interested in those that resemble a semester folder
relevant_directories = [Path(dir).resolve() for dir in possibly_relevant_directories
                        if dir.name.startswith("20")] # Hello year 2100 and up, I hope all is well.

files = []
for dir in relevant_directories:
    for file in [Path(dir, f) for f in Path(dir).iterdir() if is_file_relevant(f.name) and Path(dir, f).resolve().is_file()]:
        files.append(file)

matcher = re.compile('.*task{([^}]+)}')
matched_tasks = []
for sheet in files:
    with open(sheet, "r") as f:
        for line in f.readlines():
            match = matcher.match(line)
            if match:
                if match.group(1) in changed:
                    print("touch " + sheet.name)
                    Path(sheet).touch()
                matched_tasks.append((match.group(1), "{}/{}".format(PurePath(sheet).parent.name, PurePath(sheet).name)))

with open("collection-expanded.tex", "w") as f:
    for line in lines:
        if line.startswith("\\begin{task}"):
            in_exercise = True
            name = re.search('^.begin{task}{(.*)}', line).group(1)
            if name in [task[0] for task in matched_tasks]:
                line += "{\color{gray}This task was already used in: $\{$"
                for task in matched_tasks:
                    if name == task[0]:
                        line += "{} ".format(task[1])
                line += "$\}$}\\\\"
        f.write(line)


with open("collection-expanded.tex", "r") as input:
    with open("collection-nosolutions.tex", "w") as output:
        in_solution = False
        for line in input:
            if line.startswith("\\solution"):
                in_solution = True
            if line.startswith("\\end{task}"):
                in_solution = False
            if not in_solution:
                output.write(line.strip())

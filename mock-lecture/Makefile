SEMESTERDIRS = $(patsubst 20%, 20%/sheet01/exercise_sol.pdf, $(wildcard 20*/))

all: task-catalogue/catalogue/catalogue_sol.pdf $(SEMESTERDIRS)

20%/sheet01/exercise_sol.pdf:
	cd 20$* && $(MAKE)

task-catalogue/catalogue/catalogue_sol.pdf:
	cd task-catalogue && $(MAKE)
SHEETPDF = $(patsubst sheet%.tex, sheet%/exercise_sol.pdf, $(wildcard sheet*.tex))
EXAMPDF = $(patsubst exam%.tex, exam%/exam_sol.pdf, $(wildcard exam*.tex))

.PHONY: all clean auxcleanup catalogue

all: catalogue $(SHEETPDF) $(EXAMPDF) auxcleanup

clean:
	rm -rf sheet*/ exam*/

auxcleanup:
#	Remove remaining .aux files from sheet folders after building is complete
	rm -rf */*.aux

catalogue:
	cd ../task-catalogue && $(MAKE)

sheet%/exercise_sol.pdf: sheet%.tex mock-lecture-header.sty ../lecture-header.sty ../../misc/header.sty
	mkdir -p sheet$*;
#	Build the exercise sheet without solutions for students
	pdflatex -output-directory sheet$* -jobname=exercise     "\input{$<}";
#	Build the exercise sheet with solutions
	pdflatex -output-directory sheet$* -jobname=exercise_sol "\def\solution{} \input{$<}";

#	Build references to task numbers of past sheets, if any
	cat sheet*/exercise_sol.aux sheet$*.tex | grep newlabel > temp
	cat temp >> sheet$*/exercise_sol.aux
	cat temp >> sheet$*/exercise.aux
	rm -f temp

#	Run pdflatex a second time to ensure that references are resolved correctly
	pdflatex -output-directory sheet$* -jobname=exercise            "\input{$<}";
	pdflatex -output-directory sheet$* -jobname=exercise_sol        "\def\solution{} \input{$<}";

#	Cleanup
	rm sheet$*/*.log

exam%/exam_sol.pdf: exam%.tex mock-lecture-header.sty ../lecture-header.sty ../../misc/header.sty
	mkdir -p exam$*;
#	Build the exam as it should be handed out to students
	pdflatex -output-directory exam$* -jobname=exam            "\def\exam{} \input{$<}";
#	Build the exam with solutions
	pdflatex -output-directory exam$* -jobname=exam_sol        "\def\exam{} \def\solution{} \input{$<}";
#	Build the exam with solutions and a possibly added correction scheme (using \solscheme in tasks).
	pdflatex -output-directory exam$* -jobname=exam_sol_scheme "\def\exam{} \def\solution{} \def\scheme{} \input{$<}";
#	Cleanup
	rm exam$*/*.log exam$*/*.aux
.PHONY: all clean snippets

all: snippets catalogue/catalogue_sol.pdf

clean:
	rm -rf catalogue/ snaps/ collection-expanded.tex collection-nosolutions.tex

snippets:
	python3 ../../misc/snip-catalogue.py task-catalogue.tex

catalogue/catalogue_sol.pdf: catalogue.tex mock-lecture-header.sty snippets task-catalogue.tex ../../misc/snip-catalogue.py
	mkdir -p catalogue;
	pdflatex -output-directory catalogue -jobname=catalogue     "\def\catalogue{} \input{$<}";
	pdflatex -output-directory catalogue -jobname=catalogue     "\def\catalogue{} \input{$<}";
	pdflatex -output-directory catalogue -jobname=catalogue_sol "\def\catalogue{} \def\solution{} \input{$<}";
	pdflatex -output-directory catalogue -jobname=catalogue_sol "\def\catalogue{} \def\solution{} \input{$<}";
MAIN = main.tex
TEX = $(MAIN) reentrega.tex
BIB = references.bib
PDF = Informe_RTP1.pdf
CLEAN = *.aux *.log $(PDF) *.bbl *.blg

$(PDF): $(TEX) $(BIB)
	pdflatex $(MAIN)
	bibtex main
	pdflatex $(MAIN)
	pdflatex $(MAIN)
	mv main.pdf $(PDF)

clean:
	rm $(CLEAN)

MAIN = main.tex
TEX = $(MAIN) reentrega.tex
PDF = Informe_RTP1.pdf
CLEAN = *.aux *.log $(PDF)

$(PDF): $(TEX)
	pdflatex $(MAIN)
	pdflatex $(MAIN)
	mv main.pdf $(PDF)

clean:
	rm $(CLEAN)

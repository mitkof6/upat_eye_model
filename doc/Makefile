MAIN = manuscript
TEX = pdflatex -file-line-error -interaction=nonstopmode "\input"
BIB = bibtex
GLS = makeglossaries

all: $(MAIN).aux $(MAIN).bbl $(MAIN).gls $(MAIN).pdf
	$(TEX) $(MAIN).tex

read:
	okular $(MAIN).pdf

clean::
	rm -fv *.acn *.acr *.alg *.aux *.bbl *.blg *.glg *.glo *.gls *.idx \
	*.ind *.ist *.lot *.out *.toc *.ilg *.lof *.log chapters/*.aux


$(MAIN).aux: $(MAIN).tex
	$(TEX) $(MAIN).tex

$(MAIN).gls: $(MAIN).tex
	$(GLS) $(MAIN)

$(MAIN).bbl: $(MAIN).aux
	$(BIB) $(MAIN)

$(MAIN).pdf: $(MAIN).aux $(MAIN).bbl $(MAIN).gls
	$(TEX) $(MAIN).tex

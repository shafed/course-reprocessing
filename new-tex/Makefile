# Сборка лекций: все артефакты компиляции (PDF, aux, log) пишутся в build/
LATEX     = pdflatex
LATEXOPTS = -interaction=nonstopmode -halt-on-error -output-directory=build

SOURCES = $(wildcard Лекция_*.tex)
PDFS    = $(patsubst %.tex,build/%.pdf,$(SOURCES))

.PHONY: all clean

all: $(PDFS)

# Два прогона для корректных ссылок и нумерации
build/%.pdf: %.tex | build
	$(LATEX) $(LATEXOPTS) "$<"
	$(LATEX) $(LATEXOPTS) "$<"

build:
	mkdir -p build

# Удалить промежуточные артефакты, оставив PDF
clean:
	rm -f build/*.aux build/*.log build/*.out build/*.toc build/*.fls build/*.fdb_latexmk

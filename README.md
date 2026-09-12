# Variant Analyzer

Reads a **VCF file**, classifies the genetic variants inside it, and explains what it found —
in plain language, next to the numbers.

Available as a command-line tool and as a bilingual (EN/RO) web dashboard with charts,
filters and CSV export.

Built from scratch as a first-year MSc Bioinformatics project, to understand variant
classification by implementing it rather than by reading about it.

**Live demo:** https://variant-analyzer-le.streamlit.app
> First load can take up to a minute while the free Streamlit instance wakes up.

---

## What it does

| | |
| --- | --- |
| **Parse** | Reads `.vcf` and `.vcf.gz` with a plain-Python parser — no C dependencies |
| **Classify** | Labels each variant as SNP, insertion or deletion by comparing REF and ALT lengths |
| **Summarise** | Totals per type, plus how many variants passed the caller's own quality filter |
| **Interpret** | Turns those numbers into a sentence: mean quality, PASS percentage, and whether the call set looks high, moderate or low quality |
| **Visualise** | Variant-type breakdown and quality-score distribution, drawn with Plotly |
| **Filter** | By variant type, chromosome and minimum quality, with CSV export of the result |
| **Teach** | A Theory page on DNA, genes and variants, plus an interactive VCF explainer: click any of the eight columns and see what that field means |

Upload your own file, or leave the uploader empty and the app runs on the bundled
`data/example.vcf`.

---

## Setup

Python 3.10 or newer.

```bash
git clone https://github.com/UserLEmanuel/Variant-Analyzer.git
cd Variant-Analyzer
python -m venv venv
```

```bash
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

```bash
pip install -r src/requirements.txt
```

## Usage

### Web dashboard

```bash
cd src
streamlit run app.py
```

Two pages: **Theory** (an introduction to DNA, genomes and variants, plus the interactive VCF
explainer) and **Analyzer** (statistics, charts, filters and CSV export). The language switch
sits at the right of the navbar.

### Command line

```bash
cd src
python main.py
python main.py --file ../data/example.vcf --type SNP --chromosome 12 --min-quality 80
python main.py --type all --chromosome all --min-quality 0
```

| Option | Short | Description | Default |
| --- | --- | --- | --- |
| `--file` | `-f` | Path to the VCF file | `../data/example.vcf` |
| `--type` | `-t` | Filter by type (`SNP`, `Insertion`, `Deletion`, `all`) | `SNP` |
| `--chromosome` | `-c` | Filter by chromosome (`all` to disable) | `12` |
| `--min-quality` | `-q` | Minimum QUAL score | `80` |

---

## Project structure

The logic is kept out of the interface, so parsing and analysis can be reused and tested
on their own.

```
data/example.vcf       sample VCF file
src/parser.py          reads and parses VCF files (plain text, no C dependencies)
src/models.py          the Variant data model
src/analyzer.py        statistics and filtering — pure functions, no Streamlit
src/main.py            command-line interface (argparse + rich)
src/app.py             web dashboard entry point (Streamlit)
src/i18n.py            every string in EN and RO, behind a t() lookup
src/ui/                dashboard pages: navbar, theory, analyzer, interpretation, VCF explainer
src/requirements.txt   dependencies (also read by Streamlit Cloud on deploy)
```

---

## Why not cyvcf2

The first version used `cyvcf2`. It is the right library for production genomics work, but it
builds against **htslib**, which means a C toolchain. On Windows that is a real obstacle, and
it made the project harder to run than the project itself is.

VCF is tab-separated text. Parsing the seven fixed columns takes about thirty lines of Python
and no dependencies at all. The current parser runs identically on Windows, Linux and Streamlit
Cloud, with nothing to compile.

The trade-off is deliberate: `cyvcf2` is faster on multi-gigabyte files and handles the full
specification, including multi-allelic records and sample genotypes. For a teaching tool run on
small files, portability was worth more than speed.

---

## A one-minute VCF primer

A VCF line describes one position where the sample differs from the reference genome:

```
#CHROM  POS        ID  REF  ALT  QUAL  FILTER  INFO
7       140453136  .   C    T    99    PASS    AF=0.21
```

Chromosome 7, position 140,453,136, where the reference has a `C` and this sample has a `T`.
One letter for one letter — a **SNP**. If `ALT` were longer than `REF` it would be an
**insertion**; shorter, a **deletion**. `QUAL` is the caller's confidence; `FILTER` is its own
verdict on whether the call is trustworthy.

---

## Limitations

A learning tool, not a clinical one.

- Only the first alternate allele of a multi-allelic record is read.
- Classification is length-based, so complex substitutions fall outside SNP / insertion / deletion.
- No annotation against gene or variant databases, and therefore no claim about pathogenicity.
- Nothing here should be used to interpret a real patient's genome.

## Roadmap

- Full multi-allelic support
- Annotation against a reference gene set, so a variant can be placed in a gene
- Tests over `parser.py` and `analyzer.py`

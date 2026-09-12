# Variant Analyzer

Analizeaza variante genetice (SNP, insertii, deletii) dintr-un fisier VCF.

## Setup

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Utilizare

### CLI

```powershell
cd src
python main.py
```

Optiuni disponibile:

```powershell
python main.py --file ../data/example.vcf --type SNP --chromosome 12 --min-quality 80
python main.py --type all --chromosome all --min-quality 0
```

| Optiune | Scurt | Descriere | Implicit |
|---|---|---|---|
| `--file` | `-f` | Calea catre fisierul VCF | `../data/example.vcf` |
| `--type` | `-t` | Filtreaza dupa tip (`SNP`, `Insertion`, `Deletion`, `all`) | `SNP` |
| `--chromosome` | `-c` | Filtreaza dupa cromozom (`all` pentru toate) | `12` |
| `--min-quality` | `-q` | Calitate minima (QUAL) | `80` |

### Dashboard web

```powershell
cd src
streamlit run app.py
```

Se deschide in browser un dashboard cu statistici, un grafic al tipurilor de variante
si un tabel filtrabil. Poti incarca propriul fisier `.vcf` sau folosi fisierul exemplu.

## Structura proiectului

```
data/example.vcf   fisier VCF de test
src/parser.py       citeste si parseaza fisiere VCF (text simplu, fara dependinte C)
src/models.py        modelul de date Variant
src/analyzer.py      statistici si filtrare variante
src/main.py           interfata de linie de comanda (rich)
src/app.py            dashboard web (streamlit)
```

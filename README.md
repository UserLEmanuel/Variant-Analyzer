# Variant Analyzer

Analizeaza variante genetice (SNP, insertii, deletii) dintr-un fisier VCF.
Disponibil ca CLI si ca dashboard web bilingv (EN/RO), cu grafice si export CSV.

**Live demo:** dashboard-ul e deployat pe Streamlit Cloud (entry point `src/app.py`).

## Setup local

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r src\requirements.txt
```

## Utilizare

### Dashboard web

```powershell
cd src
streamlit run app.py
```

Se deschide un dashboard cu doua pagini:
- **Theory** — o mica introducere in ADN, genom si variante genetice, plus un explicator interactiv al coloanelor unui fisier VCF.
- **Analyzer** — statistici, grafice (distributia tipurilor si a calitatii), filtre (tip, cromozom, calitate minima) si export CSV al variantelor filtrate. Poti incarca propriul fisier `.vcf`/`.vcf.gz` sau folosi fisierul exemplu.

Limba (EN/RO) se schimba din colturile dreapta-sus ale navbar-ului.

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

## Structura proiectului

```
data/example.vcf        fisier VCF de test
src/parser.py            citeste si parseaza fisiere VCF (text simplu, fara dependinte C)
src/models.py             modelul de date Variant
src/analyzer.py           statistici si filtrare variante
src/main.py                interfata de linie de comanda (rich)
src/app.py                 punct de intrare al dashboard-ului web (streamlit)
src/i18n.py                texte EN/RO pentru dashboard
src/ui/                    paginile dashboard-ului (navbar, home/theory, analyzer, interpretare, explicator VCF)
src/requirements.txt       dependinte (citit si de Streamlit Cloud la deploy)
```

## De ce nu cyvcf2

Fisierele VCF de aici sunt text simplu tab-separated, asa ca parser.py foloseste un parser
Python simplu, fara dependinte C. `cyvcf2` (folosit initial) are nevoie de `htslib` si nu se
instaleaza usor pe Windows fara unelte de build suplimentare — varianta curenta ruleaza
identic pe Windows, Linux si Streamlit Cloud, fara nicio instalare speciala.

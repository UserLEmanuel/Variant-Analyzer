import io
from pathlib import Path

import pandas as pd
import streamlit as st

from parser import parse_vcf, classify_variant
from analyzer import analyze_variants, filter_variants
from models import Variant

st.set_page_config(page_title="Variant Analyzer", page_icon="🧬", layout="wide")

DEFAULT_VCF = Path(__file__).resolve().parent.parent / "data" / "example.vcf"


def parse_vcf_from_text(text):
    """La fel ca parse_vcf, dar pornind de la text deja citit (pentru fisiere incarcate)."""
    variants = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        chromosome, position, _id, reference, alt_field, qual, filter_field = fields[:7]
        alternative = alt_field.split(",")[0]
        quality = 0.0 if qual == "." else float(qual)
        filter_status = "PASS" if filter_field in (".", "") else filter_field
        variants.append(Variant(
            chromosome=chromosome,
            position=int(position),
            reference=reference,
            alternative=alternative,
            quality=quality,
            filter=filter_status,
            type=classify_variant(reference, alternative)
        ))
    return variants


st.title("🧬 Variant Analyzer")
st.caption("Analiza variantelor genetice dintr-un fisier VCF")

with st.sidebar:
    st.header("Fisier VCF")
    uploaded_file = st.file_uploader("Incarca un fisier .vcf", type=["vcf", "txt"])
    use_example = st.checkbox("Foloseste fisierul exemplu", value=uploaded_file is None)

variants = None
error_message = None

try:
    if uploaded_file is not None and not use_example:
        text = io.TextIOWrapper(uploaded_file, encoding="utf-8").read()
        variants = parse_vcf_from_text(text)
    else:
        variants = parse_vcf(str(DEFAULT_VCF))
except FileNotFoundError:
    error_message = "Fisierul exemplu nu a fost gasit."
except (ValueError, IndexError) as error:
    error_message = f"Fisierul VCF pare invalid: {error}"

if error_message:
    st.error(error_message)
    st.stop()

if not variants:
    st.warning("Fisierul VCF nu contine variante.")
    st.stop()

statistics = analyze_variants(variants)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total variante", statistics["total"])
col2.metric("SNP-uri", statistics["snps"])
col3.metric("Insertii", statistics["insertions"])
col4.metric("Deletii", statistics["deletions"])
col5.metric("PASS", statistics["passed"])

st.divider()

left, right = st.columns([1, 2])

with left:
    st.subheader("Distributie tipuri")
    type_counts = pd.DataFrame({
        "Tip": ["SNP", "Insertie", "Deletie"],
        "Numar": [statistics["snps"], statistics["insertions"], statistics["deletions"]]
    }).set_index("Tip")
    st.bar_chart(type_counts)

with right:
    st.subheader("Filtreaza variantele")

    all_chromosomes = sorted({v.chromosome for v in variants}, key=lambda c: (len(c), c))
    all_types = sorted({v.type for v in variants})

    f1, f2, f3 = st.columns(3)
    with f1:
        selected_type = st.selectbox("Tip variantă", ["Toate"] + all_types)
    with f2:
        selected_chromosome = st.selectbox("Cromozom", ["Toate"] + all_chromosomes)
    with f3:
        min_quality = st.slider(
            "Calitate minima",
            min_value=0.0,
            max_value=max((v.quality for v in variants), default=100.0),
            value=0.0
        )

    filtered = filter_variants(
        variants,
        variant_type=None if selected_type == "Toate" else selected_type,
        chromosome=None if selected_chromosome == "Toate" else selected_chromosome,
        min_quality=min_quality
    )

    if not filtered:
        st.info("Nicio varianta nu corespunde filtrelor selectate.")
    else:
        df = pd.DataFrame([{
            "Cromozom": v.chromosome,
            "Pozitie": v.position,
            "REF": v.reference,
            "ALT": v.alternative,
            "Tip": v.type,
            "Calitate": v.quality,
            "Filtru": v.filter,
        } for v in filtered])
        st.dataframe(df, width="stretch", hide_index=True)
        st.caption(f"{len(filtered)} din {len(variants)} variante afisate")

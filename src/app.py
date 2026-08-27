import streamlit as st
import pandas as pd
import plotly.express as px
from parser import parse_vcf
from analyzer import analyze_variants, filter_variants

st.set_page_config(page_title="Variant Analyzer", layout="wide")
st.title("🧬 Variant Analyzer")

uploaded_file = st.file_uploader("Încarcă un fișier VCF", type=["vcf", "vcf.gz"])

file_path = None
if uploaded_file is not None:
    file_path = f"/tmp/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
else:
    file_path = "../data/example.vcf"
    st.info(f"Niciun fișier încărcat — se folosește exemplul implicit ({file_path})")

variants = parse_vcf(file_path)
statistics = analyze_variants(variants)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total variante", statistics["total"])
col2.metric("SNP-uri", statistics["snps"])
col3.metric("Inserții", statistics["insertions"])
col4.metric("Deleții", statistics["deletions"])
col5.metric("PASS", statistics["passed"])

st.subheader("Grafice")
g1, g2 = st.columns(2)

df_all = pd.DataFrame([
    {
        "Cromozom": v.chromosome,
        "Poziție": v.position,
        "Tip": (
            "SNP" if len(v.reference) == 1 and len(v.alternative) == 1
            else "Inserție" if len(v.alternative) > len(v.reference)
            else "Deleție"
        ),
        "Calitate": v.quality,
    }
    for v in variants
])

with g1:
    tip_counts = df_all["Tip"].value_counts().reset_index()
    tip_counts.columns = ["Tip", "Număr"]
    fig_pie = px.pie(tip_counts, names="Tip", values="Număr", title="Distribuția tipurilor de variante")
    st.plotly_chart(fig_pie, use_container_width=True)

with g2:
    fig_hist = px.histogram(df_all, x="Calitate", nbins=20, title="Distribuția calității variantelor")
    st.plotly_chart(fig_hist, use_container_width=True)
    
st.subheader("Filtre")
c1, c2, c3 = st.columns(3)
variant_type = c1.selectbox("Tip variantă", ["Toate", "SNP", "INS", "DEL"])
chromosome = c2.text_input("Cromozom (ex: 12)", "")
min_quality = c3.number_input("Calitate minimă", value=0, step=1)

filtered = filter_variants(
    variants,
    variant_type=None if variant_type == "Toate" else variant_type,
    chromosome=chromosome if chromosome else None,
    min_quality=min_quality,
)

st.subheader(f"Variante filtrate ({len(filtered)})")
if filtered:
    df = pd.DataFrame([
        {
            "Cromozom": v.chromosome,
            "Poziție": v.position,
            "Ref": v.reference,
            "Alt": v.alternative,
            "Calitate": v.quality,
        }
        for v in filtered
    ])
    st.dataframe(df, use_container_width=True)
else:
    st.warning("Nicio variantă nu corespunde filtrelor selectate.")
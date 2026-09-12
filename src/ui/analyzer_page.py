import os
import streamlit as st
import pandas as pd
import plotly.express as px

from parser import parse_vcf
from analyzer import analyze_variants, filter_variants
from i18n import t
from ui.interpretation import render_interpretation


def render_analyzer():
    st.title(t("home_title"))

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    uploaded_file = st.file_uploader(t("upload_label"), type=["vcf", "vcf.gz"])

    if uploaded_file is not None:
        file_path = f"/tmp/{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    else:
        file_path = os.path.join(BASE_DIR, "..", "data", "example.vcf")
        st.info(t("upload_info", path=file_path))

    variants = parse_vcf(file_path)
    statistics = analyze_variants(variants)

    st.subheader(t("stats_header"))
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(t("stat_total"), statistics["total"])
    col2.metric(t("stat_snps"), statistics["snps"])
    col3.metric(t("stat_ins"), statistics["insertions"])
    col4.metric(t("stat_del"), statistics["deletions"])
    col5.metric(t("stat_pass"), statistics["passed"])

    render_interpretation(statistics, variants)

    st.subheader(t("charts_header"))
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
        fig_pie = px.pie(tip_counts, names="Tip", values="Număr", title=t("chart_pie_title"))
        st.plotly_chart(fig_pie, width="stretch")

    with g2:
        fig_hist = px.histogram(df_all, x="Calitate", nbins=20, title=t("chart_hist_title"))
        st.plotly_chart(fig_hist, width="stretch")

    st.subheader(t("filters_header"))
    c1, c2, c3 = st.columns(3)
    variant_type = c1.selectbox(t("filter_type"), [t("filter_all"), "SNP", "INS", "DEL"])
    chromosome = c2.text_input(t("filter_chrom"), "")
    min_quality = c3.number_input(t("filter_quality"), value=0, step=1)

    TYPE_MAP = {"INS": "Insertion", "DEL": "Deletion"}
    filtered = filter_variants(
        variants,
        variant_type=None if variant_type == t("filter_all") else TYPE_MAP.get(variant_type, variant_type),
        chromosome=chromosome if chromosome else None,
        min_quality=min_quality,
    )

    st.subheader(t("filtered_header", n=len(filtered)))
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
        st.dataframe(df, width="stretch")

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(t("download_csv"), csv, "variante_filtrate.csv", "text/csv")
    else:
        st.warning(t("no_results"))

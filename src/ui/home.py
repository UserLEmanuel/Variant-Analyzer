import streamlit as st
from i18n import t
from ui.vcf_explainer import render_vcf_explainer


def render_home():
    st.title(t("home_title"))

    st.header(t("section_dna_header"))
    st.write(t("section_dna_text"))

    st.header(t("section_genome_header"))
    st.write(t("section_genome_text"))

    st.header(t("section_variant_header"))
    st.write(t("section_variant_text"))

    st.header(t("home_intro_header"))
    st.write(t("home_intro_text"))
    
    render_vcf_explainer()

    st.header(t("home_types_header"))
    c1, c2, c3 = st.columns(3)

    card_style = "padding:20px; border-radius:12px; height:100%;"

    with c1:
        st.markdown(
            f'<div style="background-color:#E8F0FE; {card_style}">'
            f'<h4>🔵 SNP</h4><p>{t("home_snp_desc")}</p></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div style="background-color:#E6F4EA; {card_style}">'
            f'<h4>🟢 {t("type_ins")}</h4><p>{t("home_ins_desc")}</p></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f'<div style="background-color:#FCE8E6; {card_style}">'
            f'<h4>🔴 {t("type_del")}</h4><p>{t("home_del_desc")}</p></div>',
            unsafe_allow_html=True,
        )

    st.write("")
    st.info(t("home_cta"))
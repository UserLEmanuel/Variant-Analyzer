import streamlit as st
from i18n import t

VCF_FIELDS = ["CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO"]
EXAMPLE_VALUES = {
    "CHROM": "12",
    "POS": "345678",
    "ID": ".",
    "REF": "A",
    "ALT": "G",
    "QUAL": "99",
    "FILTER": "PASS",
    "INFO": "DP=30",
}


def _set_field(field):
    st.session_state.vcf_field = field


def render_vcf_explainer():
    st.header(t("vcf_explainer_header"))
    st.write(t("vcf_explainer_intro"))

    if "vcf_field" not in st.session_state:
        st.session_state.vcf_field = "CHROM"

    cols = st.columns(len(VCF_FIELDS))
    for i, field in enumerate(VCF_FIELDS):
        with cols[i]:
            st.caption(field)
            st.button(
                EXAMPLE_VALUES[field],
                key=f"vcf_field_btn_{field}",
                on_click=_set_field,
                args=(field,),
                type="primary" if st.session_state.vcf_field == field else "secondary",
                width="stretch",
            )

    selected = st.session_state.vcf_field
    st.info(f"**{selected}** — {t(f'vcf_field_{selected.lower()}')}")

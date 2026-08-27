import streamlit as st
from i18n import t


def _quality_level_key(avg_quality):
    if avg_quality >= 30:
        return "quality_high"
    elif avg_quality >= 20:
        return "quality_moderate"
    return "quality_low"


def render_interpretation(statistics, variants):
    st.header(t("interpretation_header"))

    total = statistics["total"]
    if total == 0:
        return

    avg_quality = sum(v.quality for v in variants) / total
    pass_pct = round(statistics["passed"] / total * 100)
    quality_level = t(_quality_level_key(avg_quality))

    text = t(
        "interpretation_text",
        total=total,
        snps=statistics["snps"],
        ins=statistics["insertions"],
        dels=statistics["deletions"],
        passed=statistics["passed"],
        pass_pct=pass_pct,
        avg_quality=round(avg_quality, 1),
        quality_level=quality_level,
    )
    st.info(text)
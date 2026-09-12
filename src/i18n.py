import streamlit as st

TEXTS = {
    "en": {
        "nav_home": "Theory",
        "nav_analyzer": "Analyzer",
        "home_title": "🧬 Variant Analyzer",

        "section_dna_header": "What is DNA?",
        "section_dna_text": (
            "DNA (deoxyribonucleic acid) is the molecule that carries the instructions "
            "for building and running every living thing. It's made of a long sequence "
            "of just four letters — **A, T, C, G** — repeated billions of times. "
            "The exact order of those letters is what makes you, you."
        ),

        "section_genome_header": "What is a gene and a genome?",
        "section_genome_text": (
            "A **gene** is a specific stretch of DNA that contains instructions for one "
            "particular trait or function — for example, eye color. A **genome** is the "
            "complete set of DNA in an organism: all the genes and everything in between, "
            "billions of letters long."
        ),

        "section_variant_header": "What is a genetic variant?",
        "section_variant_text": (
            "No two people have identical DNA. When scientists compare someone's DNA to a "
            "standard **reference genome**, the differences they find are called "
            "**variants**. Most variants are harmless, some explain traits like hair color, "
            "and some are linked to disease risk."
        ),

        "home_intro_header": "What is a VCF file?",
        "home_intro_text": (
            "A **VCF** (Variant Call Format) file is the standard way researchers store "
            "genetic variants found when comparing DNA to a reference genome.\n\n"
            "Each line in a VCF describes one variant: where it occurs (chromosome, "
            "position), what was there before (reference), what changed (alternative), "
            "and a quality score showing how confident the detection is."
        ),

        "home_types_header": "Common variant types",
        "type_ins": "Insertion",
        "type_del": "Deletion",
        "home_snp_desc": "A single DNA letter changes (e.g. A → G).",
        "home_ins_desc": "Extra letters are added compared to the reference.",
        "home_del_desc": "Letters are missing compared to the reference.",
        "home_cta": "Click **Analyzer** in the top menu to upload your own VCF file or explore an example.",

        "upload_label": "Upload a VCF file",
        "upload_info": "No file uploaded — using default example ({path})",
        "stats_header": "Statistics",
        "stat_total": "Total variants",
        "stat_snps": "SNPs",
        "stat_ins": "Insertions",
        "stat_del": "Deletions",
        "stat_pass": "PASS",
        "charts_header": "Charts",
        "chart_pie_title": "Variant type distribution",
        "chart_hist_title": "Variant quality distribution",
        "filters_header": "Filters",
        "filter_type": "Variant type",
        "filter_all": "All",
        "filter_chrom": "Chromosome (e.g. 12)",
        "filter_quality": "Minimum quality",
        "filtered_header": "Filtered variants ({n})",
        "no_results": "No variant matches the selected filters.",
        "download_csv": "⬇️ Download CSV",

        "vcf_explainer_header": "Explore a VCF line",
        "vcf_explainer_intro": "Click each column below to see what it means. This is one real line from a VCF file.",
        "vcf_field_chrom": "The chromosome where this variant was found (e.g. chromosome 12).",
        "vcf_field_pos": "The exact position (base pair) on the chromosome where the variant starts.",
        "vcf_field_id": "An identifier for the variant, if it's already known in a database (e.g. dbSNP). A dot means it's not catalogued.",
        "vcf_field_ref": "The reference base(s) — what's expected at this position in a standard genome.",
        "vcf_field_alt": "The alternative base(s) — what was actually found instead of the reference.",
        "vcf_field_qual": "A quality score (Phred-scaled) showing how confident the variant caller is. Higher is better.",
        "vcf_field_filter": "Whether this variant passed quality filters. 'PASS' means yes.",
        "vcf_field_info": "Extra details about the variant, like sequencing depth (DP) or allele frequency (AF).",

        "interpretation_header": "What does this mean?",
        "interpretation_text": (
            "This file contains **{total}** variants: {snps} SNPs, {ins} insertions, and "
            "{dels} deletions. **{passed}** out of {total} variants passed quality filters "
            "({pass_pct}%). The average variant quality is **{avg_quality}**, which is "
            "considered **{quality_level}**."
        ),
        "quality_high": "high confidence",
        "quality_moderate": "moderate confidence",
        "quality_low": "low confidence — interpret with caution",
    },
    "ro": {
        "nav_home": "Teorie",
        "nav_analyzer": "Analiză",
        "home_title": "🧬 Variant Analyzer",

        "section_dna_header": "Ce este ADN-ul?",
        "section_dna_text": (
            "ADN-ul (acidul dezoxiribonucleic) este molecula care poartă instrucțiunile "
            "pentru construirea și funcționarea oricărei ființe vii. Este format dintr-o "
            "secvență lungă de doar patru litere — **A, T, C, G** — repetate de miliarde "
            "de ori. Ordinea exactă a acestor litere e ceea ce te face pe tine, tu."
        ),

        "section_genome_header": "Ce este o genă și un genom?",
        "section_genome_text": (
            "O **genă** este o porțiune specifică de ADN care conține instrucțiuni pentru "
            "o anumită trăsătură sau funcție — de exemplu, culoarea ochilor. Un **genom** "
            "este întreaga colecție de ADN a unui organism: toate genele și tot ce e "
            "între ele, lung de miliarde de litere."
        ),

        "section_variant_header": "Ce este o variantă genetică?",
        "section_variant_text": (
            "Nu există doi oameni cu ADN identic. Când cercetătorii compară ADN-ul cuiva "
            "cu un **genom de referință** standard, diferențele găsite se numesc "
            "**variante**. Majoritatea variantelor sunt inofensive, unele explică "
            "trăsături precum culoarea părului, iar altele sunt legate de riscul de boală."
        ),

        "home_intro_header": "Ce este un fișier VCF?",
        "home_intro_text": (
            "Un fișier **VCF** (Variant Call Format) este modul standard prin care "
            "cercetătorii stochează variantele genetice găsite atunci când ADN-ul este "
            "comparat cu un genom de referință.\n\n"
            "Fiecare linie dintr-un VCF descrie o variantă: unde apare (cromozom, "
            "poziție), ce era înainte (referință) și ce s-a schimbat (alternativă), plus "
            "un scor de calitate care spune cât de sigură e detecția."
        ),

        "home_types_header": "Tipuri comune de variante",
        "type_ins": "Inserție",
        "type_del": "Deleție",
        "home_snp_desc": "O singură literă din ADN se schimbă (ex: A → G).",
        "home_ins_desc": "Se adaugă litere suplimentare față de referință.",
        "home_del_desc": "Lipsesc litere față de referință.",
        "home_cta": "Apasă pe **Analiză** din meniul de sus ca să încarci propriul fișier VCF sau să explorezi un exemplu.",

        "upload_label": "Încarcă un fișier VCF",
        "upload_info": "Niciun fișier încărcat — se folosește exemplul implicit ({path})",
        "stats_header": "Statistici",
        "stat_total": "Total variante",
        "stat_snps": "SNP-uri",
        "stat_ins": "Inserții",
        "stat_del": "Deleții",
        "stat_pass": "PASS",
        "charts_header": "Grafice",
        "chart_pie_title": "Distribuția tipurilor de variante",
        "chart_hist_title": "Distribuția calității variantelor",
        "filters_header": "Filtre",
        "filter_type": "Tip variantă",
        "filter_all": "Toate",
        "filter_chrom": "Cromozom (ex: 12)",
        "filter_quality": "Calitate minimă",
        "filtered_header": "Variante filtrate ({n})",
        "no_results": "Nicio variantă nu corespunde filtrelor selectate.",
        "download_csv": "⬇️ Descarcă CSV",

        "vcf_explainer_header": "Explorează o linie VCF",
        "vcf_explainer_intro": "Apasă pe fiecare coloană de mai jos ca să vezi ce înseamnă. Aceasta este o linie reală dintr-un fișier VCF.",
        "vcf_field_chrom": "Cromozomul pe care a fost găsită această variantă (ex: cromozomul 12).",
        "vcf_field_pos": "Poziția exactă (perechea de baze) de pe cromozom unde începe varianta.",
        "vcf_field_id": "Un identificator pentru variantă, dacă e deja cunoscută într-o bază de date (ex: dbSNP). Un punct înseamnă că nu e catalogată.",
        "vcf_field_ref": "Baza/bazele de referință — ce se așteaptă la această poziție într-un genom standard.",
        "vcf_field_alt": "Baza/bazele alternative — ce s-a găsit de fapt în locul referinței.",
        "vcf_field_qual": "Un scor de calitate (scală Phred) care arată cât de sigur e algoritmul de detecție. Mai mare e mai bine.",
        "vcf_field_filter": "Dacă această variantă a trecut de filtrele de calitate. 'PASS' înseamnă da.",
        "vcf_field_info": "Detalii suplimentare despre variantă, precum adâncimea secvențierii (DP) sau frecvența alelei (AF).",

        "interpretation_header": "Ce înseamnă asta?",
        "interpretation_text": (
            "Acest fișier conține **{total}** variante: {snps} SNP-uri, {ins} inserții și "
            "{dels} deleții. **{passed}** din {total} variante au trecut de filtrele de "
            "calitate ({pass_pct}%). Calitatea medie a variantelor este **{avg_quality}**, "
            "considerată **{quality_level}**."
        ),
        "quality_high": "încredere ridicată",
        "quality_moderate": "încredere moderată",
        "quality_low": "încredere scăzută — interpretează cu prudență",
    },
}


def t(key, **kwargs):
    lang = st.session_state.get("lang", "en")
    text = TEXTS[lang].get(key, key)
    return text.format(**kwargs) if kwargs else text

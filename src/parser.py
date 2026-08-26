import cyvcf2
from models import Variant

def parse_vcf(file_path):
    variants = []

    for record in cyvcf2.VCF(file_path):
        chromosome = record.CHROM
        position = record.POS
        reference = record.REF
        alternative = record.ALT[0]  # primul ALT, dacă sunt mai multe
        quality = record.QUAL if record.QUAL is not None else 0.0
        filter_status = record.FILTER if record.FILTER is not None else "PASS"

        variant_type = classify_variant(reference, alternative)

        variant = Variant(
            chromosome=chromosome,
            position=position,
            reference=reference,
            alternative=alternative,
            quality=quality,
            filter=filter_status,
            type=variant_type
        )
        variants.append(variant)

    return variants


def classify_variant(reference, alternative):
    if len(reference) == 1 and len(alternative) == 1:
        return "SNP"
    if len(reference) < len(alternative):
        return "Insertion"
    if len(reference) > len(alternative):
        return "Deletion"
    return "Other"
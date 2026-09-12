import gzip
from models import Variant


def _open_vcf(file_path):
    if file_path.endswith(".gz"):
        return gzip.open(file_path, "rt")
    return open(file_path, "r")


def parse_vcf(file_path):
    variants = []

    with _open_vcf(file_path) as vcf_file:
        for line in vcf_file:
            line = line.strip()

            # ## = linie de metadate, # CHROM... = header-ul coloanelor
            if not line or line.startswith("#"):
                continue

            fields = line.split("\t")
            chromosome, position, _id, reference, alt_field, qual, filter_field = fields[:7]

            alternative = alt_field.split(",")[0]  # primul ALT, dacă sunt mai multe

            quality = 0.0 if qual == "." else float(qual)
            filter_status = "PASS" if filter_field in (".", "") else filter_field

            variant_type = classify_variant(reference, alternative)

            variant = Variant(
                chromosome=chromosome,
                position=int(position),
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

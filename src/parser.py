from models import Variant


def parse_vcf(file_path):
    variants = []

    with open(file_path, "r") as file:
        for line in file:

            if line.startswith("#"):
                continue

            columns = line.strip().split()

            chromosome = columns[0]
            position = int(columns[1])
            reference = columns[3]
            alternative = columns[4]
            quality = float(columns[5])
            filter_status = columns[6]

            variant_type = classify_variant(
                reference,
                alternative
            )

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
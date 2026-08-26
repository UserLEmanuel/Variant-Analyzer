from models import Variant


def classify_variant(ref, alt):
    if len(ref) == 1 and len(alt) == 1:
        return "SNP"

    elif len(ref) < len(alt):
        return "Insertion"

    elif len(ref) > len(alt):
        return "Deletion"

    return "Other"


def analyze_vcf(file_path):
    total_variants = 0
    snp_count = 0
    insertion_count = 0
    deletion_count = 0

    chromosome_counts = {}
    variants = []

    with open(file_path, "r") as file:
        for line in file:

            if line.startswith("#"):
                continue

            columns = line.strip().split("\t")

            chrom = columns[0]
            pos = int(columns[1])
            ref = columns[3]
            alt = columns[4]
            quality = float(columns[5])
            filter_status = columns[6]

            variant_type = classify_variant(ref, alt)

            variant = Variant(
                chromosome=chrom,
                position=pos,
                reference=ref,
                alternative=alt,
                quality=quality,
                filter=filter_status,
                type=variant_type
            )

            variants.append(variant)

            total_variants += 1

            if variant_type == "SNP":
                snp_count += 1

            elif variant_type == "Insertion":
                insertion_count += 1

            elif variant_type == "Deletion":
                deletion_count += 1

            if chrom not in chromosome_counts:
                chromosome_counts[chrom] = 0

            chromosome_counts[chrom] += 1

    statistics = {
        "total_variants": total_variants,
        "snp": snp_count,
        "insertions": insertion_count,
        "deletions": deletion_count,
        "chromosomes": chromosome_counts
    }

    return variants, statistics
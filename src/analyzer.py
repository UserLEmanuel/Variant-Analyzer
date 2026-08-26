from models import Variant


def analyze_variants(variants):
    statistics = {
        "total": len(variants),
        "snps": 0,
        "insertions": 0,
        "deletions": 0,
        "passed": 0
    }

    for variant in variants:

        if variant.type == "SNP":
            statistics["snps"] += 1

        elif variant.type == "Insertion":
            statistics["insertions"] += 1

        elif variant.type == "Deletion":
            statistics["deletions"] += 1

        if variant.filter == "PASS":
            statistics["passed"] += 1

    return statistics


def filter_variants(
    variants,
    variant_type=None,
    chromosome=None,
    min_quality=None
):
    filtered_variants = []

    for variant in variants:

        if variant_type is not None:
            if variant.type != variant_type:
                continue

        if chromosome is not None:
            if variant.chromosome != chromosome:
                continue

        if min_quality is not None:
            if variant.quality < min_quality:
                continue

        filtered_variants.append(variant)

    return filtered_variants
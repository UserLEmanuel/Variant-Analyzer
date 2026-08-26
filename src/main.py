from parser import parse_vcf
from analyzer import analyze_variants, filter_variants


def main():

    file_path = "../data/example.vcf"

    variants = parse_vcf(file_path)

    statistics = analyze_variants(variants)

    filtered_variants = filter_variants(
        variants,
        variant_type="SNP",
        chromosome="12",
        min_quality=80
    )

    print("=== STATISTICI ===")

    print(f"Total variante: {statistics['total']}")
    print(f"SNP-uri: {statistics['snps']}")
    print(f"Inserții: {statistics['insertions']}")
    print(f"Deleții: {statistics['deletions']}")
    print(f"PASS: {statistics['passed']}")

    print("\n=== VARIANTE FILTRATE ===")

    for variant in filtered_variants:
        print(
            f"{variant.chromosome}:"
            f"{variant.position} "
            f"{variant.reference} -> "
            f"{variant.alternative} "
            f"QUAL={variant.quality}"
        )


if __name__ == "__main__":
    main()
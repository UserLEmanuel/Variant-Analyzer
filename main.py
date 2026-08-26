from analyzer import analyze_vcf


def main():
    file_path = "../data/example.vcf"

    variants, statistics = analyze_vcf(file_path)

    print("Total variante:", statistics["total_variants"])
    print("SNP-uri:", statistics["snp"])
    print("Inserții:", statistics["insertions"])
    print("Deleții:", statistics["deletions"])

    print("\nVariante pe cromozom:")

    for chrom, count in statistics["chromosomes"].items():
        print(f"Cromozomul {chrom}: {count}")

    print("\nPrimele variante:")

    for variant in variants[:5]:
        print(
            f"{variant.chromosome}:"
            f"{variant.position} "
            f"{variant.reference} -> {variant.alternative} "
            f"({variant.type})"
        )


if __name__ == "__main__":
    main()
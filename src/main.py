import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from parser import parse_vcf
from analyzer import analyze_variants, filter_variants

console = Console()

DEFAULT_VCF = Path(__file__).resolve().parent.parent / "data" / "example.vcf"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Analizeaza variante genetice dintr-un fisier VCF."
    )
    parser.add_argument(
        "--file", "-f",
        default=str(DEFAULT_VCF),
        help=f"Calea catre fisierul VCF (implicit: {DEFAULT_VCF})"
    )
    parser.add_argument(
        "--type", "-t",
        default="SNP",
        help="Tip de varianta pentru filtrare (SNP, Insertion, Deletion). Foloseste 'all' pentru a dezactiva."
    )
    parser.add_argument(
        "--chromosome", "-c",
        default="12",
        help="Cromozomul pentru filtrare. Foloseste 'all' pentru a dezactiva."
    )
    parser.add_argument(
        "--min-quality", "-q",
        type=float,
        default=80,
        help="Calitatea minima (QUAL) pentru filtrare (implicit: 80)"
    )
    return parser.parse_args()


def print_statistics(statistics):
    table = Table(title="Statistici variante", show_header=True, header_style="bold cyan")
    table.add_column("Categorie")
    table.add_column("Numar", justify="right")

    table.add_row("Total variante", str(statistics["total"]))
    table.add_row("SNP-uri", str(statistics["snps"]))
    table.add_row("Insertii", str(statistics["insertions"]))
    table.add_row("Deletii", str(statistics["deletions"]))
    table.add_row("PASS", f"[green]{statistics['passed']}[/green]")

    console.print(table)


def print_variants(variants, title):
    table = Table(title=title, show_header=True, header_style="bold cyan")
    table.add_column("Cromozom")
    table.add_column("Pozitie", justify="right")
    table.add_column("REF -> ALT")
    table.add_column("Calitate", justify="right")

    if not variants:
        console.print(f"[yellow]Nicio varianta nu corespunde filtrelor aplicate.[/yellow]")
        return

    for variant in variants:
        quality_style = "green" if variant.quality >= 90 else "yellow" if variant.quality >= 70 else "red"
        table.add_row(
            variant.chromosome,
            str(variant.position),
            f"{variant.reference} -> {variant.alternative}",
            f"[{quality_style}]{variant.quality:g}[/{quality_style}]"
        )

    console.print(table)


def main():
    args = parse_args()

    console.print(Panel.fit("[bold]Variant Analyzer[/bold]", border_style="cyan"))

    try:
        variants = parse_vcf(args.file)
    except FileNotFoundError:
        console.print(f"[bold red]Eroare:[/bold red] fisierul '{args.file}' nu a fost gasit.")
        sys.exit(1)
    except (ValueError, IndexError) as error:
        console.print(f"[bold red]Eroare la citirea fisierului VCF:[/bold red] {error}")
        sys.exit(1)

    if not variants:
        console.print("[yellow]Fisierul VCF nu contine variante.[/yellow]")
        sys.exit(0)

    statistics = analyze_variants(variants)
    print_statistics(statistics)

    variant_type = None if args.type.lower() == "all" else args.type
    chromosome = None if args.chromosome.lower() == "all" else args.chromosome

    filtered_variants = filter_variants(
        variants,
        variant_type=variant_type,
        chromosome=chromosome,
        min_quality=args.min_quality
    )

    filter_description = (
        f"tip={variant_type or 'toate'}, cromozom={chromosome or 'toti'}, "
        f"calitate minima={args.min_quality}"
    )
    console.print()
    print_variants(filtered_variants, f"Variante filtrate ({filter_description})")


if __name__ == "__main__":
    main()

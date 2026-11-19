"""Calcula indicadores de campanhas a partir de um CSV local."""

import argparse
import csv
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path


@dataclass
class Totais:
    investimento: Decimal = Decimal(0)
    cliques: int = 0
    leads: int = 0

    def agregar(self, item: "Totais") -> None:
        self.investimento += item.investimento
        self.cliques += item.cliques
        self.leads += item.leads


def ler_campanhas(arquivo: Path) -> dict[str, Totais]:
    por_canal: dict[str, Totais] = {}
    with arquivo.open(encoding="utf-8-sig", newline="") as entrada:
        leitor = csv.DictReader(entrada)
        if not {"canal", "investimento", "cliques", "leads"}.issubset(leitor.fieldnames or []):
            raise ValueError("Cabeçalho obrigatório: canal,investimento,cliques,leads")
        for linha in leitor:
            try:
                canal = (linha["canal"] or "").strip()
                custo = Decimal(linha["investimento"] or "")
                cliques = int(linha["cliques"] or "")
                leads = int(linha["leads"] or "")
                if not canal or not custo.is_finite() or custo < 0 or not 0 <= leads <= cliques:
                    raise ValueError
            except (InvalidOperation, ValueError) as erro:
                raise ValueError(f"Linha {leitor.line_num}: valores inválidos.") from erro
            por_canal.setdefault(canal, Totais()).agregar(Totais(custo, cliques, leads))
    return por_canal


def dividir(numerador: Decimal, denominador: int, sufixo: str = "") -> str:
    return f"{numerador / denominador:.2f}{sufixo}" if denominador else "—"


def formatar(canal: str, totais: Totais) -> str:
    cpc = dividir(totais.investimento, totais.cliques)
    cpl = dividir(totais.investimento, totais.leads)
    conversao = dividir(Decimal(totais.leads) * 100, totais.cliques, "%")
    return (f"{canal:<16} {totais.investimento:>14.2f} {totais.cliques:>8}"
            f" {totais.leads:>8} {cpc:>9} {cpl:>9} {conversao:>10}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path, help="Arquivo de campanhas")
    args = parser.parse_args()
    try:
        por_canal = ler_campanhas(args.csv)
    except (OSError, ValueError, csv.Error) as erro:
        parser.exit(1, f"Erro: {erro}\n")

    total = Totais()
    print(f"{'Canal':<16} {'Invest. (R$)':>14} {'Cliques':>8} {'Leads':>8}"
          f" {'CPC (R$)':>9} {'CPL (R$)':>9} {'Conversão':>10}")
    for canal, valores in sorted(por_canal.items()):
        print(formatar(canal, valores))
        total.agregar(valores)
    print(formatar("Total", total))


if __name__ == "__main__":
    main()

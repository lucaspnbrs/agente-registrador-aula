from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass
class AulaPlanejada:
    data: date
    turma: str
    disciplina: str
    hora_inicial: str
    hora_final: str
    conteudo_abordado: str


def carregar_aulas_planejadas(caminho_csv: Path) -> list[AulaPlanejada]:
    with caminho_csv.open(newline="", encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        return [
            AulaPlanejada(
                data=date.fromisoformat(linha["data"]),
                turma=linha["turma"],
                disciplina=linha["disciplina"],
                hora_inicial=linha["hora_inicial"],
                hora_final=linha["hora_final"],
                conteudo_abordado=linha["conteudo_abordado"],
            )
            for linha in leitor
        ]

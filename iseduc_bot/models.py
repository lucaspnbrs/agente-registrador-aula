from __future__ import annotations

from datetime import date, time
from typing import Optional

from pydantic import BaseModel, Field


class Disciplina(BaseModel):
    id_disciplina: int = Field(alias="idDisciplina")
    nome: str = Field(alias="Nome")

    model_config = {"populate_by_name": True}


class Turma(BaseModel):
    nome: str = Field(alias="Nome")

    model_config = {"populate_by_name": True}


class Aula(BaseModel):
    """Formato confirmado a partir da resposta real de criação de aula."""

    id: Optional[int] = None
    disciplina: Disciplina
    turma: Turma
    data: date
    hora_inicial: time = Field(alias="horaInicial")
    hora_final: time = Field(alias="horaFinal")

    model_config = {"populate_by_name": True}


class NovaAulaPayload(BaseModel):
    # Nomes de campo abaixo são inferidos a partir da resposta de criação de aula
    # (que usa idDisciplina/Nome) — confirmar contra o payload real capturado via cURL.
    tipo_aula: str = Field(alias="tipoAula")
    id_turma: int = Field(alias="idTurma")
    id_disciplina: int = Field(alias="idDisciplina")
    data: date
    hora_inicial: time = Field(alias="horaInicial")
    hora_final: time = Field(alias="horaFinal")

    model_config = {"populate_by_name": True}


class AlunoFrequencia(BaseModel):
    id_frequencia_aluno: int = Field(alias="idFrequenciaAluno")
    id_aula: int = Field(alias="idAula")
    id_justificativa_falta: Optional[int] = Field(default=None, alias="idJustificativaFalta")
    # Nome do aluno vem na resposta real, mas o campo exato ainda não foi confirmado.
    nome_aluno: Optional[str] = Field(default=None, alias="nomeAluno")

    model_config = {"populate_by_name": True}

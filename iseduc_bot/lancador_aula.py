from __future__ import annotations

import time
from datetime import date

from .api_client import ISEDUCClient
from .fonte_dados import AulaPlanejada
from .models import NovaAulaPayload

DELAY_ENTRE_REQUISICOES_SEGUNDOS = 2.0


def lancar_aula(client: ISEDUCClient, planejada: AulaPlanejada) -> None:
    if planejada.data > date.today():
        raise ValueError("ISEDUC não aceita data futura para registro de aula.")

    payload = NovaAulaPayload(
        tipoAula="Aula Normal",
        idTurma=_resolver_id_turma(planejada.turma),
        idDisciplina=_resolver_id_disciplina(planejada.disciplina),
        data=planejada.data,
        horaInicial=planejada.hora_inicial,
        horaFinal=planejada.hora_final,
    )
    aula = client.criar_aula(payload)
    time.sleep(DELAY_ENTRE_REQUISICOES_SEGUNDOS)

    client.salvar_registro_pedagogico(aula.id, {"conteudoAbordado": planejada.conteudo_abordado})
    time.sleep(DELAY_ENTRE_REQUISICOES_SEGUNDOS)

    # TODO: aplicar frequência (client.listar_frequencia + client.atualizar_frequencia por aluno)
    # TODO: salvar recursos didáticos (client.salvar_recursos_didaticos)
    # TODO: salvar atividade e finalizar (client.salvar_atividade)


def _resolver_id_turma(nome_turma: str) -> int:
    raise NotImplementedError("Mapeamento turma -> idTurma ainda não definido.")


def _resolver_id_disciplina(nome_disciplina: str) -> int:
    raise NotImplementedError("Mapeamento disciplina -> idDisciplina ainda não definido.")

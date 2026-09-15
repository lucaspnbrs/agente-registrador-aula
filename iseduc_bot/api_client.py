from __future__ import annotations

from .auth import ISEDUCAuth
from .models import Aula, AlunoFrequencia, NovaAulaPayload

# None = endpoint ainda não capturado. Preencher com a URL real (path relativo à base_url)
# conforme for mapeado via DevTools + tools/curl_to_request.py.
ENDPOINTS: dict[str, str | None] = {
    "listar_escolas": None,
    "listar_disciplinas": None,
    "criar_aula": None,
    "opcoes_encadeadas": None,  # competência/habilidade/objeto do conhecimento/etc.
    "salvar_registro_pedagogico": None,
    "listar_frequencia": None,
    "atualizar_frequencia": None,
    "salvar_recursos_didaticos": None,
    "salvar_atividade": None,
}


def endpoints_pendentes() -> list[str]:
    return [nome for nome, url in ENDPOINTS.items() if url is None]


class ISEDUCClient:
    def __init__(self, base_url: str) -> None:
        self.auth = ISEDUCAuth(base_url)
        self.client = self.auth.client

    def _exigir_endpoint(self, nome: str) -> str:
        url = ENDPOINTS[nome]
        if url is None:
            raise NotImplementedError(
                f"Endpoint '{nome}' ainda não mapeado. Capture o cURL correspondente "
                f"(ver tools/curl_to_request.py) e preencha ENDPOINTS['{nome}'] em api_client.py."
            )
        return url

    def criar_aula(self, payload: NovaAulaPayload) -> Aula:
        url = self._exigir_endpoint("criar_aula")
        resp = self.client.post(url, json=payload.model_dump(by_alias=True, mode="json"))
        resp.raise_for_status()
        return Aula.model_validate(resp.json())

    def listar_frequencia(self, id_aula: int) -> list[AlunoFrequencia]:
        url = self._exigir_endpoint("listar_frequencia")
        resp = self.client.get(url, params={"idAula": id_aula})
        resp.raise_for_status()
        return [AlunoFrequencia.model_validate(item) for item in resp.json()]

    def atualizar_frequencia(self, id_frequencia_aluno: int, presente: bool) -> None:
        url = self._exigir_endpoint("atualizar_frequencia")
        # Formato do payload ainda não confirmado (booleano "presente"? idJustificativaFalta?).
        # Ajustar conforme o cURL real capturado.
        resp = self.client.patch(
            url, json={"idFrequenciaAluno": id_frequencia_aluno, "presente": presente}
        )
        resp.raise_for_status()

    def salvar_registro_pedagogico(self, id_aula: int, campos: dict) -> None:
        url = self._exigir_endpoint("salvar_registro_pedagogico")
        resp = self.client.post(url, json={"idAula": id_aula, **campos})
        resp.raise_for_status()

    def salvar_recursos_didaticos(self, id_aula: int, campos: dict) -> None:
        url = self._exigir_endpoint("salvar_recursos_didaticos")
        resp = self.client.post(url, json={"idAula": id_aula, **campos})
        resp.raise_for_status()

    def salvar_atividade(self, id_aula: int, campos: dict) -> None:
        url = self._exigir_endpoint("salvar_atividade")
        resp = self.client.post(url, json={"idAula": id_aula, **campos})
        resp.raise_for_status()

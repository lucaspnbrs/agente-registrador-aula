from __future__ import annotations

import pickle
from pathlib import Path

import httpx

SESSION_FILE = Path(__file__).resolve().parent.parent / ".session_cookies.pkl"


class ISEDUCAuth:
    def __init__(self, base_url: str, client: httpx.Client | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.client = client or httpx.Client(base_url=self.base_url, timeout=30.0)
        self._carregar_sessao()

    def _carregar_sessao(self) -> None:
        if SESSION_FILE.exists():
            with SESSION_FILE.open("rb") as f:
                self.client.cookies.update(pickle.load(f))

    def _salvar_sessao(self) -> None:
        with SESSION_FILE.open("wb") as f:
            pickle.dump(dict(self.client.cookies), f)

    def login(self, cpf: str, senha: str) -> None:
        # Endpoint ainda não mapeado. Capture o cURL do POST de login no DevTools
        # (ver tools/curl_to_request.py) e substitua o bloco abaixo pela chamada real.
        raise NotImplementedError(
            "Endpoint de login ainda não mapeado — capture o cURL real e preencha ISEDUCAuth.login()."
        )
        # Formato esperado, uma vez capturado:
        # resp = self.client.post("/caminho/do/login", json={"cpf": cpf, "senha": senha})
        # resp.raise_for_status()
        # self._salvar_sessao()

    def selecionar_perfil(self, perfil: str = "Professor") -> None:
        raise NotImplementedError("Endpoint de seleção de perfil ainda não mapeado.")

    def abrir_escola(self, id_escola: int) -> None:
        raise NotImplementedError("Endpoint de abertura de escola ainda não mapeado.")

from __future__ import annotations

import os

import typer
from dotenv import load_dotenv

from iseduc_bot.api_client import ISEDUCClient, endpoints_pendentes

load_dotenv()

app = typer.Typer()


@app.command()
def status() -> None:
    """Mostra quais endpoints da API ainda faltam mapear."""
    pendentes = endpoints_pendentes()
    if not pendentes:
        typer.echo("Todos os endpoints estão mapeados.")
        return
    typer.echo("Endpoints ainda pendentes de captura (ver tools/curl_to_request.py):")
    for nome in pendentes:
        typer.echo(f"  - {nome}")


@app.command()
def lancar_aula_hoje() -> None:
    """Lança a aula planejada para hoje (requer endpoints mapeados)."""
    base_url = os.environ["ISEDUC_BASE_URL"]
    cpf = os.environ["ISEDUC_CPF"]
    senha = os.environ["ISEDUC_SENHA"]

    client = ISEDUCClient(base_url)
    client.auth.login(cpf, senha)
    # TODO: buscar a aula planejada de hoje via fonte_dados.carregar_aulas_planejadas
    # e chamar lancador_aula.lancar_aula(client, planejada)


if __name__ == "__main__":
    app()

"""Cola um comando cURL (copiado do DevTools -> Network -> Copy as cURL) via stdin
e imprime método, URL, headers (com Cookie/Authorization ocultos) e um snippet httpx
pronto pra colar em api_client.py. Uso: python tools/curl_to_request.py < curl.txt
"""
from __future__ import annotations

import json
import shlex
import sys
from urllib.parse import urlparse

CAMPOS_SENSIVEIS = {"cookie", "authorization"}


def parse_curl(comando: str) -> dict:
    tokens = shlex.split(comando.replace("\\\n", " "))
    if tokens and tokens[0] == "curl":
        tokens = tokens[1:]

    metodo = "GET"
    url = None
    headers: dict[str, str] = {}
    corpo = None

    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token in ("-X", "--request"):
            metodo = tokens[i + 1]
            i += 2
        elif token in ("-H", "--header"):
            chave, _, valor = tokens[i + 1].partition(": ")
            headers[chave] = valor
            i += 2
        elif token in ("-d", "--data", "--data-raw", "--data-binary"):
            corpo = tokens[i + 1]
            metodo = "POST" if metodo == "GET" else metodo
            i += 2
        elif token.startswith("http"):
            url = token
            i += 1
        else:
            i += 1

    return {"metodo": metodo, "url": url, "headers": headers, "corpo": corpo}


def _ocultar_sensiveis(headers: dict[str, str]) -> dict[str, str]:
    return {
        chave: ("***OCULTO***" if chave.lower() in CAMPOS_SENSIVEIS else valor)
        for chave, valor in headers.items()
    }


def gerar_snippet_httpx(info: dict) -> str:
    partes = urlparse(info["url"])
    caminho = partes.path + (f"?{partes.query}" if partes.query else "")

    linhas = [f'resp = client.{info["metodo"].lower()}(', f'    "{caminho}",']
    if info["corpo"]:
        try:
            corpo_json = json.loads(info["corpo"])
            linhas.append(f"    json={corpo_json!r},")
        except json.JSONDecodeError:
            linhas.append(f'    data="""{info["corpo"]}""",')
    linhas.append(")")
    return "\n".join(linhas)


def main() -> None:
    comando = sys.stdin.read().strip()
    if not comando:
        print("Nenhum comando recebido. Cole o cURL via stdin.", file=sys.stderr)
        return

    info = parse_curl(comando)
    print(f"Método: {info['metodo']}")
    print(f"URL: {info['url']}")
    print("Headers (sensíveis ocultos):")
    for chave, valor in _ocultar_sensiveis(info["headers"]).items():
        print(f"  {chave}: {valor}")
    if info["corpo"]:
        print("Corpo:")
        try:
            print(json.dumps(json.loads(info["corpo"]), indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print(info["corpo"])
    print("\nSnippet httpx sugerido:")
    print(gerar_snippet_httpx(info))


if __name__ == "__main__":
    main()

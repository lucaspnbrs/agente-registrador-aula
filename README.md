# ISEDUC Bot

Automação de lançamento de aulas, frequência e notas no sistema ISEDUC (SEDUC-PI), via Claude Code.

## Como usar

O projeto usa o `CLAUDE.md` como contexto fixo (fluxo mapeado, payloads de exemplo, endpoints). A partir daí, o fluxo de trabalho é conversacional: você descreve o que precisa lançar e o Claude Code gera os artefatos (CSV, scripts, chamadas de API) de acordo.

### Exemplo de prompt — gerar planilha de aulas

```
Preciso que você monte um csv agora para registrar aulas de 20 aulas de
fundamentos de UX/UI, pode colocar temas variados das aulas para a mesma
turma que você colocou antes

Os horários que eu dou aula na segunda são 14:10, na quarta 13:10 e 15:20,
na quinta 13:10 e 14:10 e na sexta 08:00, 10:10 e 11:10

Faça essa planilha e rode a partir da aula atual que você registrou, ou
seja do 2026-08-07 do horário de 10:10 em diante até dar 20 aulas
registradas e não leve em consideração 7 de setembro que foi feriado,
você entendeu?
```

**O que esse prompt gera:** um `aulas_ux_ui.csv` com 20 linhas, cada uma com `data`, `horaInicial`/`horaFinal`, `turma`, `componente`, `tipoAula` e `conteudoAbordado` (tema variado por aula), respeitando a grade semanal informada, começando no horário exato indicado e pulando feriados.

### Fluxo geral

1. Descreva o período e a grade de horários (dias da semana + horários)
2. Claude Code gera o CSV de aulas pendentes de lançamento
3. `lancador_aula.py` lê o CSV e cria as aulas via API, aula por aula
4. Frequência é registrada em seguida, por `idAula` retornado na criação
5. Notas seguem fluxo próprio (`lancador_notas.py`) — ainda em mapeamento

## Estrutura

```
agente-registra-aula/
├── CLAUDE.md           # contexto do projeto (fluxo, endpoints, payloads)
├── auth.py
├── api_client.py
├── models.py
├── fonte_dados.py
├── lancador_aula.py
├── lancador_notas.py
├── data/
│   └── aulas_ux_ui.csv
└── main.py
```

## Aviso

Projeto de uso pessoal para automatizar lançamentos em sistema de gestão pública (SEDUC-PI). Credenciais ficam em `.env` (nunca versionado). Requisições rodam com delays realistas para evitar comportamento não-humano detectável.

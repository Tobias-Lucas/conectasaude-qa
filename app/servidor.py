#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ConectaSaúde de laboratório: a API do RF-12 e duas telas.

Só biblioteca padrão do Python (3.8+). Nada para instalar.

    SENHA_TESTE=... python3 app/servidor.py          # porta 8800
    BUILD=v0.9 SENHA_TESTE=... python3 app/servidor.py

Rotas
    GET  /login           tela de login (data-testid: email, senha, entrar)
    POST /login           autentica e redireciona para /agenda
    GET  /agenda          tela de boas-vindas (data-testid: boas-vindas)
    POST /agendamento     a API do RF-12
    POST /_laboratorio/zerar   limpa a agenda entre execuções da suíte
    GET  /saude           ping, para o CI esperar o servidor subir
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import regras  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
PORTA = int(os.environ.get("PORTA", "8800"))

USUARIO = "mariana@conectasaude.test"
NOME = "Dra. Mariana"
SENHA = os.environ.get("SENHA_TESTE", "")

SEM_SENHA = """
ERRO: a variável de ambiente SENHA_TESTE está vazia.

A senha da Dra. Mariana não mora no código. Na sua máquina ela vem do
ambiente; na esteira, de um secret do repositório.

    export SENHA_TESTE='a-que-voce-escolher'
    python3 app/servidor.py

No GitHub Actions: Settings > Secrets and variables > Actions > New
repository secret, com o nome SENHA_TESTE.
"""


def pagina(nome):
    with open(os.path.join(AQUI, "web", nome), encoding="utf-8") as f:
        return f.read()


class Handler(BaseHTTPRequestHandler):
    server_version = "ConectaSaude/laboratorio"

    def log_message(self, formato, *args):
        sys.stderr.write("%s %s\n" % (self.address_string(), formato % args))

    # ------------------------------------------------------------------ util
    def _responder(self, status, corpo, tipo="application/json; charset=utf-8",
                   cabecalhos=()):
        if isinstance(corpo, (dict, list)):
            corpo = json.dumps(corpo, ensure_ascii=False, indent=2)
        dados = corpo.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(dados)))
        for chave, valor in cabecalhos:
            self.send_header(chave, valor)
        self.end_headers()
        self.wfile.write(dados)

    def _corpo(self):
        tamanho = int(self.headers.get("Content-Length") or 0)
        return self.rfile.read(tamanho) if tamanho else b""

    # -------------------------------------------------------------------- GET
    def do_GET(self):
        caminho = urlparse(self.path).path
        if caminho in ("/", "/login"):
            return self._responder(200, pagina("login.html"), "text/html; charset=utf-8")
        if caminho == "/agenda":
            if "sessao=ok" not in (self.headers.get("Cookie") or ""):
                return self._responder(
                    200, pagina("login.html").replace(
                        "<!--ERRO-->",
                        '<p class="erro" data-testid="erro">Faça login para ver a agenda.</p>'),
                    "text/html; charset=utf-8")
            html = pagina("agenda.html").replace("{{NOME}}", NOME).replace("{{BUILD}}", regras.BUILD)
            return self._responder(200, html, "text/html; charset=utf-8")
        if caminho == "/saude":
            return self._responder(200, {"ok": True, "build": regras.BUILD, "hoje": regras.HOJE})
        return self._responder(404, {"erro": "rota não encontrada"})

    # ------------------------------------------------------------------- POST
    def do_POST(self):
        partes = urlparse(self.path)
        caminho = partes.path

        if caminho == "/login":
            campos = parse_qs(self._corpo().decode("utf-8"))
            email = (campos.get("email") or [""])[0]
            senha = (campos.get("senha") or [""])[0]
            if email == USUARIO and senha == SENHA:
                return self._responder(
                    303, "", "text/plain; charset=utf-8",
                    [("Location", "/agenda"), ("Set-Cookie", "sessao=ok; Path=/")])
            html = pagina("login.html").replace(
                "<!--ERRO-->",
                '<p class="erro" data-testid="erro">Usuário ou senha inválidos.</p>')
            return self._responder(401, html, "text/html; charset=utf-8")

        if caminho == "/_laboratorio/zerar":
            regras.zerar()
            return self._responder(200, {"ok": True})

        if caminho == "/agendamento":
            try:
                pedido = json.loads(self._corpo().decode("utf-8") or "{}")
            except ValueError:
                return self._responder(422, {"erro": "corpo não é JSON válido"})
            if not isinstance(pedido, dict):
                return self._responder(422, {"erro": "corpo não é JSON válido"})

            # Stubs de laboratório: simulam falhas sem chamar serviços reais.
            # O C-11 usa whatsapp_429; o C-11b usa whatsapp_429,sms_503.
            simulacoes = set(
                parse_qs(partes.query).get("simular", [""])[0].split(",")
            )
            whatsapp_ok = "whatsapp_429" not in simulacoes
            sms_ok = "sms_503" not in simulacoes

            try:
                status, corpo = regras.agendar(
                    pedido, whatsapp_ok=whatsapp_ok, sms_ok=sms_ok)
            except regras.Recusado as recusa:
                return self._responder(recusa.status, {"erro": recusa.motivo})
            return self._responder(status, corpo)

        return self._responder(404, {"erro": "rota não encontrada"})


def main():
    if not SENHA:
        sys.stderr.write(SEM_SENHA)
        sys.exit(2)
    servidor = HTTPServer(("127.0.0.1", PORTA), Handler)
    sys.stderr.write(
        "ConectaSaude de laboratorio em http://127.0.0.1:%d  (build %s, hoje %s)\n"
        % (PORTA, regras.BUILD, regras.HOJE))
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

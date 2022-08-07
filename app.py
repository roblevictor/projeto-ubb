
from socket import timeout
from sys import flags
from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import request
from flask import make_response

app = Flask(__name__)
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/sobre/perfil")
def perfil():
    return "<h5>meu perfil</h5>"


@app.route("/cad/usuario")
def usuario():
    return render_template('usuario.html', titulo="Cadastro de usuario")

def caduser():
    return request.form


@app.route("/cad/anuncio")
def anuncio():
    return render_template('anuncio.html')

@app.route("/anuncio/pergunta")
def pergunta():
    return render_template('pergunta.html')

@app.route("/anuncio/compra")
def compra():
    print('anuncio comprado')
    return ""

@app.route("/anuncio/favoritos")
def favoritos():
    print('favorito inserido')
    return f"<h4>comprado</h4>"

@app.route("/config/categoria")
def categoria():
    return render_template('categoria.html')

@app.route("/relatorio/vendas")
def relVendas():
    return render_template('relVendas.html')

@app.route("/relatorios/compras")
def relCompras():
    return render_template('relCompras.html')

@app.route("/cad/login")
def login():
    return render_template('login.html')
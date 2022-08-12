
from socket import timeout
from sys import flags
from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import request
from flask import make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1361002Hugo@localhost:3306/minhacon'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column('usu_id', db.Integer, primary_key=True)
    nome = db.Column('usu_nome', db.String(256))
    email = db.Column('usu_email', db.String(256))
    senha = db.Column('usu_senha', db.String(256))
    end = db.Column('usu_end', db.String(256))

def __init__(self, nome, email, senha, end):
    self.nome = nome
    self.email = email
    self.senha = senha
    self.end = end
    
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


if __name__=='__main__':
    db.create_all()
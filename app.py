
from socket import timeout
from sys import flags
from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import request
from flask import make_response
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask import redirect
from flask_login import (current_user, LoginManager, login_user, logout_user, login_required)
import hashlib

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:136102Hugo@localhost:3306/meubanco'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://victorroble:136102Hugo@victorroble.mysql.pythonanywhere-services.com:3306/victorroble$meubanco'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db = SQLAlchemy(app)

app.secret_key = 'bolo de pote e muito bom'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Usuario(db.Model):
    __tablename__ = "usuario"
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

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column('cat_id', db.Integer, primary_key=True)
    nome = db.Column('cat_nome', db.String(256))
    desc = db.Column('cat_desc', db.String(256))

    def __init__ (self, nome, desc):
        self.nome = nome
        self.desc = desc

class Compra(db.Model):
    __tablename__ = "compra"
    id = db.Column('id_compra', db.Integer, primary_key=True)
    preco = db.Column("compra_preco", db.Float)
    qtd = db.Column("compra_qtd", db.Integer)
    total = db.Column("compra_total", db.Float)
    anuncio_id = db.Column("anunc_idanuncio", db.Integer, db.ForeignKey("anuncio.anu_id"))
    usu_id = db.Column("user_idusuario", db.Integer, db.ForeignKey("usuario.usu_id"))
    
    def __init__(self, preco, qtd, total, anu_id, usu_id):
        self.preco = preco
        self.qtd = qtd
        self.total = total
        self.anu_id = anu_id
        self.usu_id = usu_id

class Pergunta(db.Model):
    __tablename__ = "pergunta"
    id = db.Column("idPergunta", db.Integer, primary_key=True)
    pergunta = db.Column("per_pergunta", db.String(256))
    resposta = db.Column("per_resposta", db.String(256))
    usu_id = db.Column("usu_id", db.Integer, db.ForeignKey("usuario.usu_id"))
    anu_id = db.Column("anuncio_id", db.Integer, db.ForeignKey("anuncio.anu_id"))
    
    def __init__(self, pergunta, resposta, usu_id, anu_id):
        self.pergunta = pergunta
        self.resposta = resposta
        self.usu_id = usu_id
        self.anu_id = anu_id
    

class Anuncio(db.Model):
    __tablename__ = "anuncio"
    id = db.Column('anu_id', db.Integer, primary_key=True)
    nome = db.Column('anu_nome', db.String(256))
    desc = db.Column('anu_desc', db.String(256))
    qtd = db.Column('anu_qtd', db.Integer)
    preco = db.Column('anu_preco', db.Float)
    cat_id = db.Column('cat_id',db.Integer, db.ForeignKey("categoria.cat_id"))
    usu_id = db.Column('usu_id',db.Integer, db.ForeignKey("usuario.usu_id"))

    def __init__(self, nome, desc, qtd, preco, cat_id, usu_id):
        self.nome = nome
        self.desc = desc
        self.qtd = qtd
        self.preco = preco
        self.cat_id = cat_id
        self.usu_id = usu_id

@app.errorhandler(404)
def paginanotfound(error):
    return render_template("paginanotfound.html")

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(id)

@app.route("/")
def index():
    db.create_all()
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = hashlib.sha512(str(request.form.get('password')).encode("utf-8")).hexdigest()

        user = Usuario.query.filter_by(email=email, senha=password).first()
        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/sobre/perfil")
#@login_required
def perfil():
    return "<h5>meu perfil</h5>"

@app.route("/cad/usuario")
#@login_required
def cadusuario():
  return render_template('usuario.html',usuarios = Usuario.query.all(), titulo="Usuario")

@app.route("/usuario/criar", methods=['POST'])
def criarusuario():
    hash = hashlib.sha512(str(request.form.get('password')).encode("utf-8")).hexdigest()
    usuario = Usuario(request.form.get('user'), request.form.get('email'),hash,request.form.get('end'))
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('cadusuario'))

@app.route("/usuario/detalhes/<int:id>")
def buscarusuario(id):
    usuario = Usuario.query.get(id)
    return usuario.nome

@app.route("/usuario/editar/<int:id>", methods=['GET', 'POST'])
def editarusuario(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome = request.form.get('user')
        usuario.email = request.form.get('email')
        usuario.senha = hashlib.sha512(str(request.form.get('password')).encode("utf-8")).hexdigest()
        usuario.end = request.form.get('end')
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('cadusuario'))
    return render_template('editar.html', usuario = usuario, titulo="Usuario")
    

@app.route("/usuario/deletar/<int:id>")
def deletarusuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('cadusuario'))

@app.route("/cad/anuncio")
#@login_required
def anuncio():
    return render_template('anuncio.html', anuncios = Anuncio.query.all(), categorias = Categoria.query.all(), titulo="Anuncio")

@app.route("/anuncio/criar", methods=["POST"])
def criaranuncio():
    anuncio = Anuncio(request.form.get('nome'), request.form.get("desc"), request.form.get("qtd"), request.form.get("preco"), request.form.get("cat"), request.form.get("usu"))
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for('anuncio'))


@app.route("/anuncio/editar/<int:id>", methods=['GET','POST'])
def editaranuncio(id):
    anuncio = Anuncio.query.get(id)
    if request.method == 'POST':
        anuncio.nome = request.form.get('nome')
        anuncio.desc = request.form.get('desc')
        anuncio.qtd = request.form.get('qtd')
        anuncio.preco = request.form.get('preco')
        anuncio.cat_id = request.form.get('cat_id')
        anuncio.usu_id = request.form.get('usu_id')
        db.session.add(anuncio)
        db.session.commit()
        return redirect(url_for('anuncio'))
    return render_template('editanuncio.html', anuncio = anuncio, titulo="Anuncio")

@app.route("/anuncio/deletar/<int:id>")
def deletaranuncio(id):
    anuncio = Anuncio.query.get(id)
    db.session.delete(anuncio)
    db.session.commit()
    return redirect(url_for('anuncio'))    

@app.route("/anuncios/pergunta")
def pergunta():
    return render_template('anuncioPergunta.html', perguntas = Pergunta.query.all())

@app.route("/anunc/fazerpergunta/<int:id>")
def fazerpergunta(id):
    anuncio = Anuncio.query.get(id)
    return render_template("fazerpergunta.html", anuncio = anuncio, perguntas = Pergunta.query.filter_by(anuncio_id = anuncio.id))

@app.route("/anunc/fazerpergunta/<int:anuncio>/<int:id>", methods=['POST'])
def fazerresposta(anuncio, id):
    pergunta = Pergunta.query.get(id)
    pergunta.resposta = request.form.get("resposta")
    db.session.add(pergunta)
    db.session.commit()
    return redirect(url_for("fazerpergunta", id = anuncio))

@app.route("/anunc/pergunta/criar/<int:id>", methods=['POST'])
def criarpergunta(id):
    anuncio = Anuncio.query.get(id)
    pergunta = Pergunta(request.form.get("pergunta"),
    None, 
    current_user.id,
    anuncio.id)
    db.session.add(pergunta)
    db.session.commit()
    return redirect(url_for("fazerpergunta", id = id))

@app.route("/anunc/pergunta/resposta/<int:id>", methods=['GET','POST'])
def editarperguntar(id):
    pergunta = Pergunta.query.get(id) 
    if request.method == "POST":
        pergunta.pergunta = pergunta.pergunta
        pergunta.resposta = request.form.get("resposta")
        pergunta.usu_id = pergunta.usu_id
        pergunta.anuncio_id = pergunta.anuncio_id
        db.session.add(pergunta)
        db.session.commit()
        return redirect(url_for("pergunta"))
    return render_template("responderpergunta.html", pergunta = pergunta)

@app.route("/config/categoria")
#@login_required
def categoria():
    return render_template('categoria.html', categorias = Categoria.query.all(), titulo='Categoria')

@app.route("/categoria/criar", methods=['POST'])
def criarcategoria():
    categoria = Categoria(request.form.get('nome'), request.form.get('desc'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))

@app.route("/categoria/editar/<int:id>", methods=['GET','POST'])
def editarcategoria(id):
    categoria = Categoria.query.get(id)
    if request.method == 'POST':
        categoria.nome = request.form.get('nome')
        categoria.descricao = request.form.get('desc')
        db.session.add(categoria)
        db.session.commit()
        return redirect(url_for('categoria'))
    return render_template('editcategoria.html', categoria = categoria, titulo="Categoria")

@app.route("/categoria/deletar/<int:id>")
def deletarcategoria(id):
    categoria = Categoria.query.get(id)
    db.session.delete(categoria)
    db.session.commit()
    return redirect(url_for('categoria')) 

@app.route("/anuncio/compra/")
def compra():
    return redirect(url_for('index'))

@app.route("/anuncio/compra/<int:id>")
@login_required
def comprar(id):
    anuncio = Anuncio.query.get(id)
    aux = anuncio.qtd
    return render_template("comprar.html", aux = aux, anuncio = anuncio, usuarios = Usuario.query.all())

@app.route("/anuncio/compra/confirmarcompra/<int:id>", methods=['GET','POST'])
def confirmarcompra(id):
    anuncio = Anuncio.query.get(id)
    if int(request.form.get("qtd")) > anuncio.qtd:
        return render_template("errocompra.html")
    else:
        compra = Compra(anuncio.preco, request.form.get("qtd"), anuncio.preco * float(request.form.get("qtd")), anuncio.id, request.form.get("user"))
        anuncio.nome = anuncio.nome
        anuncio.desc = anuncio.desc
        anuncio.qtd = anuncio.qtd - int(request.form.get("qtd"))
        anuncio.preco = anuncio.preco
        anuncio.usu_id = anuncio.usu_id
        anuncio.cat_id = anuncio.cat_id
        db.session.add(compra)
        db.session.commit()
        db.session.add(anuncio)
        db.session.commit()
        return redirect(url_for("relCompras"))  


@app.route("/relatorio/vendas")
#@login_required
def relVendas():
    return render_template('relVendas.html')

@app.route("/relatorios/compras")
#@login_required
def relCompras():
    return render_template('relCompras.html')

if __name__=='buf':
    print('app')
    db.create_all()
    
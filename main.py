from flask_openapi3 import OpenAPI, Info, Tag
from flask import render_template, redirect, request, url_for
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
import hashlib

from models import Usuario
from model import Processo, Session  
from db import db
from schemas import *
from schemas.processo import Apresenta_Processo_Lista, ProcessoViewSchema, apresenta_processo
from logger import logger

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)

app.secret_key = 'brenorial'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database/database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app, origins="*")

with app.app_context():
    db.create_all()

def hash(txt):
    return hashlib.sha256(txt.encode('utf-8')).hexdigest()

@login_manager.user_loader
def user_loader(id):
    return db.session.query(Usuario).filter_by(id=id).first()

home_tag = Tag(name="Documentação", description="Seleção de documentação")
processo_tag = Tag(name="Processo", description="Cadastro de processo")

@app.route('/')
@login_required
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        nome = request.form['nomeForm']
        senha = request.form['senhaForm']
        user = db.session.query(Usuario).filter_by(nome=nome, senha=hash(senha)).first()
        if not user:
            return 'Nome ou senha incorretos'
        login_user(user)
        return redirect(url_for('inserir_processo'))

@app.route('/inserir_processo')
@login_required
def inserir_processo():
    return render_template('inserir_processo.html')


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'GET':
        return render_template('registrar.html')
    else:
        nome = request.form['nomeForm']
        senha = request.form['senhaForm']
        novo_usuario = Usuario(nome=nome, senha=hash(senha))
        db.session.add(novo_usuario)
        db.session.commit()
        login_user(novo_usuario)
        return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.get('/docs', tags=[home_tag])
def docs():
    return redirect('/openapi')

@app.post('/processo', tags=[processo_tag],
          responses={"200": ProcessoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
@login_required
def add_processo(form: ProcessoSchema):
    processo = Processo(
        numero=form.numero,
        descricao=form.descricao,
        data_inicio=form.data_inicio,
        data_fim=form.data_fim,
        usuario_id=current_user.id
    )
    logger.debug(f"Usuário {current_user.nome} inserindo processo '{processo.numero}'")

    try:
        session = Session()
        session.add(processo)
        session.commit()
        return Apresenta_Processo_Lista([processo]), 200
    except IntegrityError:
        return {"message": "Número de processo já cadastrado"}, 409
    except Exception as e:
        return {"message": f"Erro ao salvar: {str(e)}"}, 400

@app.get('/processos', tags=[processo_tag], responses={"200": ListagemDeProcessosSchema})
def get_processos():
    session = Session()
    processos = session.query(Processo).all()
    return Apresenta_Processo_Lista(processos), 200

@app.get('/busca_processo', tags=[processo_tag], responses={"200": ProcessoViewSchema, "404": ErrorSchema})
def get_processo(query: ProcessoBuscaSchema):
    session = Session()
    processo = session.query(Processo).filter(Processo.numero == query.numero).first()
    if not processo:
        return {"message": "Processo não encontrado"}, 404
    return apresenta_processo(processo), 200

@app.delete('/del_processo', tags=[processo_tag], responses={"200": ProcessoDelSchema, "404": ErrorSchema})
def del_processo(query: ProcessoBuscaSchema):
    session = Session()
    count = session.query(Processo).filter(Processo.numero == query.numero).delete()
    session.commit()
    if count:
        return {"message": "Processo removido", "numero": query.numero}, 200
    return {"message": "Processo não encontrado"}, 404

@app.put('/processo/atualizar', tags=[processo_tag], responses={"200": ProcessoViewSchema, "404": ErrorSchema})
def update_processo(form: ProcessoSchema):
    session = Session()
    processo = session.query(Processo).filter(Processo.numero == form.numero).first()
    if not processo:
        return {"message": "Processo não encontrado"}, 404

    processo.descricao = form.descricao
    processo.data_inicio = form.data_inicio
    processo.data_fim = form.data_fim
    session.commit()
    return apresenta_processo(processo), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

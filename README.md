# Projeto Flask com SQLAlchemy e Flask-SQLAlchemy

Este projeto é uma API REST para cadastro e gerenciamento de processos, usando Flask, Flask-Login, Flask-OpenAPI3 e banco de dados SQLite.

---

## Estrutura do Projeto

- `app.py`: arquivo principal da aplicação Flask.
- `db.py`: configuração do banco de dados e instância do Flask-SQLAlchemy.
- `model/`: modelos SQLAlchemy para o banco de dados.
- `schemas/`: schemas para validação e apresentação.
- `templates/`: arquivos HTML para as páginas.
- `logger.py`: configuração de logging.

---

## Configuração do Banco de Dados

Usamos **Flask-SQLAlchemy** para integração do SQLAlchemy com Flask, garantindo o uso de uma única sessão (`db.session`) em toda a aplicação.

### db.py

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

### Modelo Processo (em `model/processo.py`)

```python
from datetime import datetime
from db import db

class Processo(db.Model):
    __tablename__ = 'processo'

    id = db.Column("pk_processo", db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario = db.relationship("Usuario")

    numero = db.Column(db.String(50), unique=True, nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    data_insercao = db.Column(db.DateTime, default=datetime.now)
```

### Configuração do app Flask (exemplo simplificado)

```python
from flask import Flask
from db import db
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database/database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'sua_chave_secreta'

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

with app.app_context():
    db.create_all()
```

---

## Boas Práticas

- Use **apenas `db.session`** do Flask-SQLAlchemy para todas as operações no banco de dados para evitar conflitos.
- Não misture sessões manuais do SQLAlchemy (`sessionmaker()`) com `db.session`.
- Se precisar de múltiplos bancos, configure `SQLALCHEMY_BINDS` no Flask e use o atributo `__bind_key__` nos modelos.
- Sempre execute `db.create_all()` dentro do contexto do app (`with app.app_context()`).

---

## Exemplo de uso do banco na rota

```python
@app.route('/processo', methods=['POST'])
@login_required
def add_processo():
    form = request.form
    processo = Processo(
        numero=form['numero'],
        descricao=form['descricao'],
        data_inicio=form['data_inicio'],
        data_fim=form['data_fim'],
        usuario_id=current_user.id
    )
    try:
        db.session.add(processo)
        db.session.commit()
        return {"message": "Processo inserido com sucesso"}, 200
    except Exception as e:
        db.session.rollback()
        return {"message": f"Erro: {str(e)}"}, 400
```

---

## Solução de problemas comuns

- **Dados não sendo salvos:** verifique se está usando `db.session.commit()` e se está usando o `db.session` correto.
- **Erro ao criar tabela:** execute `db.create_all()` no contexto do app e garanta que o modelo está registrado no `db`.
- **Conflito entre sessões:** evite criar sessões SQLAlchemy manualmente (`Session()`) se usar Flask-SQLAlchemy.

---

## Dependências

- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-OpenAPI3
- SQLAlchemy
- Flask-CORS

Instale com:

```bash
pip install flask flask-sqlalchemy flask-login flask-openapi3 sqlalchemy flask-cors
```

---

## Execução

```bash
export FLASK_APP=app.py
flask run
```

Ou

```bash
python app.py
```

---

Se precisar de ajuda para ajustar o código para usar Flask-SQLAlchemy exclusivamente ou para configurar múltiplos bancos, posso ajudar!

---

# FIM

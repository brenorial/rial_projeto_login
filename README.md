# 🛡️ Rial Login

Este é um projeto simples de **sistema de login com Flask**, desenvolvido em Python. Ele utiliza hash (SHA-256) para armazenar as senhas com segurança e gerenciar sessões de login de usuários.

---

## 🔧 Tecnologias utilizadas

- [Flask](https://flask.palletsprojects.com/) – framework web leve e rápido
- [Flask-Login](https://flask-login.readthedocs.io/) – gerenciamento de login e sessão
- [SQLAlchemy](https://www.sqlalchemy.org/) – ORM para banco de dados
- SQLite – banco de dados leve, usado localmente
- hashlib – biblioteca padrão do Python para gerar hashes

---

## ✅ Funcionalidades

- **Registro de usuários** com nome e senha (criptografada com SHA-256)
- **Login seguro** com validação de senha via hash
- **Gerenciamento de sessão** com Flask-Login
- **Proteção de rotas** com `@login_required`
- **Logout** que encerra a sessão atual

---

## 📂 Estrutura do projeto

```bash
rial_login/
│
├── app.py               # Arquivo principal com as rotas e lógica
├── db.py                # Inicialização do banco de dados
├── models.py            # Definição do modelo de usuário
├── templates/           # Páginas HTML (login, registrar, home)
│   ├── login.html
│   ├── registrar.html
│   └── home.html
└── database.db          # Banco de dados SQLite (gerado automaticamente)
```

---

## ▶️ Como rodar o projeto

1. Clone o repositório:

```bash
git clone https://github.com/brenorial/rial_login.git
cd rial_login
```

2. (Opcional) Crie um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Instale as dependências:

```bash
pip install flask flask-login flask_sqlalchemy
```

4. Execute o projeto:

```bash
python app.py
```

5. Acesse o navegador em:
   `http://localhost:5000`

---

## 🔒 Segurança

As senhas dos usuários são protegidas com `hashlib.sha256` antes de serem armazenadas no banco de dados. Isso significa que mesmo que alguém tenha acesso ao banco, não verá as senhas reais.

---

## 📌 Observações

- Este projeto é uma base simples para estudo ou prototipagem.
- Para produção, recomenda-se adicionar validações, mensagens amigáveis, melhorias no design e usar hashing com **salt** (ex: `bcrypt`) para mais segurança.

---

## ✍️ Autor

Feito por [@brenorial](https://github.com/brenorial)

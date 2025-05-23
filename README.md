# 🌱 GreenLink Marketplace — Backend

Este repositório contém o backend da plataforma **GreenLink Marketplace**, desenvolvido em **Django**. O backend é responsável pela gestão de usuários, anúncios de materiais reutilizáveis, transações sustentáveis, sistema de recompensas e integração com o frontend web e mobile.

---

## 🚀 Tecnologias Utilizadas

- [Python 3.10+](https://www.python.org/)
- [Django 4.x](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker (opcional)](https://www.docker.com/)
- [Gunicorn + Nginx (para deploy)](https://gunicorn.org/)
- [python-decouple](https://github.com/henriquebastos/python-decouple)

---

## ⚙️ Como rodar o projeto localmente

### 1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/greenlink-marketplace-backend.git
cd greenlink-marketplace-backend
```

### 2. Crie e ative o ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
```

### 3. Instale as dependências:

```bash
pip install -r requirements.txt
```

<<<<<<< HEAD
### 4. Configure as variáveis de ambiente com um arquivo `.env`:

Crie um arquivo chamado `.env` na raiz do projeto com o seguinte conteúdo:

```ini
DEBUG=True
SECRET_KEY=sua_chave_secreta
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=nome_do_seu_bd
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=host_do_seu_bd
DB_PORT=posta_do_seu_bd
```

⚠️ **Importante:** nunca comite o arquivo `.env` no repositório. Certifique-se de que ele está listado no `.gitignore`.
=======
### 4. Configure variáveis de ambiente:

```bash
DEBUG=True
SECRET_KEY=sua_chave_secreta
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://usuario:senha@localhost:5432/greenlink
```

Dica: você pode usar o pacote python-decouple ou django-environ para carregar variáveis do .env.

### 4. Configure variáveis de ambiente:

```bash
DEBUG=True
SECRET_KEY=sua_chave_secreta
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://usuario:senha@localhost:5432/greenlink
```

Dica: você pode usar o pacote python-decouple ou django-environ para carregar variáveis do .env.
>>>>>>> 6d72243bf80770720653559233c0235be9e66be3

### 5. Execute as migrações:

```bash
python manage.py migrate
```

### 6. Crie um superusuário (opcional):

```bash
python manage.py createsuperuser
```

### 7. Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

<<<<<<< HEAD
---

=======
>>>>>>> 6d72243bf80770720653559233c0235be9e66be3
## 📡 Endpoints da API

Após subir o servidor, os endpoints estarão disponíveis em:

```bash
http://127.0.0.1:8000/api/
```

Endpoints principais:

<<<<<<< HEAD
- `/api/users/` – Gerenciamento de usuários
- `/api/materials/` – Anúncios e materiais recicláveis
- `/api/transactions/` – Transações e trocas
- `/api/rewards/` – Sistema de pontos e recompensas

> A documentação interativa da API está disponível via Django REST Framework Browsable API (ou Swagger, se configurado).

---
=======
/api/users/ – Gerenciamento de usuários

/api/materials/ – Anúncios e materiais recicláveis

/api/transactions/ – Transações e trocas

/api/rewards/ – Sistema de pontos e recompensas

Nota: documentação interativa da API disponível via DRF Browsable API ou Swagger se configurado.
>>>>>>> 6d72243bf80770720653559233c0235be9e66be3

## 🧪 Testes

Para rodar os testes automatizados:

```bash
python manage.py test
```

<<<<<<< HEAD
---

=======
>>>>>>> 6d72243bf80770720653559233c0235be9e66be3
## 📦 Deploy (em construção)

Planejamos utilizar:

<<<<<<< HEAD
- Docker
- PostgreSQL
- Gunicorn + Nginx
- Railway / Render / VPS próprio

Guia de deploy em breve.

---

## 👥 Contribuidores

Rodrigo Cruz ([@rodrig-crzz](https://github.com/rodrig-crzz)) — Desenvolvedor principal

---

Vamos construir um futuro mais sustentável juntos! 🌱
=======
Docker

PostgreSQL

Gunicorn + Nginx

Railway / Render / VPS próprio

Guia de deploy em breve.

## 👥 Contribuidores

Rodrigo Cruz (@rodrig-crzz) — Desenvolvedor principal
>>>>>>> 6d72243bf80770720653559233c0235be9e66be3

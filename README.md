# 🌱 GreenLink Marketplace — Backend

Este repositório contém o backend da plataforma **GreenLink Marketplace**, desenvolvido em **Django**. O backend é responsável pela gestão de usuários, anúncios de materiais reutilizáveis, transações sustentáveis, sistema de recompensas e integração com o frontend web e mobile.

---

## 🚀 Tecnologias Utilizadas

- [Python 3.10+](https://www.python.org/)
- [Django 4.x](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Gunicorn + Nginx (para deploy)](https://gunicorn.org/)
- [python-decouple](https://github.com/henriquebastos/python-decouple)
- [djangorestframework-simplejwt](https://github.com/jazzband/djangorestframework-simplejwt)

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

### 4. Configure as variáveis de ambiente com um arquivo `.env`:

Crie um arquivo chamado `.env` na raiz do projeto com o seguinte conteúdo:

```ini
DB_NAME=nome_do_seu_bd
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=host_do_seu_bd
DB_PORT=posta_do_seu_bd
```

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

## 📡 Endpoints da API

Após subir o servidor, os endpoints estarão disponíveis em:

```bash
http://127.0.0.1:8000/api/
```

Endpoints principais:

- `/api/accounts/` – Gerenciamento de usuários: Inclui endpoints para autenticação, cadastro, perfil, permissões e gerenciamento de credenciais.
- `/api/marketplace/` – Gerenciamento do marketplace: Engloba o cadastro, busca e visualização de produtos, além da interação entre consumidores e empresas.
- `/api/recycling/` – Gerenciamento de processos de reciclagem: Controle de operações de coleta, resíduos, recicladoras, e pontos de coleta.
- `/api/core/` – Gerenciamento de configurações e administração: Inclui funcionalidades centrais do sistema, configurações administrativas, dados de contato/bancários e comprovantes.

## 🧪 Testes

Para rodar os testes automatizados:

```bash
python manage.py test
```

## 📦 Deploy (em construção)

Planejamos utilizar:

- Gunicorn + Nginx

Guia de deploy em breve.

---

## 👥 Contribuidores

Rodrigo Cruz ([@rodrig-crzz](https://github.com/rodrig-crzz)) — Desenvolvedor principal

---

Vamos construir um futuro mais sustentável juntos! 🌱

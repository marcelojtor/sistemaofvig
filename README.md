# 📊 Sistema de Controle de Presença de Colaboradores

Sistema web completo para gestão de presença de colaboradores em eventos e contratos, desenvolvido com Flask, SQLite e interface moderna em dark mode.

---

## 🚀 Funcionalidades

### 🔐 Autenticação
- Login com controle de sessão
- Perfis de acesso:
  - Diretor (acesso total)
  - Supervisor (acesso limitado)
  - Desenvolvedor (acesso total)

---

### 📁 Gestão por Evento/Contrato
- Seleção de evento ou contrato
- Dados vinculados ao evento ativo
- Controle via sessão

---

### 👥 Cadastro de Colaboradores
- Cadastro completo com:
  - Nome
  - CPF
  - CN
  - Sexo
  - Profissão
  - Valor de pagamento
  - Pix
  - Banco
- Vinculação automática ao evento

---

### 📅 Controle de Presença (Dinâmico)
- Adição de múltiplas datas
- Botão "Adicionar dia"
- Armazenamento em tabela relacional

---

### 📋 Listagem e Exclusão
- Visualização de todos colaboradores do evento
- Exclusão com confirmação
- Restrição para perfil Supervisor

---

### 📊 Dashboard / Relatórios
- Total de colaboradores
- Soma de pagamentos
- Listagem de presenças
- Botão de impressão

---

## 🧱 Tecnologias Utilizadas

- Python (Flask)
- SQLite
- SQLAlchemy
- Flask-Login
- HTML + CSS + JavaScript
- Bootstrap 5
- Gunicorn

---

## 📁 Estrutura do Projeto

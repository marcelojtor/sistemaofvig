from flask import render_template, request, redirect, url_for, session, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, Usuario, Evento, Colaborador, Presenca
from werkzeug.security import check_password_hash
from datetime import datetime

def init_routes(app):

    # ==============================
    # LOGIN
    # ==============================
    @app.route('/', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user = Usuario.query.filter_by(username=username).first()

            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('selecionar_evento'))
            else:
                flash('Usuário ou senha inválidos')

        return render_template('login.html')


    # ==============================
    # LOGOUT
    # ==============================
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        session.clear()
        return redirect(url_for('login'))


    # ==============================
    # SELEÇÃO DE EVENTO
    # ==============================
    @app.route('/selecionar_evento', methods=['GET', 'POST'])
    @login_required
    def selecionar_evento():
        eventos = Evento.query.all()

        if request.method == 'POST':
            evento_id = request.form.get('evento')
            session['evento_id'] = evento_id
            return redirect(url_for('menu'))

        return render_template('selecionar_evento.html', eventos=eventos)


    # ==============================
    # MENU PRINCIPAL
    # ==============================
    @app.route('/menu')
    @login_required
    def menu():
        if 'evento_id' not in session:
            return redirect(url_for('selecionar_evento'))

        evento = Evento.query.get(session['evento_id'])
        return render_template('menu.html', evento=evento, user=current_user)


    # ==============================
    # CADASTRAR COLABORADOR
    # ==============================
    @app.route('/cadastrar', methods=['GET', 'POST'])
    @login_required
    def cadastrar():

        if 'evento_id' not in session:
            return redirect(url_for('selecionar_evento'))

        if request.method == 'POST':
            nome = request.form['nome']
            cpf = request.form['cpf']
            cn = request.form['cn']
            sexo = request.form['sexo']
            valor = request.form['valor']
            pix = request.form['pix']
            banco = request.form['banco']
            profissao = request.form['profissao']

            colaborador = Colaborador(
                nome=nome,
                cpf=cpf,
                cn=cn,
                sexo=sexo,
                valor_pagamento=float(valor),
                pix=pix,
                banco=banco,
                profissao=profissao,
                evento_id=session['evento_id']
            )

            db.session.add(colaborador)
            db.session.commit()

            # ==============================
            # PRESENÇAS DINÂMICAS
            # ==============================
            datas = request.form.getlist('datas[]')

            for data in datas:
                if data:
                    presenca = Presenca(
                        colaborador_id=colaborador.id,
                        data_presenca=datetime.strptime(data, '%Y-%m-%d')
                    )
                    db.session.add(presenca)

            db.session.commit()

            flash('Colaborador cadastrado com sucesso!')
            return redirect(url_for('menu'))

        return render_template('cadastro.html')


    # ==============================
    # LISTAR TODOS
    # ==============================
    @app.route('/colaboradores')
    @login_required
    def listar_colaboradores():
        if 'evento_id' not in session:
            return redirect(url_for('selecionar_evento'))

        colaboradores = Colaborador.query.filter_by(
            evento_id=session['evento_id']
        ).all()

        return render_template('listar.html', colaboradores=colaboradores)


    # ==============================
    # EXCLUIR (BLOQUEIO PARA SUPERVISOR)
    # ==============================
    @app.route('/excluir/<int:id>')
    @login_required
    def excluir(id):
        if current_user.role == 'supervisor':
            flash('Acesso negado!')
            return redirect(url_for('menu'))

        colaborador = Colaborador.query.get_or_404(id)
        db.session.delete(colaborador)
        db.session.commit()

        flash('Colaborador excluído!')
        return redirect(url_for('listar_colaboradores'))


    # ==============================
    # RELATÓRIOS / DASHBOARD
    # ==============================
    @app.route('/relatorios')
    @login_required
    def relatorios():
        if 'evento_id' not in session:
            return redirect(url_for('selecionar_evento'))

        evento = Evento.query.get(session['evento_id'])

        colaboradores = Colaborador.query.filter_by(
            evento_id=session['evento_id']
        ).all()

        total_colaboradores = len(colaboradores)
        total_pagamentos = sum(c.valor_pagamento for c in colaboradores)

        presencas = Presenca.query.join(Colaborador).filter(
            Colaborador.evento_id == session['evento_id']
        ).all()

        return render_template(
            'relatorios.html',
            evento=evento,
            total_colaboradores=total_colaboradores,
            total_pagamentos=total_pagamentos,
            presencas=presencas
        )

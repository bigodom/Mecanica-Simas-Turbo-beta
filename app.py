from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///manutencao.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)

@app.before_first_request
def create_tables():
    db.drop_all()
    db.create_all()


class Manutencao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    placa = db.Column(db.String(7), nullable=False)
    data = db.Column(db.String(10), nullable=False)
    dataS = db.Column(db.String(10), nullable=True)
    tipo = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    observacoes = db.Column(db.Text, nullable=False)


    def __repr__(self):
        return '<Manutencao %r>' % self.id


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        placa = request.form['placa']
        data = request.form['data']
        tipo = request.form['tipo']
        valor = request.form['valor']
        observacoes = request.form['observacoes']

        manutencao = Manutencao(nome=nome, placa=placa, data=data, tipo=tipo, valor=valor, observacoes=observacoes)

        try:
            db.session.add(manutencao)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'Erro ao adicionar manutenção'

    else:
        manutencoes = Manutencao.query.order_by(Manutencao.data).all()
        return render_template('index.html', manutencoes=manutencoes)


@app.route('/delete/<int:id>')
def delete(id):
    manutencao = Manutencao.query.get_or_404(id)

    try:
        db.session.delete(manutencao)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'Erro ao deletar manutenção'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    manutencao = Manutencao.query.get_or_404(id)

    if request.method == 'POST':
        manutencao.nome = request.form['nome']
        manutencao.placa = request.form['placa']
        manutencao.data = request.form['data']
        manutencao.tipo = request.form['tipo']
        manutencao.valor = request.form['valor']
        manutencao.observacoes = request.form['observacoes']

        try:
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'Erro ao atualizar manutenção'

    else:
        return render_template('update.html', manutencao=manutencao)


@app.route('/clear')
def clear():
    try:
        Manutencao.query.delete()
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'Erro ao limpar manutenções'

@app.route('/cadastrar')


@app.route('/concluidos')
def concluidos():
    if request.method == 'POST':
        nome = request.form['nome']
        placa = request.form['placa']
        data = request.form['data']
        dataS = request.form['dataS']
        tipo = request.form['tipo']
        valor = request.form['valor']
        observacoes = request.form['observacoes']

        manutencao = Manutencao(nome=nome, placa=placa, data=data, dataS=dataS, tipo=tipo, valor=valor, observacoes=observacoes)

        try:
            db.session.add(manutencao)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'Erro ao adicionar manutenção'

    else:
        manutencoes = Manutencao.query.order_by(Manutencao.data)
        return render_template('concluidos.html', manutencoes=manutencoes)

if __name__ == "__main__":
    app.run(debug=True)

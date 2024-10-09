from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///consultas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo para armazenar consultas
class Consulta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    data = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Consulta {self.nome} - {self.data}>'

# Cria o banco de dados e a tabela se não existirem
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/mensagem', methods=['POST'])
def mensagem():
    mensagem = request.form['mensagem']
    etapa = int(request.form['etapa'])

    # Respostas baseadas na etapa
    if etapa == 1:
        if mensagem == "1":
            return jsonify(resposta="Você escolheu marcar uma consulta. Por favor, escolha uma data.", proxima_etapa=2)
        elif mensagem == "2":
            return jsonify(resposta="Você escolheu acompanhar resultados. Por favor, digite seu ID de resultado:", proxima_etapa=3)
        elif mensagem == "3":
            return jsonify(resposta="Obrigado por usar o chatbot. Até logo!", proxima_etapa=5)
        else:
            return jsonify(resposta="Opção inválida. Por favor, escolha uma opção válida (1, 2 ou 3).", proxima_etapa=1)
    
    elif etapa == 2:  # Para marcar consulta
        return jsonify(resposta="Agora, por favor, digite seu nome completo:", proxima_etapa=3)

    elif etapa == 3:  # Solicitar CPF após o nome
        return jsonify(resposta="Agora, por favor, digite seu CPF:", proxima_etapa=4)

    elif etapa == 4:  # Armazenar consulta
        # Armazena as informações
        nomeCompleto = request.form['nomeCompleto']
        cpf = request.form['mensagem']  # CPF recebido do usuário
        dataConsulta = request.form['dataConsulta']  # Supondo que você tenha a data
        consulta = Consulta(nome=nomeCompleto, cpf=cpf, data=dataConsulta)
        db.session.add(consulta)
        db.session.commit()
        return jsonify(resposta="Consulta marcada com sucesso!", proxima_etapa=5)

    elif etapa == 5:  # Acompanhar resultados
        return jsonify(resposta="Por favor, digite seu ID de resultado:", proxima_etapa=6)

    elif etapa == 6:  # Aqui você pode adicionar a lógica para buscar resultados
        idResultado = mensagem  # ID recebido do usuário
        # Aqui você poderia buscar o resultado no banco de dados
        return jsonify(resposta=f"Você digitou o ID: {idResultado}. Que mais posso ajudar?", proxima_etapa=5)

    return jsonify(resposta="Algo deu errado. Tente novamente.", proxima_etapa=1)





@app.route('/consultas', methods=['GET'])
def ver_consultas():
    consultas = Consulta.query.all()
    return render_template('consultas.html', consultas=consultas)





if __name__ == "__main__":
    app.run(debug=True)




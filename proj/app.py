import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

#realiza a conexao com o db
def get_db():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1805",
            database="tarefas_db"
        )
        print("Banco conectado com sucesso")
        return db
    except mysql.connector.Error as e:
        print("Erro ao conectar:", e)
        return None
    

#criar usuario (POST)
@app.route('/users', methods=['POST'])
def add_user():
    nome = request.json.get('nome')
    senha = request.json.get('senha')

    if not nome or not senha:
        return jsonify({'error' : 'Os dados sao obrigatorios'}), 400
    
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO users (nome, senha) VALUES (%s, %s)', (nome, senha))
        db.commit()
        return jsonify({'message': 'dado gravado com sucesso'}), 201
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500    
    finally:
        db.close()

#consultar usuarios existentes (GET)
@app.route('/users', methods=['GET'])
def get_users():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users')
        #logica para consultar e transformar os dados // o cursor.description coleta os nomes das colunas
        columns = [col[0] for col in cursor.description]
        users = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return jsonify(users)
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500    
    finally:
        db.close()

#consultar usuario pelo id (GET)
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,)) #ao final tem que ter "," para reconhecer como tupla
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone() #ao invers de fetchall pois retornara so um dicionario
        if row:
            user = dict(zip(columns, row)) #vai transformar a linha em dicionario -> chave = nome da coluna || valor = dado.
            return jsonify(user)
        else: 
            return jsonify({'error': 'Dado nao encontrado'}), 404
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500    
    finally:
        db.close()

#consultar e retornar usauario por ID
@app.route('/login', methods=['POST'])
def login():
    nome = request.json.get('nome')
    senha = request.json.get('senha')
    print("Tentando login com:", nome, senha) # 👀 debug

    if not nome or not senha:
        return jsonify({'error': 'Nome e senha são obrigatórios'}), 400

    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE nome = %s AND senha = %s', (nome, senha))
        row = cursor.fetchone()
        print("Resultado:", row) # 👀 debug
        if row:
            # pega os nomes das colunas
            columns = [col[0] for col in cursor.description]
            user = dict(zip(columns, row))
            return jsonify({'message': 'Usuário encontrado', 'id': user['id'], 'nome': user['nome']}), 200
        else:
            return jsonify({'error': 'Usuário ou senha inválidos'}), 401
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


#atualizar usuario (PUT)
@app.route('/users/<int:user_id>', methods=['PUT'])
def put_user(user_id):

    nome = request.json.get('nome')
    senha = request.json.get('senha')

    if not nome or not senha:
        return jsonify({'error' : 'Os dados sao obrigatorios'}), 400
    
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('UPDATE users SET nome = %s, senha = %s WHERE id = %s', (nome, senha, user_id))
        db.commit()
        return jsonify({'message': 'Usuario atualizado com sucesso'}), 201
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500    
    finally:
        db.close()

#deletar usuario (DELETE)
@app.route('/users/<int:user_id>', methods=['DELETE'])
def del_user(user_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
        db.commit()
        return jsonify({'message' : 'Dado deletado com sucesso'}), 200
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500    
    finally:
        db.close()

##//--> area das tarefas

#criar tarefa (POST)
@app.route('/users/<int:user_id>/tarefas', methods=['POST'])
def add_tarefa(user_id):
    titulo = request.json.get('titulo')
    descricao = request.json.get('descricao')
    status = request.json.get('status', 'pendente') #caso o primeiro nao seja satisfeito substitui pela segunda opcao

    if not titulo:
        return jsonify({'error': 'Deve conter ao menos o titulo'})
        
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO tarefas (titulo, descricao, status, user_id) VALUES (%s, %s, %s, %s)', (titulo, descricao, status, user_id))
        db.commit()
        return jsonify({'message': 'tarefa registrada com sucesso'}), 201
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500    
    finally:
        db.close()

#consultar tarefas registradas (GET)
@app.route('/users/<int:user_id>/tarefas', methods=['GET'])
def get_tarefas(user_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM tarefas WHERE user_id = %s', (user_id,))
        #logica para consultar e transformar os dados // o cursor.description coleta os nomes das colunas
        columns = [col[0] for col in cursor.description]
        tarefas = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return jsonify(tarefas)
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500    
    finally:
        db.close()

#atualizar tarefa (PUT)
@app.route('/users/<int:user_id>/tarefas/<int:tarefa_id>', methods=['PUT'])
def put_tarefa(user_id, tarefa_id):
    titulo = request.json.get('titulo')
    descricao = request.json.get('descricao')
    status = request.json.get('status', 'pendente')

    if not titulo:
        return jsonify({'error': 'Deve conter ao menos o titulo'})
    
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('UPDATE tarefas SET titulo = %s, descricao = %s, status = %s WHERE user_id = %s AND id = %s', (titulo, descricao,status, user_id, tarefa_id))
        db.commit()
        return jsonify({'message': 'tarefa atualizada com sucesso'}), 201
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500    
    finally:
        db.close()

#deletar tarefa (DELETE)
@app.route('/users/<int:user_id>/tarefas/<int:tarefa_id>', methods=['DELETE'])
def delete_tarefa(user_id, tarefa_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM tarefas WHERE user_id = %s AND id = %s',(user_id, tarefa_id))
        db.commit()
        return jsonify({'message':'Tarefa deletada'})
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500    
    finally:
        db.close()

if __name__ == '__main__':
    get_db()
    app.run(debug=True)

import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db_name = os.getenv('POSTGRES_DB', 'postgresdb')
db_user = os.getenv('POSTGRES_USER', 'admin')
db_password = os.getenv('POSTGRES_PASSWORD', 'psltest')

db_uri = f'postgresql://{db_user}:{db_password}@localhost:5432/{db_name}'

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Task(db.Model):
    content = db.Column(db.String(200), primary_key=True)
    completed = db.Column(db.String(10))

@app.route('/get', methods=['GET'])
def get_all_tasks():
    tasks = Task.query.all()
    output = [{'content': task.content, 'completed': task.completed} for task in tasks]
    return jsonify({'tasks': output})

@app.route('/post', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(content=data['content'], completed=data['completed'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully'})

@app.route('/home/delete/<content>', methods=['DELETE'])
def delete_task(content):
    task = Task.query.get(content)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'})
    else:
        return jsonify({'message': 'Task not found'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

db_connect = create_engine('sqlite:///tasks.db')
app = Flask(__name__)
api = Api(app)


class Task(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from tasks")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

    def post(self):
        conn = db_connect.connect()
        task = request.json['task']
        done = request.json['done']

        conn.execute(
            "insert into tasks values(null, '{0}','{1}')".format(task, done))

        query = conn.execute('select * from tasks order by id desc limit 1')
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

    def put(self):
        conn = db_connect.connect()
        id = request.json['id']
        task = request.json['task']
        done = request.json['done']

        conn.execute("update tasks set task ='" + str(task) +
                     "', done ='" + str(done) + "'  where id =%d " % int(id))

        query = conn.execute("select * from tasks where id=%d " % int(id))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

class TaskById(Resource):
    def delete(self, id):
        conn = db_connect.connect()
        conn.execute("delete from tasks where id=%d " % int(id))
        return {"status": "success"}

    def get(self, id):
        conn = db_connect.connect()
        query = conn.execute("select * from tasks where id =%d " % int(id))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

api.add_resource(Task, '/api/tasks')
api.add_resource(TaskById, '/api/tasks/<id>')

if __name__ == '__main__':
    app.run()
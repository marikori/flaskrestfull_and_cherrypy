from app_api.task_api import TaskApi
from app_api.task_data import TaskData

from flask_restful import Resource, fields, marshal
from flask import request 

app_data = TaskData()


task_fields = {
    'title': fields.String,
    'description': fields.String,
    'done': fields.Boolean,
    'uri': fields.Url('task')
}

class TaskListRestApi(Resource):
    
    def __init__(self):
        self.task_api = TaskApi(app_data)
    
    def get(self):
        tasks = self.task_api.get_tasks()
        return {"tasks": marshal(tasks, task_fields)}
    
    def post(self):
        task = self.task_api.create_task(request.json)
        return {"task": marshal(task, task_fields)}, 201
    
    

class TaskRestApi(Resource):
    
    def __init__(self):
        self.task_api = TaskApi(app_data)
    
    def get(self, id):
        task = self.task_api.get_task(id)
        return {"task": marshal(task, task_fields)}
    
    def put(self, id):
        task = self.task_api.update_task(request.json, id)
        return {"task": marshal(task, task_fields)}
    
    def delete(self, id):
        ret_val = self.task_api.delete_task(id)
        return {"result": ret_val}

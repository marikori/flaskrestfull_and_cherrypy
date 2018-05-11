'''
@author: marikori
'''

from rest_api.common_rest_api import CommonRestApi

class TaskListRestApi(CommonRestApi):
    '''
    classdocs
    '''
    
    def get(self):
        return {"tasks": self.task_api.get_tasks()}
    
    

class TaskRestApi(CommonRestApi):
    '''
    classdocs
    '''
    
    def get(self, task_id):
        return {"task": self.task_api.get_tasks(task_id)}


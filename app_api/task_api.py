'''
@author: marikori
'''

from app_api.task_data import TaskData


class TaskError(Exception):
    
    def __init__(self, message, code):
        self._code = code
        self._message = message

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._message

    def __str__(self):
        return self.__class__.__name__ + ': ' + self.message



class TaskNotFound(TaskError):
    
    def __init__(self, task_id):
        super().__init__('Task ID {} not found.'.format(task_id), 404)



class BadRequest(TaskError):
    
    def __init__(self, message):
        super().__init__(message, 400)



class TaskApi(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.app_data = TaskData()
    
    
    
    def get_tasks(self, task_id = None):
        
        if task_id is None:
            return self.app_data.get_tasks()
        
        else:
            task = [task for task in self.app_data.get_tasks() if task["id"] == task_id]
            
            if len(task) == 0:
                raise TaskNotFound(task_id)
            
            return task[0]
    
    
    
    def create_task(self, request):
        
        if not request or not 'title' in request:
            raise BadRequest("Missing required key \'title\'")
        
        task = {
            'title': request['title'],
            'description': request.get('description', ""),
            'done': False
        }
        
        return self.app_data.append_task(task)
    
    
    
    def update_task(self, request, task_id):
        
        task = [task for task in self.app_data.get_tasks() if task['id'] == task_id]
        
        if len(task) == 0:
            raise TaskNotFound(task_id)
        
        if not request:
            raise BadRequest("No data provided")
        
        if 'title' in request and type(request['title']) != str:
            raise BadRequest("Title has to be string")
        
        if 'description' in request and type(request['description']) is not str:
            raise BadRequest("Description has to be string")
        
        if 'done' in request and type(request['done']) is not bool:
            raise BadRequest("Done has to be boolean")
        
        task[0]['title'] = request.get('title', task[0]['title'])
        task[0]['description'] = request.get('description', task[0]['description'])
        task[0]['done'] = request.get('done', task[0]['done'])
        
        return task[0]
    
    
    
    def delete_task(self, task_id):
        
        task = [task for task in self.app_data.get_tasks() if task['id'] == task_id]
        
        if len(task) == 0:
            raise TaskNotFound(task_id)
        
        return self.app_data.remove_task(task[0])


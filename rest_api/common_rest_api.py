'''
@author: marikori
'''

from flask_restful import Resource
from app_api.task_api import TaskApi


class CommonRestApi(Resource):
    '''
    classdocs
    '''
    
    
    def __init__(self):
        '''
        Constructor
        '''
        self.task_api = TaskApi()
        
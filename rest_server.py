#!/usr/bin/env python3

import argparse, sys
import cherrypy

import flask_restful
from flask import Flask

from rest_api.task_rest_api import TaskListRestApi, TaskRestApi
from rest_api.errs import errs



app = Flask(__name__)
api = flask_restful.Api(app, catch_all_404s = True, errors = errs)


def GetArgs():
    
    parser = argparse.ArgumentParser(description = "Start the server; select from options:", formatter_class = argparse.RawTextHelpFormatter)
    parser.add_argument('--use_FlaskDev', required = False, action = 'store_true', help = 'Flask dev server to be used for development (default = False).', default = False)
    parser.add_argument('--use_CherryPy', required = False, action = 'store_true', help = 'CherryPy stand alone server to be used in production (default = False).', default = False)
    
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        parser.print_usage()
    else:
        return args


def main():
    
    api.add_resource(TaskListRestApi, '/todo/api/v1.0/tasks', endpoint = 'tasks')
    api.add_resource(TaskRestApi, '/todo/api/v1.0/tasks/<int:id>', endpoint = 'task')
    
    args = GetArgs()
    
    if args is not None:
        
        if args.use_FlaskDev:
            app.run(debug = False)
        
        elif args.use_CherryPy:
            cherrypy.tree.graft(app.wsgi_app, '/')
            cherrypy.config.update({'server.socket_host': '0.0.0.0',
                                    'server.ssl_module':'builtin',
                                    'server.ssl_certificate':'cert/cert.pem',
                                    'server.ssl_private_key':'cert/privkey.pem',
                                    'engine.autoreload.on': False
                                    })
            
            cherrypy.engine.start()



if __name__ == '__main__':
    main()

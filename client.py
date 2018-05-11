#!/usr/bin/env python3
'''
@author: marikori
'''

import argparse, sys

from urllib.request import Request
from urllib.request import urlopen
import ssl, json, base64

ssl_context = ssl.create_default_context();
ssl_context.check_hostname=False
ssl_context.verify_mode=ssl.CERT_NONE



def GetArgs():
    
    parser = argparse.ArgumentParser(description = "Select from options:", formatter_class = argparse.RawTextHelpFormatter)
    parser.add_argument('--method', required = False, nargs = 1, metavar=('GET|POST|PUT|DELETE'), action = 'store', help = 'HTTP method to be used (default GET).')
    parser.add_argument('--url', required = True, nargs = 1, metavar=('URL'), action = 'store', help = 'URL to be used for the request - e.g. http://127.0.0.1:5000/todo/api/v1.0/tasks')
    parser.add_argument('--data', required = False, nargs = 1, metavar=('FILE'), action = 'store', help = 'File where data to be used in HTTP(S) body are stored.')
    
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        parser.print_usage()
    else:
        return args


def call(uri, data = None, headrs = None, method = "GET"):
    
    print("REQUEST")
    print(method + " " + uri)
    print("headrs " + str(headrs))
    print("data " + str(data))
    
    try:
        if headrs is not None:
            request = Request(uri, data, headers = headrs, method = method)
        
        else:
            request = Request(uri, data, method = method)
        
        resp = urlopen(request, context = ssl_context)
    
    except Exception as e:
        if hasattr(e, "read"):
            print("EXCEPTION")
            print("code " + str(e.code))
            print(e.read().decode('utf-8'))
        
        raise e
    
    resp_json = json.loads(resp.read().decode('utf-8'))
    
    print("RESPONSE")
    print(json.dumps(resp_json, indent=4, sort_keys=True))
    print()
    
    return resp_json



if __name__ == '__main__':
    
    args = GetArgs()
    
    if args is not None:
        
        if not args.method or args.method[0].upper() not in ["POST", "PUT", "DELETE", "GET"]:
            method = "GET"
        else:
            method = args.method[0].upper()
        
        # "http://localhost:5000"
        # "https://localhost:8080"
        url = args.url[0].lower()
        
        data = ""
        if args.data:
            with open(args.data[0], 'r') as f:
                data = json.load(f)
    
    
    headrs = {'Content-Type' : 'application/json'}
    creds = "user007:python"
    headrs['Authorization'] = b"Basic " + base64.b64encode(creds.encode('ascii'))
    
    call(url, headrs = headrs, method = method)

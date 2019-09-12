from flask import Flask
from flask import jsonify
from flask import request,make_response
from flask_api import status
from gevent.pywsgi import WSGIServer
import mongoconnect as db
from settings import LOGGER
import os
from utils import response_data
app = Flask(__name__)
mongo=db.Mongodb()

@app.route('/getcollections',methods=['GET'])
def get_collections():
    try:
        response=mongo.get_collections()
        LOGGER.info("Response = %s",response)
        return response
    except Exception as exp:
        LOGGER.error("message= %s",str(exp))
        return response_data(str(exp),status.HTTP_400_BAD_REQUEST)
        
@app.route('/insert',methods=['POST'])
def insert_doc():
    try:
        req = request.get_json()
        response=mongo.insert(req)
        LOGGER.info("Response = %s",response)
        return response
    except Exception as exp:
        LOGGER.error("message= %s",str(exp))
        return response_data(str(exp),status.HTTP_400_BAD_REQUEST)


@app.route('/find',methods=['GET'])
def get_documents():
    try:
        collection =request.args.get("collection")
        req=request.get_json()
        response=mongo.find(collection,req)
        LOGGER.info("Response = %s",response)
        return response
    except Exception as exp:
        LOGGER.error("message= %s",str(exp))
        return response_data(str(exp),status.HTTP_400_BAD_REQUEST)

@app.route('/update',methods=['POST'])
def update_doc():
    try:
        collection=request.args.get("collection")
        create=request.args.get("create")
        many = request.args.get("many")
        req=request.get_json()
        response=mongo.update(collection,req,create,many)
        LOGGER.info("Response = %s",response)
        return response
    except Exception as exp:
        LOGGER.error("message= %s",str(exp))
        return response_data(str(exp),status.HTTP_400_BAD_REQUEST)

@app.route('/delete',methods=['POST'])
def delete_doc():
    try:
        collection=request.args.get("collection")
        many = request.args.get("many")
        query=request.get_json()["query"]
        response=mongo.delete(query,collection,many)
        LOGGER.info("Response = %s",response)
        return response
    except Exception as exp:
        LOGGER.error("message= %s",str(exp))
        return response_data(str(exp),status.HTTP_400_BAD_REQUEST)


if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', 8002), app)
    http_server.serve_forever()
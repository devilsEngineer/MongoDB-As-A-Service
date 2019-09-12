from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_api import status
from bson.json_util import dumps
import settings
from utils import convert2bool,response_data
class Mongodb():

    def __init__(self):
        try:
            self.connect()
            user = settings.USER
            pwd =settings.PWD
            if user is not None:
                self.set_db(user,pwd)
            else:
                self.set_db()
            settings.LOGGER.info("Message= %s","Mongo DB connection Successful")
        except Exception as exp:
            settings.LOGGER.error("message= %s",str(exp)) 

    def connect(self):
        try:
            self.client= MongoClient(settings.HOST, int(settings.PORT))
        except Exception as exp:
            settings.LOGGER.error("message= %s",str(exp)) 

    def set_db(self,user=None,pwd=None):
        try:
            self.database=self.client[settings.DATABASE]
            if user is not None:
                self.database.authenticate(user,pwd)
        except Exception as exp:
            settings.LOGGER.error("message= %s",str(exp))

    def set_collection(self,collection):
        try:
            self.collection=self.database[collection]
        except Exception as exp:
            settings.LOGGER.error("message= %s",str(exp))

    def get_collections(self):
        """
        Get list of collections from DB
        """
        try:
            collection_list=self.database.collection_names()
            settings.LOGGER.info("Response Data= %s",collection_list) 
            return response_data(collection_list,status.HTTP_200_OK)
        except Exception as exp:
            settings.LOGGER.error("message= %s",str(exp))
            return response_data(str(exp),status.HTTP_400_BAD_REQUEST)
            
    def insert(self,request):
        """
        Insert a doc to collection
        Document : data to insert
        """
        try:
            data= request["Document"]
            self.set_collection(request["collection"])
            if type(data) is list:
                self.collection.insert_many(data)
            else:
                self.collection.insert(data)
            settings.LOGGER.info("Response Data= %s","INSERT SUCCESSFUL") 
            return response_data("INSERT SUCCESSFUL",status.HTTP_200_OK)
        except Exception as exp:
            settings.LOGGER.error("message= %s",str(exp))
            return response_data(str(exp),status.HTTP_400_BAD_REQUEST)

    def find(self,collection,request):
        """
        Find a doc from a collection
        query : condition to find
        """
        try:
            self.set_collection(collection)
            print(self.get_collection_keys())
            data={}
            if request is not None and "query" in request:
                data= request["query"]

            if '_id' in data:
                data['_id']=ObjectId(data['_id'])

            cursor=self.collection.find(data)
            response={}
            result=[doc for doc in cursor]
            for doc in result:
                doc["_id"]=str(doc["_id"])
            response.update({'data':result})
            response.update({'count':len(response['data'])})
            settings.LOGGER.info("Response Data= %s",response) 
            return response_data(response,status.HTTP_200_OK)
        except Exception as exp:
            settings.LOGGER.error("message= %s",str(exp))
            return response_data(str(exp),status.HTTP_400_BAD_REQUEST)

    def update(self,collection,request,create=False,many=False):
        """
        Update a doc from a collection
        query : condition to update
        Document : data to update with
        many : boolean to update more than one
        create : boolean to create if doesn't exist
        """
        try:
            self.set_collection(collection)
            create=convert2bool(create)
            if request is not None and "query" in request:
                query= request["query"]
                data= request["Document"]

            if '_id' in query:
                query['_id']=ObjectId(query['_id'])

            if many:
                self.collection.update_many(query,{ "$set": data},upsert=create)
            else:
                self.collection.update_one(query,{ "$set": data},upsert=create)  
            settings.LOGGER.info("Response Data= %s","UPDATE SUCCESSFUL")   
            return response_data("UPDATE SUCCESSFUL",status.HTTP_200_OK)
        except Exception as exp:
            settings.LOGGER.error("message= %s",str(exp))
            return response_data(str(exp),status.HTTP_400_BAD_REQUEST)

    def delete(self,query,collection,many=False):
        """
        Delete a doc from a collection
        query : condition for delete
        many : boolean to delete more than one
        """
        try:
            self.set_collection(collection)
            many=convert2bool(many)
            if '_id' in query:
                query['_id']=ObjectId(query['_id'])

            if many:
                self.collection.delete_many(query)
            else:
                self.collection.delete_one(query)
            settings.LOGGER.info("Response Data= %s","DELETE SUCCESSFUL")   
            return response_data("DELETE SUCCESSFUL",status.HTTP_200_OK)
        except Exception as exp:
            settings.LOGGER.error("message= %s",str(exp))
            return response_data(str(exp),status.HTTP_400_BAD_REQUEST)

    def get_collection_keys(self):
        """Get a set of keys from a collection"""
        keys_list = []
        collection_list = self.collection.find({})
        for document in collection_list:
            for field in document.keys():
                keys_list.append(field)
        keys_set =  set(keys_list)
        return keys_set

    

"""
mongo=Mongodb()
mongo.set_collection('test1')
mongo.get_collections()
#mongo.insert({"name":"ananthu"})
#mongo.insert([{"name":"akhil"},{"name":"albin"}])
#mongo.find({'name': 'ananthu'}) 
"""
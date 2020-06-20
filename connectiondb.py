import pymongo
from bson.objectid import ObjectId
def connection(collection):
    connect = "mongodb+srv://osmanballi:hqlcYHbIqPKfAowd@cluster0-cpclg.mongodb.net/node-app?retryWrites=true&w=majority"
    myclient = pymongo.MongoClient(connect)
    mydb=myclient["Movie-App"]
    mycollection = mydb[collection]
    return mycollection
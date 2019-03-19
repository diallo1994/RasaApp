import pymongo
from bson.objectid import ObjectId

def createDB(DBname,Cname,url):
      myclient = pymongo.MongoClient(url) #"mongodb://10.31.11.147:27017/"
      mydb = myclient[DBname]
      dblist = myclient.list_database_names()
      if DBname in dblist:
        print("The database exists.")

      # Create an collection
      mycol = mydb[Cname]
      # print(mydb.list_collection_names())
      collist = mydb.list_collection_names()
      if Cname in collist:
        print("The collection exists.")
      return mycol

def addOneDocument(DBname,Cname,url,document):
  collection=createDB(DBname,Cname,url)
  return collection.insert_one(document)

def addManyDocument(DBname,Cname,url,document):
  collection=createDB(DBname,Cname,url)
  return collection.insert_many(document)

# mydict = { "name": "John", "address": "Highway 37" }
# mylist = [
#   { "_id": 1, "name": "John", "address": "Highway 37"},
#   { "_id": 2, "name": "Peter", "address": "Lowstreet 27"},
#   { "_id": 3, "name": "Amy", "address": "Apple st 652"},
#   { "_id": 4, "name": "Hannah", "address": "Mountain 21"},
#   { "_id": 5, "name": "Michael", "address": "Valley 345"},
#   { "_id": 6, "name": "Sandy", "address": "Ocean blvd 2"},
#   { "_id": 7, "name": "Betty", "address": "Green Grass 1"},
#   { "_id": 8, "name": "Richard", "address": "Sky st 331"},
#   { "_id": 9, "name": "Susan", "address": "One way 98"},
#   { "_id": 10, "name": "Vicky", "address": "Yellow Garden 2"},
#   { "_id": 11, "name": "Ben", "address": "Park Lane 38"},
#   { "_id": 12, "name": "William", "address": "Central st 954"},
#   { "_id": 13, "name": "Chuck", "address": "Main Road 989"},
#   { "_id": 14, "name": "Viola", "address": "Sideway 1633"}
# ]

def findVectorOfOneDocument(DBname,Cname,url,id):
  collection=createDB(DBname,Cname,url)
  myquery = { "_id": ObjectId(id)}
  print(myquery)
  mydoc = collection.find_one(myquery)
  print(mydoc)
  return mydoc

def findDocuments(DBname,Cname,url):
  collection=createDB(DBname,Cname,url)
  print(collection.find().count())
  return collection.find()





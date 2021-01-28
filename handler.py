import json
from bson import ObjectId
import pymongo
from db.dbs import dbs
dbs=dbs()
db=dbs.setrecord()

def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        # "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """

def insert(event, context):
    try:
        data=json.loads(event['body'])
        db.myTbl.insert(data)
        print("data insert successfully")
        response=event['body']
        return response
    except:
        print("Error!")

def update(event, context):
    try:
        _id=event['pathParameters']['id'] 
        dataSet=json.loads(event['body'])
        db.myTbl.update_one({'_id':ObjectId(_id)},{'$set':dataSet},upsert=True)
        response=event['body']
        return response
    except:
        print("Error!")

def delete(event, context):
    try:
        _id=event['pathParameters']['id'] 
        db.myTbl.delete_one({'_id':ObjectId(_id)})
        result = { 
            "message": "Delete successfully",
        }
        response = {
            "statusCode":200,
            "body":json.dumps(result)
        }
        return response
    except:
        print("Error!")

def viewbyid(event, context):
    try:
        print(event['pathParameters'])
        _id=event['pathParameters']['id'] 
        result = db.myTbl.find_one({'_id':ObjectId(_id)})   
        result.update({'_id':str(result['_id'])})
        response = {
            "statusCode":200,
            "body":json.dumps(result)
        }
        return response
    except:
        print("Error!")

def allview(event, context):
    try:
        result=db.myTbl.find()
        data = []
        for r in result:
            r.update({'_id':str(r['_id'])})
            data.append(r)

        response = {
            "statusCode":200,
            "body":json.dumps({
                "user":data
            })
        } 
        return response
    except:
        print("Error!")
def joining_view(event, context):
    result = db.myTbl.aggregate([ {'$lookup' : {'from': 'myTbl1','localField': 'name','foreignField': 'name','as': 'results' }}])
    # print(result)
    data=[]
    for i in result:
        if i['results']:
            i.update({'_id':str(i['_id'])})
            for j in i['results']:
                j.update({'_id':str(j['_id'])})
            data.append(i)
                
            
    response = {
            "statusCode":200,
            "body":json.dumps({
                "user":data
            })
        }
    return response
def viewbyname(event, context):
    name=event['queryStringParameters']['name']
    # dataSet=json.loads(event['body'])
    # name=None
    # for key,value in dataSet.items():
    #     name=value
    result=db.myTbl.find({ 'name' : {'$regex': '^'+name} })
    # result=db.myTbl.aggregate([ { '$match' : { 'name' : name } } ])
    data = []
    for r in result:
        r.update({'_id':str(r['_id'])})
        data.append(r)
    response = {
            "statusCode":200,
            "body":json.dumps({
                "user":data
            })
        }
    return response
def getData(event, context):
    try:
        print(event['pathParameters'])
        pathParam=event['pathParameters']
        limit=0
        skip=0
        print(pathParam['limit'].isnumeric())
        print(pathParam['skip'].isnumeric())
        if pathParam['limit'].isnumeric():
            if int(pathParam['limit']) <= 0:
                limit=0
            else:
                limit=int(pathParam['limit'])
        else:
            if pathParam['limit'].isalpha() or pathParam['limit'] == ' ':
                response = {
                            "statusCode":404,
                            "body":json.dumps({
                                "info":"Please enter positive number"
                            })
                        }
                return response
            else:
                limit=0
        if pathParam['skip'].isnumeric():
            if int(pathParam['skip']) <= 0:
                skip=0
            else:
                skip=int(pathParam['skip'])
        else:
            if pathParam['skip'].isalpha() or pathParam['skip'] == ' ':
                response = {
                            "statusCode":404,
                            "body":json.dumps({
                                "info":"Please enter positive number"
                            })
                        }
                return response
            else:
                skip=0
        
        result=db.myTbl.find().skip(skip).limit(limit)
        data = []
        for r in result:
            r.update({'_id':str(r['_id'])})
            data.append(r)
        response = {
                "statusCode":200,
                "body":json.dumps({
                    "user":data
                })
            }
        return response
    except:
        print("Error!")
def searching(event, context):
    name=None
    email=None
    result=None
    limit=0
    skip=0
    queryStringParameters=event['queryStringParameters']
    if queryStringParameters == None:
        result=db.myTbl.find().skip(skip).limit(limit)
    else:
        if queryStringParameters['limit'].isnumeric():
            if int(queryStringParameters['limit']) <= 0:
                limit=0
            else:
                limit=int(queryStringParameters['limit'])
        else:
            if queryStringParameters['limit'].isalpha() or queryStringParameters['limit'] == ' ':
                response = {
                            "statusCode":404,
                            "body":json.dumps({
                                "info":"Please enter positive number"
                            })
                        }
                return response
            else:
                limit=0
        if queryStringParameters['skip'].isnumeric():
            if int(queryStringParameters['skip']) <= 0:
                skip=0
            else:
                skip=int(queryStringParameters['skip'])
        else:
            if queryStringParameters['skip'].isalpha() or queryStringParameters['skip'] == ' ':
                response = {
                            "statusCode":404,
                            "body":json.dumps({
                                "info":"Please enter positive number"
                            })
                        }
                return response
            else:
                skip=0
        for key,value in queryStringParameters.items():
            if(key == 'name'):
                if(value != ''):
                    name=value
            if(key == 'email'):
                if(value != ''):
                    email=value
        if name != None and email != None:
            result=db.myTbl.aggregate([ { '$match' : { 'name' : {'$regex': '^'+name}, 'email': {'$regex': '^'+email} } },{'$skip': skip},{'$limit':limit} ])
        if name != None and email == None:
            result=db.myTbl.aggregate([ { '$match' : { 'name' : {'$regex': '^'+name}} },{'$skip': skip},{'$limit':limit} ])
        if name == None and email != None:
            result=db.myTbl.aggregate([ { '$match' : { 'email' : {'$regex': '^'+email}} },{'$skip': skip},{'$limit':limit} ])
    data = []
    for r in result:
        r.update({'_id':str(r['_id'])})
        data.append(r)
    response = {
            "statusCode":200,
            "body":json.dumps({
                "user":data
            })
        }
    return response
    


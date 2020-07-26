from flask import Flask

from flask_pymongo import PyMongo

from flask import jsonify,request

app = Flask(__name__)

app.config['MONGO_DBNAME']='prettyprinted_res'
app.config['MONGO_URI']= 'mongodb://localhost:27017/testdb'

mongo = PyMongo(app)

@app.route('/testdb', methods=['GET'])
def get_all_testdb():
    testdb = mongo.db.testdb

    output = []

    for q in testdb.find():
        output.append({'name':q['name'],'jobTitle':q['jobTitle'],'emailAddress':q['emailAddress'],'salary':q['salary']})

    return jsonify({'result':output})

@app.route('/testdb/<name>', methods = ['GET'])
def get_testdb(name):
    testdb = mongo.db.testdb

    q = testdb.find_one({'name':name})
    
    if q:
        output = {'name':q['name'],'jobTitle':q['jobTitle'],'emailAddress':q['emailAddress'],'salary':q['salary']}
    else:
        output = 'No Record'
    return jsonify({'result':output})

@app.route('/testdb', methods = ['POST'])
def add_testdb():
    testdb = mongo.db.testdb
    name = request.json['name']
    jobTitle = request.json['jobTitle']
    emailAddress = request.json['emailAddress']
    salary = request.json['salary']       

    try:
        testdb_name = testdb.insert({'name':name,'jobTitle':jobTitle,'emailAddress':emailAddress,'salary':salary})
        new_testdb = testdb.find_one({'_name':testdb_name})
        output = {'name':new_testdb['name'],'jobTitle':new_testdb['jobTitle'],'emailAddress':new_testdb['emailAddress'],'salary':new_testdb['salary']}
        return jsonify({'result': output['name'] + 'Added Sucessfully'})
    finally:
        return ({'msg': 'already exists'})





if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo, DESCENDING

from bson.json_util import dumps


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/academic_report"
mongo = PyMongo(app)


@app.route('/')
def test():
    # return "I'm totally on top of this!"
    user = mongo.db.marks.find_one({"subject": 'Mathematics'})
    #l =[]
    #for k,v in user:
    #   l.append()
    user.pop("_id")
    return jsonify({"msg":user})
    # return user

@app.route('/avgmath')
def avg_math():
    # return "I'm totally on top of this!"
    user = mongo.db.marks.find({"subject": 'Mathematics'})
    c = 0
    f = []
    su = 0
    for e in user:
        f.append(e)
    for i in f:
        su += i['marks']
        c += 1
    avg = su/c
    return jsonify({"Avg marks in Mathematics":avg})

@app.route('/avg')
def avg():
    sub = ['Mathematics', 'Telugu', 'English', 'Social', 'Physics', 'Chemistry']
    # return "I'm totally on top of this!"
    sub_avg = {}
    for i in sub:
        # print(sub[i])
        user = mongo.db.marks.find({"subject": i})
        c = 0
        f = []
        su = 0
        for e in user:
            f.append(e)
        for j in f:
            su += j['marks']
            c += 1
        avg = su/c
        print(avg)
        sub_avg[i]=avg
        print(sub_avg)
        # return jsonify({"Avg marks in"+str(sub[i]):avg})

    return jsonify({"Avg marks subject wise":sub_avg})

    # user = mongo.db.marks.find({"subject": 'Mathematics'}).sort("marks")

@app.route('/math')
def math_max():
    user = mongo.db.marks.find({"subject": 'Mathematics'}).sort("marks",DESCENDING).limit(1)
    l = dumps(user)
    return l

    # user = mongo.db.marks.find({"subject": 'Mathematics'}).sort("marks")

@app.route('/highest')
def highest():
    highest = mongo.db.marks.aggregate(
        [
        {
        "$group":
            {
            "_id": "$name",
            "sum": { "$sum": "$marks"}

            }
        }
    ]
    )
    l= [(doc["_id"],doc["sum"]) for doc in highest]
    x = max(l, key=lambda x:x[1])
    print(type(x))
    return jsonify({"Highest total":x})

@app.route('/lowest')
def lowest():
    lowest = mongo.db.marks.aggregate(
        [
        {
        "$group":
            {
            "_id": "$name",
            "sum": { "$sum": "$marks"}

            }
        }
    ]
    )
    l= [(doc["_id"],doc["sum"]) for doc in lowest]
    x = min(l, key=lambda x:x[1])
    print(type(x))
    return jsonify({"Lowest total":x})

@app.route('/newsub', methods=['POST'])
def add_sub():
    data = request.get_json()
    subject = data["subject"]
    name = data["name"]
    n_id = mongo.db.faculty.insert({'subject': subject, 'name': name})
    new_en = mongo.db.faculty.find_one({'_id': n_id })
    output = {'subject' : new_en['subject'], 'name' : new_en['name']}
    return jsonify({'result' : output})


@app.route('/newformsub', methods=['POST'])
def add_sub_form(): # To add using form data
    subject = request.form.get('subject')
    print("000000000000000000000000000000000000000000000000000000000000000000")
    name = request.form.get('name')
    print(subject)
    print(type(subject))
    n_id = mongo.db.faculty.insert({'subject': subject, 'name': name})
    new_en = mongo.db.faculty.find_one({'_id': n_id })
    output = {'subject' : new_en['subject'], 'name' : new_en['name']}
    return jsonify({'result' : output})


@app.route('/manins', methods=['POST'])
def manins():
    data = request.get_json()
    print(data)
    print(data['name'])
    # subject = data["subject"]
    # name = data["name"]
    # n_id = mongo.db.faculty.insert({'subject': subject, 'name': name})
    # new_en = mongo.db.faculty.find_one({'_id': n_id })
    # output = {'subject' : new_en['subject'], 'name' : new_en['name']}
    # return jsonify({'result' : output})
    return jsonify({'result' : "I got this"})
    
# {{"name":"Andromeda Galaxy", "distance": "25321425"}, {"name":"Nigga Galaxy", "distance": "253214254555"}}

@app.route('/newcol')
def newcol():
    # return "I'm totally on top of this!"
    user = mongo.db.marks.find()
    # user = mongo.db.marks.find({"name": 'student1'})

    print(user)
    subs = {}
    for i in user:
        if i["name"] not in subs:
            subs[i["name"]] = {i["subject"]:i["marks"]}
        else:
            subs[i["name"]].update({i["subject"]:i["marks"]})

    for j, k in subs.items():
        mongo.db.stu_marks.insert({j:k})
    return jsonify({"Avg marks in Mathematics":"avg"})

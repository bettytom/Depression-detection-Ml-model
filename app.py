from flask import Flask, render_template,json
from flask import request
import json
import mysql.connector
import pickle
import numpy as np
model=pickle.load(open('dcmodel.pkl','rb'))
app=Flask(__name__,template_folder='templates')
@app.route('/')
def home():
    return render_template('MLhomepage.html')

@app.route('/userview.html')
def user():
    return render_template('userview.html')

@app.route('/usertests.html')
def usertest():
    return render_template('usertests.html')

@app.route('/reviews.html')
def review():
    return render_template('reviews.html')

@app.route('/formlogin.html')
def login():
    return render_template('formlogin.html')

@app.route('/about.html')
def aboutus():
    return render_template('about.html')

@app.route('/adminform.html')
def admin():
    return render_template('adminform.html')

@app.route('/dashboard.html')
def dash():
    return render_template('dashboard.html')

@app.route('/moodquiz.html')
def quiz():
    return render_template('moodquiz.html')

@app.route('/form2.html')
def survey():
    return render_template('form2.html')

@app.route('/form3.html')
def survey2():
   return render_template('form3.html')

@app.route('/predictionreport.html')
def outcome():
   return render_template('predictionreport.html')

@app.route('/admin',methods=['POST','GET'])
def admindata():
     if request.method == 'POST':
        ad=request.form.get('adid')
        email=request.form.get('email')
        name=request.form.get('name')
        my_db=mysql.connector.connect(host="localhost",port="3306",user="root",passwd="",database="healthadmin")
        my_cursor=my_db.cursor()
        my_cursor.execute("INSERT INTO admin(adminid,email,pass) VALUES(%s,%s,%s)",(ad,email,name))
        my_db.commit()
        my_cursor.close()
        return render_template('adminform.html')

@app.route('/data',methods=['POST','GET'])
def showdata():
     if request.method == 'POST':
        id=request.form.get('usid')
        gender=request.form.get('sex')
        number=request.form.get('number')
        school=request.form.get('educ')
        mail=request.form.get('mail')
        passw=request.form.get('passw')
        my_db=mysql.connector.connect(host="localhost",port="3306",user="root",passwd="",database="depression")
        my_cursor=my_db.cursor()
        my_cursor.execute("INSERT INTO user(userid,gender,phonenumber,education,email,pass) VALUES(%s,%s,%s,%s,%s,%s)",(id,gender,number,school,mail,passw))
        my_db.commit()
        my_cursor.close()
        return render_template('form3.html')


@app.route('/predict',methods=['POST','GET'])
def prediction():
    if request.method == 'POST':
        ed=request.form.get('edu')
        expenses=request.form.get('exp')
        alcohol=request.form.get('alc')
        amount=request.form.get('chamount')
        food=request.form.get('foodad')
        food2=request.form.get('foodcd')
        sick=request.form.get('sickdays')
        cigar=request.form.get('smoke')

        test_data = [ed, expenses, alcohol, amount,food,food2,sick,cigar]
        print(test_data)
        #convert value data into numpy array
        test_data = np.array(test_data)
        #reshape array
        test_data = test_data.reshape(1,-1)
        print(test_data)
        #predict
        prediction = model.predict(test_data)

        #jsonfile
        columns=['education','medicalexpenses','alcohol','childeduexpenses','adultsmissedfood','chmissedfood','housesickdays','tobacco']
        list = [ed,expenses, alcohol, amount,food,food2,sick,cigar]
        for i in columns:
            list.append(i)
        data=[]
        for i in list:
            data.append(i)
        with open("predictform.json","w") as file:
            json.dump(data,file)
        return render_template('form2.html', pred="Probability of depression is {}".format(prediction))

if __name__== '__main__' :
    app.run(port=5000,debug=True)

   



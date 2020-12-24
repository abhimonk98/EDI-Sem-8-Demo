from flask import Flask, render_template, request, redirect
import pandas as pd 
import numpy as np

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        login = request.form.get('role')
        if login=='SugarFactory':
            return redirect('/sugar-factory-home')
        else:
            return redirect('/mukadam-home')

@app.route('/sugar-factory-home',methods=['GET'])
def sugarfactoryhome():
    return render_template('sugar-factory-home.html')

@app.route('/mukadam-home',methods=['GET'])
def mukadamhome():
    return render_template('mukadam-home.html')

@app.route('/mukadam-send-request',methods=['GET','POST'])
def mukadamsendrequest():
    data = pd.read_csv("sugar_factories_maharashtra.csv")
    data = data.replace(np.nan,0)
    talukas = pd.read_csv("districts.csv")

    if request.method=='GET':
        return render_template('mukadam-send-request.html',sugar_factory=data,talukas=talukas,districts=talukas.District.unique())
    elif request.method=='POST':
        return redirect('/mukadam-send-request')

@app.route('/mukadam-enter-worker-performance',methods=['GET','POST'])
def mukadamenterworkerperformance():
    return render_template('mukadam-enter-worker-performance.html')

@app.route('/mukadam-register-worker',methods=['GET','POST'])
def mukadamregisterworker():
    if request.method == 'GET':
        return render_template('mukadam-register-worker.html')
    elif request.method == 'POST':
        data = pd.read_csv("sugar_factories_maharashtra.csv")
        data = data.replace(np.nan,0)
        talukas = pd.read_csv("districts.csv")

        if(request.form.get('aadhar')=="1"):
            message="Worker is already registered! Cannot register again."
        else:
            message=""
        return render_template('mukadam-register-worker.html',message=message,talukas=talukas,districts=talukas.District.unique())

if __name__ == "__main__":  
    
    # print(type(data)) 
    app.run( debug=True, threaded=True, host='0.0.0.0')
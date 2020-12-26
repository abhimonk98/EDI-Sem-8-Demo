from flask import Flask, render_template, request, redirect, session
import pandas as pd
import numpy as np
from flask_session import Session
import datetime
from multidict import MultiDict

app = Flask(__name__)

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        login = request.form.get('role')

        if login == 'SugarFactory':
            id = int(request.form.get('id'))
            session['id'] = id
            session['type'] = 'sugar factory'
            return redirect('/sugar-factory-home')
        else:
            id = int(request.form.get('id'))
            session['id'] = id
            session['type'] = 'mukadam'
            mukadam = pd.read_csv('mukadam.csv')
            found = mukadam['aadhar'].where(mukadam['aadhar'] == id).count()
            if found > 0:
                return redirect('/mukadam-home')
            else:
                return 'Please Register Yourself'


@app.route('/sugar-factory-home', methods=['GET'])
def sugarfactoryhome():
    return render_template('sugar-factory-home.html')


@app.route('/mukadam-home', methods=['GET'])
def mukadamhome():
    return render_template('mukadam-home.html')


@app.route('/mukadam-dashboard', methods=['GET'])
def mukadamdashboard():
    return render_template('mukadam-dashboard.html')


@app.route('/mukadam-send-request', methods=['GET', 'POST'])
def mukadamsendrequest():
    data = pd.read_csv("sugar_factories_maharashtra.csv")
    data = data.replace(np.nan, 0)
    talukas = pd.read_csv("districts.csv")
    mukadam_data = pd.read_csv('mukadam.csv')
    found_mukadam = mukadam_data[mukadam_data['aadhar'] == session.get('id')]
    # print(found_mukadam)
    current_no_of_workers = mukadam_data.loc[found_mukadam.index, 'current no of workers']
    # current_no_of_workers = mukadam_data[mukadam_data['']]
    current_no_of_workers = current_no_of_workers.iloc[0]
    # print(current_no_of_workers)

    if request.method == 'GET':
        return render_template('mukadam-send-request.html',
                               sugar_factory=data,
                               talukas=talukas,
                               districts=talukas.District.unique(), current_no_of_workers=current_no_of_workers)
    elif request.method == 'POST':
        form = MultiDict(request.form)
        factory_code = 0

        for i in form:
            if i.find('button') == 0:
                factory_code = i.replace('button', 'input')
                break

        assigned_no_of_workers = int(form[factory_code])
        factory_code = int(factory_code.replace('input', ''))

        sugar_factory_data = pd.read_csv('sugar_factories_maharashtra.csv')
        mukadam_data = pd.read_csv('mukadam.csv')

        found_sugar_factory = sugar_factory_data[sugar_factory_data['Code No.'] == factory_code]
        found_sugar_factory_index = found_sugar_factory.index

        found_mukadam = mukadam_data[mukadam_data['aadhar'] == session.get('id')]
        found_mukadam_index = found_mukadam.index

        required_no_of_workers = found_sugar_factory.loc[found_sugar_factory_index]['Required no of workers']
        current_no_of_workers = found_mukadam.loc[found_mukadam_index]['current no of workers']

        required_no_of_workers = required_no_of_workers.tolist()
        current_no_of_workers = current_no_of_workers.tolist()

        required_no_of_workers = required_no_of_workers[0]
        current_no_of_workers = current_no_of_workers[0]

        if assigned_no_of_workers <= required_no_of_workers and assigned_no_of_workers <= current_no_of_workers:
            mukadam_data.at[
                found_mukadam_index, 'current no of workers'] = current_no_of_workers - assigned_no_of_workers
            mukadam_data.to_csv('mukadam.csv')

            # print(type(assigned_no_of_workers))

            requests_data = pd.read_csv('requests.csv')
            new_request = pd.DataFrame({
                "mukadam aadhar": [session.get('id')],
                "requested workers": [assigned_no_of_workers],
                "factory code no": [factory_code],
                "request date": [datetime.datetime.now().strftime("%x")],
                "request status": ['pending']
            })

            data = requests_data.append(new_request, ignore_index=True)
            print(data)
            data.to_csv('requests.csv', index=False)

            return '<h4>Successfully registered ' + str(assigned_no_of_workers) + ' workers!</h4>'

        else:
            return "<h4>ERROR: check your available workers/ factory's requirement!</h4> "


@app.route('/mukadam-enter-worker-performance', methods=['GET', 'POST'])
def mukadamenterworkerperformance():
    return render_template('mukadam-enter-worker-performance.html')


@app.route('/mukadam-assign-worker-to-factory', methods=['GET', 'POST'])
def mukadamassignfactorytoworker():
    if request.method == 'GET':
        mukadam_data = pd.read_csv('mukadam.csv')
        requests_data = pd.read_csv('requests.csv')

        found_mukadam = mukadam_data[mukadam_data['aadhar'] == session.get('id')]

        total_no_of_workers = mukadam_data.loc[found_mukadam.index, 'total no of workers']
        total_no_of_workers = total_no_of_workers.iloc[0]

        available_workers = mukadam_data.loc[found_mukadam.index, 'current no of workers']
        available_workers = available_workers.iloc[0]

        need_to_assign = total_no_of_workers - available_workers

        return render_template('mukadam-assign-factory-to-worker.html', need_to_assign=need_to_assign)

    return render_template('mukadam-assign-factory-to-worker.html')


@app.route('/register-mukadam', methods=['GET', 'POST'])
def registermukadam():
    if request.method == 'GET':
        return render_template('register-mukadam.html')
    elif request.method == 'POST':
        mukadam_data = pd.read_csv('mukadam.csv')
        worker_data = pd.read_csv('workers.csv')
        name = request.form.get('name')
        aadhar = int(request.form.get('aadhar'))
        mukadam_found = mukadam_data['aadhar'].where(mukadam_data['aadhar'] == aadhar).count()
        worker_found = worker_data['aadhar'].where(worker_data['aadhar'] == aadhar).count()
        if mukadam_found > 0 or worker_found > 0:
            return 'Aadhar no is already registered. Please try again!'
        else:
            new_data = pd.DataFrame({"name": [name],
                                     "aadhar": [aadhar],
                                     "current no of workers": [0],
                                     "total no of workers": [0],
                                     "registered date": [datetime.datetime.now().strftime("%x")]})
            data = mukadam_data.append(new_data, ignore_index=True)
            data.to_csv('mukadam.csv', index=False)
            return 'Mukadam is registered successfully!'


@app.route('/mukadam-register-worker', methods=['GET', 'POST'])
def mukadamregisterworker():
    if request.method == 'GET':
        return render_template('mukadam-register-worker.html')
    elif request.method == 'POST':

        data = pd.read_csv("sugar_factories_maharashtra.csv")
        data = data.replace(np.nan, 0)
        talukas = pd.read_csv("districts.csv")
        # worker_aadhar = request.form.get('aadhar')

        if 'aadhar' in request.form:
            worker_aadhar = request.form.get('aadhar')
            session['worker_aadhar'] = int(worker_aadhar)
            # print(session.get('worker_aadhar'))
            workers_data = pd.read_csv('workers.csv')
            mukadam_data = pd.read_csv('mukadam.csv')
            found_worker_aadhar = workers_data['aadhar'].where(workers_data['aadhar'] == int(worker_aadhar))
            found_mukadam_aadhar = mukadam_data['aadhar'].where(mukadam_data['aadhar'] == int(worker_aadhar))
            # found_worker_aadhar1 = workers_data[workers_data['aadhar'] == session.get('worker aadhar')]

            print(found_mukadam_aadhar.count())
            # print(found_worker_aadhar1)
            if found_worker_aadhar.count() > 0:
                message = "Worker already registered! cannot register now "
            elif found_mukadam_aadhar.count() > 0:
                # found_mukadam = mukadam_data[mukadam_data['aadhar'] == session.get('id')]
                message = "This aadhar no is registered by Mukadam ! cannot register now"
            else:
                message = ""
            return render_template('mukadam-register-worker.html',
                                   aadhar=worker_aadhar,
                                   message=message,
                                   talukas=talukas,
                                   districts=talukas.District.unique())
        elif 'name' in request.form:
            # worker_aadhar = request.form.get('worker_aadhar')
            workers_data = pd.read_csv('workers.csv')
            mukadam_data = pd.read_csv('mukadam.csv')
            # print(type(session.get('id')))
            found_mukadam = mukadam_data[mukadam_data['aadhar'] == session.get('id')]
            current_no_of_workers = mukadam_data.loc[found_mukadam.index, 'current no of workers']
            mukadam_data.at[found_mukadam.index, 'current no of workers'] = current_no_of_workers + 1
            mukadam_data.at[found_mukadam.index, 'total no of workers'] = current_no_of_workers + 1
            # print(found_mukadam)
            new_workers_data = pd.DataFrame({"first name": [request.form.get('name')],
                                             "aadhar": session.get('worker_aadhar'),
                                             "district": [request.form.get('district')],
                                             "registered date": [datetime.datetime.now().strftime("%x")],
                                             "Mukadam name": found_mukadam['name'][found_mukadam.index],
                                             "Mukadam Aadhar": [session.get('id')],
                                             "contact": [request.form.get('contact')],
                                             "gender": [request.form.get('gender')]})
            workers_data = workers_data.append(new_workers_data, ignore_index=True)
            # print(workers_data)
            workers_data.to_csv('workers.csv', index=False)
            mukadam_data.to_csv('mukadam.csv', index=False)
            return redirect('/mukadam-register-worker')
        else:
            return redirect('/mukadam-register-worker')


if __name__ == "__main__":
    app.run(debug=True, threaded=True, host='0.0.0.0')

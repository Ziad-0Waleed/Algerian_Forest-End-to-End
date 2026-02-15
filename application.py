import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle
from flask import Flask, request, jsonify, render_template

application = Flask(__name__)
app=application

ridge_model = pickle.load(open('models/ridge.pkl', 'rb'))
standard_scaler = pickle.load(open('models/scaler.pkl', 'rb'))



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        Temperature = float(request.form.get('Temperature'))
        RH = float(request.form.get('RH'))
        Ws = float(request.form.get('Ws'))
        Rain = float(request.form.get('Rain'))
        FFMC = float(request.form.get('FFMC'))
        DMC = float(request.form.get('DMC'))
        ISI = float(request.form.get('ISI'))
        Classes = float(request.form.get('Classes'))
        Region = float(request.form.get('Region'))

        new_scaled_data = standard_scaler.transform([[Temperature, RH, Ws, Rain, FFMC, DMC, ISI, Classes, Region]])
        prediction = ridge_model.predict(new_scaled_data)
        return render_template('home.html', result=round(prediction[0], 2))
    else:
        return render_template('home.html')

@app.route('/api/predict', methods=['POST'])
def predict_api():
    try:
        data = request.json
        Temperature = float(data['Temperature'])
        RH = float(data['RH'])
        Ws = float(data['Ws'])
        Rain = float(data['Rain'])
        FFMC = float(data['FFMC'])
        DMC = float(data['DMC'])
        ISI = float(data['ISI'])
        Classes = float(data['Classes'])
        Region = float(data['Region'])
        new_data_scaled = standard_scaler.transform([[Temperature, RH, Ws, Rain, FFMC, DMC, ISI, Classes, Region]])
        prediction = ridge_model.predict(new_data_scaled)

        return jsonify({
            'status': 'success',
            'prediction': round(prediction[0], 2)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 10:15:54 2021

@author: Nicolas Carval
"""

import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index2.html')

@app.route('/predict',methods=['POST'])
def predict():

    int_features = [x for x in request.form.values()]
    if int_features[-1] == "Autumn":
        int_features.pop()
        int_features.extend([1,0,0,0])
    elif int_features[-1] == "Spring":
        int_features.pop()
        int_features.extend([0,1,0,0])
    elif int_features[-1] == "Summer":
        int_features.pop()
        int_features.extend([0,0,1,0])
    else:
        int_features.pop()
        int_features.extend([0,0,0,1])
    
    int_features = [int(int_features[x]) if x not in [1,3] else float(int_features[x]) for x in range(len(int_features))]
    for elem in int_features:
        print(elem,' de type:',type(elem))
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0])

    return render_template('index2.html', prediction_text='Number of bike to be rented should be {0}'.format(output))

#@app.route('/results',methods=['POST'])
#def results():
#
#    data = request.get_json(force=True)
#    prediction = model.predict([np.array(list(data.values()))])
#    output = prediction[0]
#    return jsonify(output)

if __name__ == "__main__":
    app.run(host='localhost', port=8989)
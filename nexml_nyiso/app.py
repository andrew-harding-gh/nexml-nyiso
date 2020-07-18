import numpy as np
import pandas as pd
import pickle
from flask import Flask, jsonify, request, render_template
from plumbum import local

from nexml_nyiso.clients.weatherbit_client import WbClient
from nexml_nyiso.utility import JFK, LGA
from nexml_nyiso.notebooks.utils import preprocess


app = Flask(__name__)

app.secret_key = 'something_secret'

model_file = local.path(__file__).dirname / 'resources'/ 'model.h5'
MODEL = pickle.load(open(model_file, 'rb'))
WBCLIENT = WbClient(local.env['WB_KEY'])


@app.route('/predict', methods=['GET'])
def predict():
    if not request.json:
        return jsonify({'error': 'no request received'})

    forecast_data = WBCLIENT.get_hourly_forecast_by_station(JFK.id)
    fc_df = pd.DataFrame(forecast_data)
    processed = preprocess(fc_df)

    y_pred = MODEL.predict(processed)

    response = dict(PREDICTION=y_pred, **forecast_data)
    return jsonify(response)

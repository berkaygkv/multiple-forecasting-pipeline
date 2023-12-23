from pathlib import Path
import uvicorn
from fastapi import FastAPI
import joblib
import numpy as np
import os
import datetime
import json


app = FastAPI(title="Sales Prediction", debug=True)


def load_model(model_name):

    from fbprophet.serialize import model_from_json
    with open(ROOT_DIR.joinpath("models", model_name + ".json"), 'r') as fin:
        model = model_from_json(fin.read())  # Load model
    # model = joblib.load(ROOT_DIR.joinpath("models", model_name + ".pkl"))
    return model


def predict_next_nth_day(provider, periods=1):
    m = load_model(provider)
    future = m.make_future_dataframe(periods=periods, freq="D")
    pred = m.predict(future)
    pred = pred[["ds", "yhat", "yhat_lower", "yhat_upper"]].iloc[-1:]
    return pred


def list_all_models():
    model_paths = [
        k.replace(".json", "")
        for k in os.listdir(ROOT_DIR.joinpath("models"))
        if k.endswith(".json")
    ]
    return model_paths


@app.get("/")
def home():
    return {"message": "API working."}


@app.get("/predict_next_day/")
def predict(timestep):
    # assert provider != None
    conf_js = read_config_file()
    nth_day = int(timestep)
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    results = []
    for model_name in model_list:
        latest_train_date = datetime.datetime.strptime(
            conf_js[model_name][0]["latest_date"], "%d-%m-%Y"
        )
        training_gap = yesterday - latest_train_date
        training_gap_in_days = training_gap.days
        nth_day_modified = (
            nth_day if training_gap_in_days == 0 else training_gap_in_days + nth_day
        )
        df = predict_next_nth_day(model_name, nth_day_modified)
        df["provider"] = model_name
        df["ds"] = df["ds"].dt.strftime("%d-%m-%Y")
        df["mdape"] = conf_js[model_name][0]["mdape"] * 100
        df["mae"] = conf_js[model_name][0]["mae"]
        df["number_of_gaps_in_days"] = training_gap_in_days
        df.fillna("null", inplace=True)
        df = df.replace({np.inf: "positive inf", -np.inf: "negative inf"})
        result = df.to_dict(orient="records")[0]
        results.append(result)
    return results


def read_config_file():
    metric_path = ROOT_DIR.joinpath("product", "metrics", "performance_results.json")
    with open(metric_path, "r") as rd:
        conf_js = json.load(rd)
    return conf_js

file_path = os.path.abspath(__file__)
ROOT_DIR = os.path.dirname(file_path)
ROOT_DIR = Path(ROOT_DIR).parent
model_list = list_all_models()
# uvicorn.run(app, host="0.0.0.0", port=8080)

from fastapi import FastAPI
import pickle
import pandas as pd

app = FastAPI()

model_path = "../models/pipeline.pkl"
model = pickle.load(open(model_path, "rb"))

def calculate_year_range(year):
    bins = [1988, 1993, 1996, 1999, 2004, 2008, 2012, 2016, 2020, 2024]
    labels = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    return pd.cut([year], bins=bins, labels=labels)[0]

def calculate_km_range(kms):
    bins = [0, 30000, 60000, 90000, 120000, 150000, 180000, 210000, 240000, 
            270000, 300000, 330000, 360000, 390000, 410000, 440000, 470000, 
            500000, 533530]
    labels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    return pd.cut([kms], bins=bins, labels=labels)[0]

@app.post("/predict")
def predict(data: dict):
    if 'Year' in data:
        data['Year_Range'] = int(calculate_year_range(data['Year']))
    if "KM's driven" in data:
        data["KM's driven_Range"] = int(calculate_km_range(data["KM's driven"]))
    
    input_df = pd.DataFrame([data])
    
    try:
        prediction = model.predict(input_df)
        prediction = prediction.round(0).astype(int)
    except Exception as e:
        return {"error": str(e)}
    
    return {"prediction": prediction.tolist()}

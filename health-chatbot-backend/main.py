import os
import pandas as pd
from fastapi import FastAPI,Query
from fastapi.middleware.cors import CORSMiddleware

# Get the current folder (where main.py is)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build correct paths for CSVs
homeopathy_csv = os.path.join(BASE_DIR, "sample_20_diseases_detailed_symptoms_homeopathy_sources.csv")
remedies_csv = os.path.join(BASE_DIR, "home_remedies.csv")

# Load datasets
homeopathy_df = pd.read_csv(homeopathy_csv)
home_remedies_df = pd.read_csv(remedies_csv)

app = FastAPI()

# Enable CORS so frontend can connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Chatbot API running successfully!"}

@app.get("/get_diseases")
def get_diseases(type: str):
    if type == "homeopathy":
        diseases = homeopathy_df["Disease Name"].unique().tolist()
    else:
        diseases = home_remedies_df["Disease"].unique().tolist()
    return {"diseases": diseases}

@app.get("/get_symptoms")
def get_symptoms(disease: str, type: str):
    if type == "homeopathy":
        row = homeopathy_df[homeopathy_df["Disease Name"].str.lower() == disease.lower()]
        if row.empty:
            return {"error": "Disease not found"}
        symptoms = row.iloc[0]["Symptoms"].split(",")
    else:
        row = home_remedies_df[home_remedies_df["Disease"].str.lower() == disease.lower()]
        if row.empty:
            return {"error": "Disease not found"}
        symptoms = row.iloc[0]["Symptoms"].split(",")
    return {"symptoms": [s.strip() for s in symptoms]}

@app.get("/get_treatment")
def get_treatment(disease: str, type: str, selected_symptoms: list[str] = Query(...)):
    if len(selected_symptoms) < 2:
        return {"error": "Please select at least 2 symptoms"}

    if type == "homeopathy":
        row = homeopathy_df[homeopathy_df["Disease Name"].str.lower() == disease.lower()]
        if row.empty:
            return {"error": "Disease not found"}
        return {
            "disease": disease,
            "symptoms": selected_symptoms,
            "medicine": row.iloc[0]["Homeopathy Medicines"],
            "source": row.iloc[0]["Source"]
        }
    else:
        row = home_remedies_df[home_remedies_df["Disease"].str.lower() == disease.lower()]
        if row.empty:
            return {"error": "Disease not found"}
        return {
            "disease": disease,
            "symptoms": selected_symptoms,
            "home_remedy": row.iloc[0]["Home Remedy"],
            "preparation": row.iloc[0]["Preparation"],
            "source": row.iloc[0]["Source"]
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

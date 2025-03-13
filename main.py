import re
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

file_path = "dataset.csv"
dataset = pd.read_csv(file_path)
egyptian_cities = set()
for city_list in dataset["cities"]:
    for city in city_list.split("|"): 
        egyptian_cities.add(city.strip())

def extract_cities(query: str):
    found_cities = [city for city in egyptian_cities if re.search(rf"\b{re.escape(city)}\b", query, re.IGNORECASE)]
    return found_cities

@app.post('/extract')
def extract_entities(query_request: QueryRequest):
    query = query_request.query
    extracted_cities = extract_cities(query)

    if not extracted_cities:
        return {"cities": []}
    
    return {"cities": extracted_cities}

if __name__ == "__main__":
    load_dotenv()
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT",800)))

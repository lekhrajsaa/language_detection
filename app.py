#import required libraries
from fastapi import FastAPI
import uvicorn
import pickle
import pandas as pd
import numpy as np
import os

#initialize the app
app = FastAPI()

#function which vectorizes the input sentence using the vectorizer pickle file
def feature(vectorizer,corpus):
    X = vectorizer.fit_transform(corpus)
    features = vectorizer.get_feature_names_out()
    train_features = pd.DataFrame(data=X.toarray(),columns=features)
    
    return train_features

#execute command to print present working directory
path = os.getcwd()

#load the vectorizer pickle file , model pickle file and label encoder pickle file
vectorizer = pickle.load(open(f'{path}/vectorizer', 'rb'))
encoder = pickle.load(open(f'{path}/encoder', 'rb'))
model = pickle.load(open(f"{path}/finalized_model.sav",'rb'))


#function to get the prediction from the model
def predict(sentence):
    sentence = [sentence]
    vector = feature(vectorizer,sentence)
    label = model.predict(vector)
    conf = np.amax(label,axis=1)
    label=np.argmax(label,axis=1)
    prediction = encoder.inverse_transform(label)   
    return str(prediction[0]) ,float(conf[0])

#root route to check if the app is running
@app.get("/")
def root():
    return {"message": "Hello World"}

#route to get the prediction from the model
#sample command to check 
#curl -i -H "Content-Type: application/json" -X POST -d '{"text": "this is a trial ip"}' 139.59.4.62:8000/lang_id
@app.post("/lang_id")
def lang_id(dict : dict):
    try:
        sentence = dict['text']
    except:
        return {"message": "Please provide a text"}
    prediction,conf = predict(sentence)
    return {prediction: conf}

#run the app 
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 

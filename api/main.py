
from fastapi import FastAPI

import pickle

#Text preprocess function
from limpieza import preprocess

from decouple import config

from fastapi.middleware.cors import CORSMiddleware

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, HTMLResponse

import requests



import pandas as pd


app = FastAPI()
# configure header parameters to access

# Conection with react port
origins = [
    "http://localhost:3000",
    "localhost:3000"
]
app.add_middleware(
    CORSMiddleware, # https://fastapi.tiangolo.com/tutorial/cors/
    allow_origins=['*'], # wildcard to allow all, more here - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin
    allow_credentials=True, # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Credentials
    allow_methods=['*'], # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Methods
    allow_headers=['*'], # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Headers
)


#Vectoriser
with open ('Vectoriser.pkl', 'rb') as d:
    vectoriser = pickle.load(d)
#Model 
with open ('MultinomialNB_NLP.pkl', 'rb') as f:
    model = pickle.load(f)


@app.get("/predict")
async def predict_hate(prompt:str):
    
    processed_data= preprocess([prompt])
    print(processed_data)
    vectorised_data = vectoriser.transform(processed_data)
    print(vectorised_data)
    prediction = model.predict(vectorised_data)
    print('----------------PREDICTION---------------------')
    print(prediction)
    
    value = 'Toxic comment' if prediction == 1 else 'Not toxic'
    
     # Convert predictions into JSON format
    json_compatible_item_data = jsonable_encoder(value)
    return JSONResponse(content=json_compatible_item_data)

@app.get("/predict_youtube_comment")
async def predict_youtubeVid(prompt:str):
    video_id = prompt
    YOUTUBE_API_KEY = config("YOUTUBE_API_KEY")
    print(config("YOUTUBE_API_KEY"),YOUTUBE_API_KEY)
    response = requests.get(f"https://youtube.googleapis.com/youtube/v3/commentThreads?part=id%2C%20snippet&maxResults=5&videoId={video_id}&key={YOUTUBE_API_KEY}")

   # From Json to Dataframe
    data = response.json()
    # print(data)
    print((data), 'PRINT THE DATA FROM THE JSON')
    #create a dict from the json and index only the comments from video
    
    #lista vacia con los reultados de los comentarios
    predictions= []
    
    x = range(5)
    for n in x:
      comments = dict(comment_threads= data['items'][n]['snippet']["topLevelComment"]["snippet"]['textDisplay'], index=[n])
      
    
      
    # create a df from the dict
      df = pd.DataFrame.from_dict(comments)
      print (df['comment_threads'])

# select only the comments column from the df
    
   

    # Apply ML model
      processed_data= preprocess(df['comment_threads'])
   
      print(processed_data)
      vectorised_data = vectoriser.transform(processed_data)
      print(vectorised_data)
      prediction = model.predict(vectorised_data)
      print('----------------PREDICTION---------------------')
      print(prediction)
    
      
      

      value = 'Toxic comment' if prediction == 1 else 'Not toxic'
      predictions.append(value)

    print(predictions)

    results = dict(zip(range(len(predictions)), predictions))

    print(results)
      

    

    

    

    

    


     

    
    
    return {
#     # If prediction is a data frame use this to respond to the client
        'Video Comments' : results
      }
    
    

    







    

   
    
    
    




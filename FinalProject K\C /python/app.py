import psycopg2
from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.sql.functions import count
from sqlalchemy import create_engine
from psycopg2.extras import RealDictCursor
from datetime import datetime
import pandas as pd
from catboost import CatBoostClassifier
from load_my_features import batch_load_sql, load_features
from model_loading import get_model_path, load_models
from schema import PostGet
from get_top_5_posts import get_top_5_posts
import os


database = 'postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml'

model = load_models()
data = load_features().drop('target', axis=1)


app = FastAPI()
@app.get('/post/recommendations/', response_model=List[PostGet])
def recommended_posts(id: int, limit: int=5) -> List[PostGet]:
    user_data = data[data['user_id'] == id]

    posts = []

    for i in range(user_data.shape[0]):
        if model.predict(user_data.iloc[i]) == 1:
            post_id = user_data.iloc[i]['post_id']

            id_of_post = post_text[post_text['post_id'] == post_id].values[0][0]
            text_of_post = post_text[post_text['post_id'] == post_id].values[0][1]
            topic_of_post = post_text[post_text['post_id'] == post_id].values[0][2]

            if len(posts) < limit:
                posts.append({
                    'id': id_of_post,
                    'text': text_of_post,
                    'topic': topic_of_post
                })

            else:
                break

    if len(posts) < limit:
        post_text = pd.read_sql(
            'SELECT post_id, text, topic FROM post_text_df',
            database
        )

        return get_top_5_posts(post_text)

    else:
        return posts
    
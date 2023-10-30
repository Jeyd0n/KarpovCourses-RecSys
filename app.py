import os
import sys

sys.path.append('..')


from typing import List
from fastapi import FastAPI
import pandas as pd
from modules.load_my_features import load_features
from modules.model_loading import load_models
from modules.schema import PostGet
from modules.get_top_5_posts import get_top_5_posts
import os


sys.path.append('..')

database = os.getenv('POSTGRES_KEY')
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
    
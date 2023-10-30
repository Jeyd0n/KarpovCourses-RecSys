def get_top_5_posts(post_text):
    top_5_posts = []

    for post_id in (7093, 3121, 3694, 3639, 3428):
        id_of_post = post_text[post_text['post_id'] == post_id].values[0][0]
        text_of_post = post_text[post_text['post_id'] == post_id].values[0][1]
        topic_of_post = post_text[post_text['post_id'] == post_id].values[0][2]

        top_5_posts.append({
                    'id': id_of_post,
                    'text': text_of_post,
                    'topic': topic_of_post
                })
        
    return top_5_posts
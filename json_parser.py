import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.parser import isoparse

def plot_comments(comments_file):
    with open(comments_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    comments = []
    likes = []
    authors = []
    times = []

    for item in data:
        if 'text' in item:
            comments.append(item['text'])
            likes.append(item['likes'])
            authors.append(item['author'])
            times.append(isoparse(item['time']).strftime('%Y-%m-%d')) #PEGA TIMESTAMP E TRANSFORMA EM DATA

    df = pd.DataFrame({
        'comments': comments,
        'likes': likes,
        'authors': authors,
        'times': times
    })

    daily_likes = df.groupby('times')['likes'].sum().reset_index()

    print(df) #PRINT DO DATA FRAME

    plt.figure(figsize=(10, 6))
    plt.bar(daily_likes['times'], daily_likes['likes'])
    plt.xlabel('Time')
    plt.ylabel('Likes')
    plt.title('Likes over time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('likes_over_time.png')
    plt.close()

    total_comments = data[0]['total_comments']
    total_likes = data[0]['total_likes']

    plt.figure(figsize=(6, 6))
    plt.bar(['Comments', 'Likes'], [total_comments, total_likes])
    plt.title('Total comments and likes')
    plt.savefig('total_comments_likes.png')
    plt.close()

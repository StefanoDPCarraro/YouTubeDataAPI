'''
    Possiveis informações adicionais que podem ser coletadas:

    Data de publicação: A data em que o comentário foi publicado.
    Número de curtidas: O número de curtidas recebidas pelo comentário.
    Número de respostas: O número de respostas que o comentário recebeu.
    ID do comentário: O identificador único do comentário.
    ID do vídeo: O identificador único do vídeo ao qual o comentário está associado.
    ID do canal: O identificador único do canal do autor do comentário.
    ID da resposta: O identificador único da resposta, se o comentário for uma resposta a outro comentário.
    Contagem de palavras: O número de palavras no comentário.
    Contagem de caracteres: O número de caracteres no comentário.
    Classificação de spam: Uma pontuação indicando a probabilidade de o comentário ser spam.
'''

import json
import time
import requests
from ai import evaluate_sentiment
import json_parser
from config import API_KEY;

def get_comments(nome, ID):

    VideoID = ID

    params = {
        'key': API_KEY,
        'part': 'snippet', #PODE SER ALTERADO PARA MOSTRAR MAIS DO QUE APENAS O COMENTÁRIO (REPLIES, AUTORES, ETC)
        'videoId': VideoID,
        'order': 'time', #PODE SER ALTERADO PARA MOSTRAR OS COMENTÁRIOS DE OUTRAS FORMAS (RATING, RELEVANCE)
        'textFormat': 'plainText',
        'maxResults': 20 #QUANTIDADE DE COMENTÁRIOS QUE SERÃO MOSTRADOS, QUANTO MAIS MELHOR(GASTA MENOS REQUESTS)
    }

    #URL PARA REQUISIÇÃO
    url = 'https://www.googleapis.com/youtube/v3/commentThreads'
    jsonData = []
    total_comments_likes = 0
    total_comments = 0

    #LOOP PARA PEGAR TODOS OS COMENTÁRIOS
    while True:
        try:
            #CRIA UM JSON COM OS COMENTÁRIOS
            response = requests.get(url, params=params)
            data = response.json()

            #SE HOUVER COMENTÁRIOS, DA APPEND NO JSON DATA
            if 'items' in data: 
                comments = data['items']
                for comment in comments:
                    top_level_comment = comment['snippet']['topLevelComment']['snippet']
                    author =  top_level_comment['authorDisplayName']
                    text = top_level_comment['textDisplay']
                    like_count = top_level_comment.get('likeCount', 0)
                    published_at = top_level_comment['publishedAt']
                    total_reply_count = comment['snippet']['totalReplyCount']
                    total_comments_likes += like_count
                    #moderation_status = top_level_comment.get('moderationStatus') MOST ARE NULL
                    #comment_Id = comment['snippet']['topLevelComment']['id'] USELESS
                    print('Comment by', remove_emoji(author), ':', remove_emoji(text))
                    print('Likes:', like_count)
                    print('Published At:', published_at)
                    print('Total reply count:', total_reply_count)
                    #print('Moderation Status:', moderation_status)
                    #print('Comment ID:', comment_Id) USELESS
                    print()

                    jsonData.append({'text': remove_emoji(text), 'author': remove_emoji(author), 'likes': like_count, 'time': published_at, 'total_reply_count': total_reply_count})
                comment_size = len(comments)
                total_comments += comment_size

            #SE HOUVER MAIS PÁGINAS DE COMENTÁRIOS, PEGA A PRÓXIMA
            if 'nextPageToken' in data: 
                params['pageToken'] = data['nextPageToken']

            #SE NÃO HOUVER MAIS PÁGINAS, SALVA O JSON EM UM ARQUIVO
            else:
                video_data = {
                'total_comments': total_comments,
                'total_likes': total_comments_likes
                }
                jsonData.insert(0, video_data)

                with open(nome+'outputComments.json', 'w', encoding='utf-8') as jsonFile:
                    print('Total comments: ', total_comments)
                    print('Total comments likes: ', total_comments_likes)
                    json.dump(jsonData, jsonFile, indent=2, ensure_ascii=False)
                print('Comments saved in '+nome+' outputComments.json')
                break
            
            #ESPERA 5 SEGUNDOS PARA NÃO SOBRECARREGAR O SERVIDOR
            time.sleep(5)
        except Exception as e:
            print(e)


def remove_emoji(text):
    new_text = ''.join(char if ord(char) < 256 else '' for char in text)
    if new_text != None:
        return fix_encoding(new_text)
    return ''

def fix_encoding(text):
    return text.encode('latin-1', 'ignore').decode('latin-1')



if __name__ == '__main__':
    video_name = 'Video1' #NOME DO ARQUIVO QUE SERÁ ANALISADO
    get_comments(video_name, 'aGOe24sUYS4') #ID DO VÍDEO QUE SERÁ ANALISADO
    json_parser.plot_comments(video_name + 'outputComments.json')
    sentiment_dict = evaluate_sentiment(video_name + 'outputComments.json')
    json.dump(sentiment_dict, open(video_name + 'outputSentiments.json', 'w'), indent=2, ensure_ascii=False)
from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt, mpld3
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import json
from io import BytesIO
import base64

def wordCloud(data_path, room_type_category):
    df = pd.read_json(data_path)
    values = {'review_count':0, 'listing_name': ' '}
    df = df.fillna(value=values)

    df['months'].replace(0, 1, inplace=True)

    df['reviews_per_month'] = df.reviews_count / df.months

    km = KMeans(
        n_clusters=3, init='random',
        n_init=10, max_iter=300,
        tol=1e-04, random_state=0
    )

    df_reviews = df[df['room_type_category'] == room_type_category].reviews_per_month
    list_reviews = df_reviews.to_list()
    np_reviews = np.array(list_reviews)
    np_reviews = np_reviews.reshape(-1, 1)
    label = km.fit_predict(np_reviews)
    df_label = pd.DataFrame(label)
    df_label.columns = ['label']

    count = []
    for i in range(3):
        count.append(np_reviews[label == i].max())
    max_label = count.index(max(count))

    reviews = df[df['room_type_category'] == room_type_category].loc[:,
              ['listing_name', 'reviews_per_month']].reset_index(drop=True)
    res = pd.concat([df_label, reviews], axis=1)
    res_max = res[res['label'] == max_label]

    text_list = res_max.listing_name.to_list()
    text = ' '.join(text_list)

    stopwords = set(STOPWORDS)
    stopwords.update(['Apt', 'Room', 'Apartment', 'Private', 'Bedroom', 'manhattan', 'brooklyn', 'NYC',
                      'cozy', 'studio', 'Williamsburg', 'Bedford-Stuyvesant', 'Harlem', 'Bushwick', 'Upper West Side',
                      'Hell\'s Kitchen', 'East Village', 'Upper East Side', 'Crown Heights', 'Midtown'])
    wordcloud = WordCloud(max_font_size=50, stopwords=stopwords, max_words=1000, background_color="white").generate(
        text)
    fig = plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    '''
    sio = BytesIO()
    plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
    data = base64.encodebytes(sio.getvalue()).decode()
    src = 'data:image/png;base64,' + str(data)
    return src
    '''
    html = mpld3.fig_to_html(fig)
    return html


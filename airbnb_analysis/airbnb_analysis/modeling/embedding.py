import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import gensim.downloader as api
from sklearn.decomposition import PCA


stop_words = stopwords.words('english')



def name2Vec(name):
    # data_path = os.path.join(BASE_DIR, "static"),
    name_vectors2 = np.load("./airbnb_analysis/modeling/name_vectors.npy")
    tokens = word_tokenize(name)  # split into words
    words = [word for word in tokens if word.isalpha()]  # remove punctuation or special characters
    words = [w for w in words if not w in stop_words]  # remove stopwords
    word_vectors = api.load("glove-wiki-gigaword-100")
    vector_list = [word_vectors[word] for word in words if word in word_vectors.vocab]
    if len(vector_list) > 1:
        name_vector = np.mean(vector_list, axis=0)
    if len(vector_list) == 1:
        name_vector = vector_list[0]
    if len(vector_list) == 0:
        name_vector = np.array([0] * 100)
    name_vectors = np.concatenate((name_vectors2, np.array([name_vector])), axis=0)
    pca = PCA(n_components=15, random_state=10)
    reduced_vec = pca.fit_transform(name_vectors)
    return reduced_vec[-1]
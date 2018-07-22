import pandas as pd
import os
from surprise import SVD, Dataset, KNNBasic, Reader, accuracy
from surprise.model_selection import cross_validate, PredefinedKFold




item_stream = open('data/ml-100k/u.item', 'r')
date_item = item_stream.read().split('\n')
date_item = list(map(lambda case: case.split('\t')[:2], date_item))
item_stream.close()

data_stream = open('data/ml-100k/u.base', 'r')
data_base = data_stream.read().split('\n')
data_base = list(map(lambda case: case.split('\t')[:2], data_base))
data_base = data_base[: len(data_base) -1]
data_stream.close()



user_id , movie_id = zip(*date_item)
user_set = set(user_id) 
movie_set = set(movie_id)

database = pd.DataFrame({'user_id': user_id, 'movie_id': movie_id})
not_wash = {user: movie_set.difference(database.query('user_id == %s' %(user)).movie_id) for user in user_set}

files_dir = os.path.expanduser('data/ml-100k/')

data =  Reader('data/ml-100k')

train_file = files_dir + 'u%d.base'
test_file = files_dir + 'u%d.test'
folds_file = [(train_file % i, test_file % i) for i in [1]]


date = Dataset.load_from_file(folds_file, reader =data)
pkf = PredefinedKFold()

sim_opt = {
    'name' : 'cosine',
    'user_band' : True
}

algo = KNNBasic(sim_options=sim_opt, k = 4, min_k= 2)

for trainset, testset in pkf.split(date):
    algo.fit(trainset)

def get_top_5(u_id):
    top_5 = []
    movies = not_wash[u_id]

    for movie in movies:
        top_5.append((movie,algo.predict(uid=u_id,iid=movie).est))

    return sorted(top_5,key = lambda movie: movie[1], reverse = True)[:5]

def get_top_5_movies(uid):
    top5 = get_top_5(uid)
    return [date_item[int(movie[0])][1] for movie in top5]

import pandas as pd
import os
from surprise import Dataset, KNNBasic, Reader, accuracy, SVD
from surprise.model_selection import cross_validate, PredefinedKFold

__all__ = ['get_top_5_movies_KNN', 'user_set', 'get_top_5_movies_SVD', 'get_top_5_neighbors']

items_stream = open('ml-100k/u.item', 'r')
item_data = items_stream.read().split('\n')
item_data = list(map(lambda item: item.split('|')[:2], item_data))
items_stream.close()

database = pd.read_csv('ml-100k/u1.base.csv')
user_set = set(database.user_id)
item_set = set(database.item_id)
not_watch = {user: item_set.difference(database.query('user_id == %s' %(user)).item_id) for user in user_set}

# path to dataset folder
files_dir = os.path.expanduser('ml-100k/')

# This time, we'll use the built-in reader.
reader = Reader('ml-100k')

# folds_files is a list of tuples containing file paths:
# [(u1.base, u1.test), (u2.base, u2.test), ... (u5.base, u5.test)]
train_file = files_dir + 'u%d.base'
test_file = files_dir + 'u%d.test'
folds_files = [(train_file % i, test_file % i) for i in [1]]

data = Dataset.load_from_folds(folds_files, reader=reader)
pkf = PredefinedKFold()

sim_options = {
    'name': 'cosine',
    'user_based': True  # compute  similarities between items
}

algo = KNNBasic(sim_options=sim_options, k=4, min_k=2)
algo_svd = SVD()
for trainset, testset in pkf.split(data):

    # train and test algorithm.
    algo.fit(trainset)
    algo_svd.fit(trainset)



def get_top_5(uid):
    top = []
    items = not_watch[int(uid)]
    
    for item in items:
        top.append((item, algo.predict(uid=uid, iid=str(item)).est))
    
    return sorted(top, key=lambda item: item[1], reverse=True)[:5]


def get_top_5_movies_KNN(uid):
    top_5 = get_top_5(uid)
    return [item_data[int(item[0])][1] for item in top_5]


def get_top2_5(uid):
    top = []
    items = not_watch[int(uid)]
    
    for item in items:
        top.append((item, algo_svd.predict(uid=uid, iid=str(item)).est))
    
    return sorted(top, key=lambda item: item[1], reverse=True)[:5]


def get_top_5_movies_SVD(uid):
    top_5 = get_top2_5(uid)
    return [item_data[int(item[0])][1] for item in top_5]


def get_top_5_neighbors(uid):
    inner_uid = algo.trainset.to_inner_uid(uid)
    neighbords = algo.get_neighbors(iid=inner_uid, k=5)
    return [algo.trainset.to_raw_uid(iid) for iid in neighbords]
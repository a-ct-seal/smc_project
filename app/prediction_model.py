import pandas as pd
import random


def _flatten(lst):
    return [x for xs in lst for x in xs]


class PredictionModel:
    def __init__(self, knn_model, transformed_data, initial_data):
        self.knn_model = knn_model
        self.transformed_data = transformed_data
        self.initial_data = initial_data

    def get_prediction(self, list_ID, gen_size=60, recommend_size=20):  # todo fix warning
        list_track = self.transformed_data.iloc[list_ID]
        neighbors = self.knn_model.kneighbors(list_track, return_distance=False, n_neighbors=gen_size)
        indexes = list(set(_flatten(list(map(list, neighbors)))))
        chosen_indexes = random.choices(indexes, k=recommend_size)
        res = pd.DataFrame(self.initial_data.iloc[chosen_indexes])[['artist_name', 'track_name']].values.tolist()
        return [(chosen_indexes[idx], res[idx][0] + ', ' + res[idx][1]) for idx in range(len(res))]

    def get_random_recommendation(self, size):  # todo rewrite
        return list(range(size))

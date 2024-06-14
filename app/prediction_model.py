import pandas as pd
import random
import warnings

warnings.filterwarnings(action="ignore", category=UserWarning)


def _flatten(lst):
    return [x for xs in lst for x in xs]


class PredictionModel:
    def __init__(self, knn_model, transformed_data, initial_data):
        self.knn_model = knn_model
        self.transformed_data = transformed_data
        self.initial_data = initial_data

    def get_prediction(self, list_ID, gen_size=60, recommend_size=20):
        if len(list_ID) == 0:
            base_list = self.get_random_recommendation()
        else:
            base_list = list_ID

        list_track = self.transformed_data.iloc[base_list]
        neighbors = self.knn_model.kneighbors(list_track, return_distance=False, n_neighbors=gen_size)
        indexes = list(set(_flatten(list(map(list, neighbors)))))
        chosen_indexes = random.sample(population=indexes, k=recommend_size)
        res = self.get_tracks_by_ids(chosen_indexes)
        return list(zip(chosen_indexes, res))

    def get_random_recommendation(self, size=100):
        return random.sample(population=range(len(self.initial_data)), k=size)

    def get_tracks_by_ids(self, list_ID):
        res = pd.DataFrame(self.initial_data.iloc[list_ID])[['artist_name', 'track_name']].values.tolist()
        return [track[0] + ' - ' + track[1] for track in res]

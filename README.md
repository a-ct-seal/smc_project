# SMC_project
Repository for final project on Social Media Computing course

# Recommendation model
We use music from [this dataset](https://www.kaggle.com/datasets/saurabhshahane/music-dataset-1950-to-2019).

For text preprocessing [google universal sentence encoder](https://www.kaggle.com/models/google/universal-sentence-encoder) is used.
It is a model that encodes text into 512-dimensional vectors that can be used for different natural language tasks.

For recommendation itself, some tracks that user liked are stored, and KNN-based model recommend similar ones.
Because of big number of features, we use KNN, that is based on ball trees (see [docs](https://scikit-learn.org/stable/modules/neighbors.html#nearest-neighbor-algorithms:~:text=using%20nearest%20neighbors.-,1.6.4.%20Nearest%20Neighbor%20Algorithms,-%23) for more info).

There is a simple web application in "app" folder, based on [flask framework](https://flask.palletsprojects.com/en/3.0.x/).
For local run you need to first initialize a user database by running `init.sh` script.
After that application can be run on localhost by command `flask run`.

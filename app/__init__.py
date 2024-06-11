import pandas as pd
import pickle

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from app.prediction_model import PredictionModel


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

knn_model = pickle.load(open('knn.txt', 'rb'))
transformed_data = pd.read_csv('transformed_data.csv')
initial_data = pd.read_csv('tcc_ceds_music.csv')
prediction_model = PredictionModel(knn_model, transformed_data, initial_data)

from app import routes, models

import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db, login, prediction_model
from typing import Optional
from sqlalchemy.ext.mutable import MutableList
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


MAX_LIKED_TRACKS_SIZE = 100  # todo change to 1000


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(256), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    liked_tracks_ids: so.Mapped[list[int]] = (
        so.mapped_column(MutableList.as_mutable(sa.PickleType),
                         default=prediction_model.get_random_recommendation(size=MAX_LIKED_TRACKS_SIZE // 4)))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_liked_tracks(self, new_liked_tracks):  # todo add uninitialized state
        self.liked_tracks_ids.extend(new_liked_tracks)
        if len(self.liked_tracks_ids) > MAX_LIKED_TRACKS_SIZE:
            self.liked_tracks_ids = self.liked_tracks_ids[len(self.liked_tracks_ids) - MAX_LIKED_TRACKS_SIZE:]


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

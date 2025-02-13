from . import db
from flask_login import UserMixin
from datetime import datetime


followers = db.Table(
    "followers",
    db.Column("follower_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("following_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    current_activity_id = db.Column(
        db.Integer, db.ForeignKey("activity.id"), nullable=True
    )
    current_activity = db.relationship(
        "Activity",
        uselist=False,
        backref="current_user",
        lazy=True,
        foreign_keys=[current_activity_id],
    )
    following = db.relationship(
        "User",
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.following_id == id),
        backref=db.backref("followers", lazy="dynamic"),
        lazy="dynamic",
    )

    def is_following(self, user):
        return self.following.filter(followers.c.following_id == user.id).count() > 0

    def is_followed_by(self, user):
        return self.followers.filter(followers.c.follower_id == user.id).count() > 0


class FriendRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    sender = db.relationship("User", foreign_keys=[sender_id], backref="sent_requests")
    receiver = db.relationship(
        "User", foreign_keys=[receiver_id], backref="received_requests"
    )


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(20), nullable=True)
    description = db.Column(db.Text, nullable=True)
    visibility = db.Column(db.String(20), nullable=False)
    is_goal = db.Column(db.String(20), nullable=False, default="False")
    timestamp = db.Column(db.DateTime, default=datetime.now)
    image_filename = db.Column(db.String(150), nullable=True)
    latitude = db.Column(db.String(50), nullable=True)
    longitude = db.Column(db.String(50), nullable=True)
    is_archived = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref="activities", foreign_keys=[user_id])


"""
    goal_status = db.Column(
        db.String(20), nullable=False, default="pending"
    )  # 'pending', 'success', 'failure'
"""

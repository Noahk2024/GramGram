from app import db
db.create_all()

class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(50), nullable=True)
    bio = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    image = db.Column(db.LargeBinary, nullable=True)
    age = db.Column(db.String(3), nullable=True)
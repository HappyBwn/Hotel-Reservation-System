import random
import sys
from faker import Faker
from flask import Flask
from datetime import datetime
# from bootstrap_table import db, User

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Admin/Desktop/HoanNguyen-Reservation-System-main/HoanNguyen-Reservation-System-main/db.sqlite'
db = SQLAlchemy(app)
f = Faker()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ten = db.Column(db.String(64), index=True)
    sdt = db.Column(db.String(20))
    loai = db.Column(db.String(20))
    diachi = db.Column(db.String(256))
    cccd = db.Column(db.String(20))
    ghichu = db.Column(db.String(256))
    khuphong = db.Column(db.String(20))
    sophong = db.Column(db.Integer, index=True) 
    giaphong = db.Column(db.Integer, index=True)
    ngayden = db.Column(db.DateTime, nullable=False)
    ngaydi = db.Column(db.DateTime, nullable=True)
    
def create_fake_users(n):
    """Generate fake users."""
    faker = Faker()
    with app.app_context():
        db.create_all()
        for i in range(n):
            user = User(ten=faker.name(),
                        sdt=faker.phone_number(),
                        loai=faker.name(),
                        diachi=faker.address().replace('\n', ', '),
                        cccd=random.randint(2161515200, 2161515500),
                        ghichu=faker.md5(),
                        khuphong=faker.tld(),
                        sophong=random.randint(1, 30),
                        giaphong=random.randint(10, 30) * 1000,
                        ngayden=faker.date_time(),
                        ngaydi=faker.date_time())
            db.session.add(user)
        db.session.commit()
        print(f'Added {n} fake users to the database.')


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Pass the number of users you want to create as an argument.')
        sys.exit(1)
    create_fake_users(int(sys.argv[1]))

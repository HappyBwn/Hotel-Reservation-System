import random
import sys
from faker import Faker
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from flask import jsonify

from flask import Flask, request
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Admin/Desktop/HoanNguyen-Reservation-System-main/HoanNguyen-Reservation-System-main/db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
cors = CORS(app, resources={r"/checkin": {"origins": "*"}})
cors = CORS(app, resources={r"/checkout": {"origins": "*"}})


with app.app_context():
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

        def to_dict(self):
            return {
                'ten': self.name,
                'sdt': self.name,
                'loai': self.name,
                'diachi': self.name,
                'cccd': self.name,
                'ghichu': self.name,
                'khuphong': self.name,
                'sophong': self.name,
                'giaphong': self.name,
                'ngayden': self.name,
                'ngaydi': self.name
            }

    db.create_all()
    def create_fake_users():
        """Generate fake dns record."""
        faker = Faker()
    #    user = User(name=faker.name(),
    #                age=random.randint(20, 80),
    #                address=faker.address().replace('\n', ', '),
    #                phone=faker.phone_number(),
    #                email=faker.email())
    ####### Change to DNS Record
        user = User(ten=data['ten'],
                    sdt=data['sdt'],loai=data['loai'],diachi=data['diachi'],cccd=data['cccd'],ghichu=data['ghichu'],khuphong=data['khuphong'],sophong=data['sophong'],giaphong=data['giaphong'],ngayden=data['ngayden'],ngaydi=data['ngaydi'])
        db.session.add(user)
        db.session.commit()
        print(f'Added fake users to the database.')
    #if __name__ == '__main__':
    #    create_fake_users()

    @app.route('/checkin', methods = ['POST'])
    def sample():
    #        print(data['time'])
    #        print(data['record'])
        if request.method == 'POST':
            data = request.json
    #        print("POST'd", request.json)
    #        people = create_fake_users()
            checkin = datetime.strptime(data['ngayden'], '%d-%m-%Y')
            checkout = datetime.strptime(data['ngaydi'], '%d-%m-%Y')
            existing_reservations = User.query.filter(
                (User.sophong == data['sophong']) &
                (User.ngayden < checkout) &
                (User.ngaydi > checkin)
            ).all()
            if len(existing_reservations) > 0:
                return jsonify({'error': 'Time conflict with existing reservation(s)'}), 409
            else:
                user = User(ten=data['ten'],
                        sdt=data['sdt'],loai=data['loai'],diachi=data['diachi'],cccd=data['cccd'],ghichu=data['ghichu'],khuphong=data['khuphong'],sophong=data['sophong'],giaphong=data['giaphong'],ngayden=checkin,ngaydi=checkout)
                db.session.add(user)
                db.session.commit()
    #    return "handled"
        return "handled"
    @app.route('/checkout', methods=['POST'])
    def delete_record():
        if request.method == 'POST':
            data = request.json
            # checkin = datetime.strptime(data['ngayden'], '%Y-%m-%d %H:%M:%S')
            # checkout = datetime.strptime(data['ngaydi'], '%Y-%m-%d %H:%M:%S')            
            # user = User(ten=data['ten'],
                    # sdt=data['sdt'],loai=data['loai'],diachi=data['diachi'],cccd=data['cccd'],ghichu=data['ghichu'],khuphong=data['khuphong'],sophong=data['sophong'],giaphong=data['giaphong'],ngayden=checkin,ngaydi=checkout)
            record_to_delete = User.query.filter_by(sdt=data['sdtcheckout']).first()                    
            if record_to_delete:
                db.session.delete(record_to_delete)
                db.session.commit()
                return 'Record deleted successfully'
            else:
                return jsonify({'error': 'SDT not existing reservation(s)'}), 409      
    if __name__ == '__main__':
        app.run(host='0.0.0.0', use_reloader=False, debug=True, port=5050)

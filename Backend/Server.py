import os
from flask import send_from_directory
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Admin/Desktop/HoanNguyen-Reservation-System-main/HoanNguyen-Reservation-System-main/db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
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
                'ten': self.ten,
                'sdt': self.sdt,
                'loai': self.loai,
                'diachi': self.diachi,
                'cccd': self.cccd,
                'ghichu': self.ghichu,
                'khuphong': self.khuphong,
                'sophong': self.sophong,
                'giaphong': self.giaphong,
                'ngayden': self.ngayden,
                'ngaydi': self.ngaydi
            }

    db.create_all()

    @app.route('/')
    def index():
        return render_template('server_table.html', title='System Reservation Table')

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'templates'),
                              'favicon.ico',mimetype='image/vnd.microsoft.icon')

    @app.route('/api/data')
    def data():
        query = User.query

        # search filter
        search = request.args.get('search[value]')
        if search:
            query = query.filter(db.or_(
                User.ten.like(f'%{search}%'),
                User.loai.like(f'%{search}%'),
                User.khuphong.like(f'%{search}%'),
                User.sophong.like(f'%{search}%')
            ))
        total_filtered = query.count()

        # sorting
        order = []
        i = 0
        while True:
            col_index = request.args.get(f'order[{i}][column]')
            if col_index is None:
                break
            col_name = request.args.get(f'columns[{col_index}][data]')
            if col_name not in ['ten', 'sophong', 'giaphong']:
                col_name = 'ten'
            descending = request.args.get(f'order[{i}][dir]') == 'desc'
            col = getattr(User, col_name)
            if descending:
                col = col.desc()
            order.append(col)
            i += 1
        if order:
            query = query.order_by(*order)

        # pagination
        start = request.args.get('start', type=int)
        length = request.args.get('length', type=int)
        query = query.offset(start).limit(length)

        # response
        return {
            'data': [user.to_dict() for user in query],
            'recordsFiltered': total_filtered,
            'recordsTotal': User.query.count(),
            'draw': request.args.get('draw', type=int),
        }


    if __name__ == '__main__':
    #    app.run()
        app.run(host='0.0.0.0', use_reloader=False, debug=True, port=8080)

from flask import Flask, render_template, flash, request, Response
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import pymysql, time, cv2, os, datetime




app = Flask(__name__)


app.config['SECRET_KEY'] = '123123'

CAPTURES_DIR = os.path.join('static', 'captures')
if not os.path.exists(CAPTURES_DIR):
    os.makedirs(CAPTURES_DIR)

fourcc = cv2.VideoWriter_fourcc(*'XVID')



def video_stream():
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    capture_interval =  1800 # 캡쳐 간격 (초)
    last_capture_time = time.time()
    while True:
        # 매 초마다 스트리밍을 수행
        ret, frame = cam.read()
        if not ret:
            break
        
        # 캡쳐 간격이 되면 프레임을 저장
        if time.time() - last_capture_time >= capture_interval:
            last_capture_time = time.time()
            _, jpeg = cv2.imencode('.jpg', frame)
            now = datetime.datetime.now()
            filename = now.strftime('%Y%m%d_%H%M%S.jpg')
            filepath = os.path.join(CAPTURES_DIR, filename)
            with open(filepath, 'wb') as f:
                f.write(jpeg.tobytes())
        
        # 이미지 스트리밍
        _, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')




@app.route('/video')
def video():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/live')
def live():
    flash('you can watch live plant')
    return render_template("live.html")


@app.route('/data')
def data():
    flash('목록을 눌러 데이터를 확인하실 수 있습니다!')
    return render_template('data.html')

@app.route('/data1')
def data1():
    conn = pymysql.connect(user='root', 
                        passwd='1234', 
                        host='localhost', 
                        db='test', 
                        charset='utf8')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM temperature")
    data_list = cursor.fetchall()
    conn.close()
    return render_template('data1.html',data_list=data_list)

@app.route('/data2')
def data2():
    conn = pymysql.connect(user='root', 
                        passwd='1234', 
                        host='localhost', 
                        db='test', 
                        charset='utf8')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM humidity")
    data_list = cursor.fetchall()
    conn.close()
    return render_template('data2.html',data_list=data_list)

@app.route('/data3')
def data3():
    conn = pymysql.connect(user='root', 
                        passwd='1234', 
                        host='localhost', 
                        db='test', 
                        charset='utf8')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM soil")
    data_list = cursor.fetchall()
    conn.close()
    return render_template('data3.html',data_list=data_list)

@app.route('/reset1')
def reset1():
    conn = pymysql.connect(user='root', 
                            passwd='1234', 
                            host='localhost', 
                            db='test', 
                            charset='utf8')
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE temperature")
    conn.commit()
    data_list = cursor.fetchall()
    conn.close()
    return render_template('data1.html',data_list=data_list)
    
@app.route('/reset2')
def reset2():
    conn = pymysql.connect(user='root', 
                            passwd='1234', 
                            host='localhost', 
                            db='test', 
                            charset='utf8')
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE humidity")
    conn.commit()
    data_list = cursor.fetchall()
    conn.close()
    return render_template('data2.html',data_list=data_list)
    
@app.route('/reset3')
def reset3():
    conn = pymysql.connect(user='root', 
                            passwd='1234', 
                            host='localhost', 
                            db='test', 
                            charset='utf8')
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE soil")
    conn.commit()
    data_list = cursor.fetchall()
    conn.close()
    return render_template('data3.html',data_list=data_list)
    
# db = SQLAlchemy(app)

# class Users(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     email = db.Column(db.String(200), nullable=False, unique=True)
#     date_added = db.Column(db.DateTime, default=datetime.utcnow)


    # def __repr__(self):
    #     return '<Name %r>' % self.name

# ''' 필터 종류 
# safe (효과 적용)
# capitalize (맨 앞글자만 대문자)
# lower
# upper
# title (앞글자 대문자)
# trim (뒤 공백 제거)
# striptags (효과 제거)
# '''

class NamerForm(FlaskForm):
    name = StringField("what's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("success")

    return render_template("index.html", name = name, form = form)



@app.route('/Credit')
def credit():
    flash('Our history')
    return render_template("credit.html")





@app.errorhandler(404)
def handle_404(er):
    return render_template('404.html'), 404

@app.errorhandler(500)
def handle_500(er):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2504, debug=True)

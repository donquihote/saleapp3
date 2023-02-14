from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary



app= Flask(__name__)

app.secret_key = 'lephibien1982vothithuhien1989'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:phibien1982@localhost/labsaledb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 8
app.config['COMMENT-SIZE'] = 20
db = SQLAlchemy(app=app)


cloudinary.config(
    cloud_name ='dejlhncgu',
    api_key = '445548396235361',
    api_secret ='EJWOBrnMiEsHevPzvqjc0sv4fns',
)

login=LoginManager(app=app)
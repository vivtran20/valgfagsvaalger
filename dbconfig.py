from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from scrape import * 

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:hej123@localhost:5432/valgfagsvælgeren_db'
db.init_app(app)

class f2023(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    code=db.Column(db.String(), nullable=False)
    title=db.Column(db.String(), nullable=False)
    ects=db.Column(db.Float, nullable=False)
    termin=db.Column(db.String(), nullable=False)
    indgangskrav=db.Column(db.String(), nullable=True)
    eksamen=db.Column(db.String(), nullable=False)


with app.app_context():
    db.create_all()


x = getCourseCodes("f2023")
i = 0
for course in x:
    y = getPageContent(course)
    entry = f2023(id=i, code=course, title=title(y), ects=ects(y), termin=termin(y), indgangskrav=indgangskrav(y), eksamen= eksamen(y))
    with app.app_context():
        db.session.add(entry)
        db.session.commit()
    i = i + 1
#entry = Courses(id="dm571", title="software engineering", ects=10, termin="efterår", indgangskrav="ingen", eksamen= "mundtlig eksamen")
#with app.app_context():
    #db.session.add(entry)
    #db.session.commit()
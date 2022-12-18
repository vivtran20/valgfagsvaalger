from flask import Flask, redirect, url_for, render_template, request
import psycopg2

app = Flask(__name__)
try:
    conn = psycopg2.connect(
        database="valgfagsvælgeren_db",
        user="postgres",
        password="hej123",
        host="localhost")
    print("connected")
except:
    print("I am unable to connect to the database")

mycursor = conn.cursor()


@app.route("/", methods=['post','get'])
def database():
    if request.method == "POST":
        if request.form.get('termin') == 'f2023':
            ects = request.form.get('ects')
            eksamen = request.form.get('eksamen')
            mycursor.execute("SELECT title, ects, eksamen FROM f2023 WHERE ects=%(some_ects)s AND eksamen=%(some_eksamen)s",
            {"some_ects": ects, "some_eksamen": eksamen})
            data = mycursor.fetchall()
            return render_template("search.html", data=data)
        elif request.form.get('termin') == 'e2023':
            ects = request.form.get('ects')
            eksamen = request.form.get('eksamen')
            mycursor.execute("SELECT title, ects, eksamen FROM e2023 WHERE ects=%(some_ects)s AND eksamen=%(some_eksamen)s",
            {"some_ects": ects, "some_eksamen": eksamen})
            data = mycursor.fetchall()
            return render_template("search.html", data=data)
        elif request.form.get('termin') == 'f2022':
            ects = request.form.get('ects')
            eksamen = request.form.get('eksamen')
            mycursor.execute("SELECT title, ects, eksamen FROM f2022 WHERE ects=%(some_ects)s AND eksamen=%(some_eksamen)s",
            {"some_ects": ects, "some_eksamen": eksamen})
            data = mycursor.fetchall()
            return render_template("search.html", data=data)
        elif request.form.get('termin') == 'e2022':
            ects = request.form.get('ects')
            eksamen = request.form.get('eksamen')
            mycursor.execute("SELECT title, ects, eksamen FROM e2022 WHERE ects=%(some_ects)s AND eksamen=%(some_eksamen)s",
            {"some_ects": ects, "some_eksamen": eksamen})
            data = mycursor.fetchall()
            return render_template("search.html", data=data)

    else:
        return render_template("search.html")

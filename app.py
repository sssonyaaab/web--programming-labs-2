from flask import Flask, redirect, request, url_for, render_template
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3

app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)

@app.route("/")


@app.route("/index")
def start():
    return redirect ("/menu", code=302)


@app.route("/menu")
def menu():
    return """
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>

        <p><a href="http://127.0.0.1:5000/lab1">Первая лабораторная</a></p>
        <p><a href="http://127.0.0.1:5000/lab2/">Вторая лабораторная</a></p>
        <p><a href="http://127.0.0.1:5000/lab3/">Третья лабораторная</a></p>

        <footer>
            &copy; Софья Баранова, ФБИ-24, 3 курс, 2024
        </footer>
    </body>
</html>
"""

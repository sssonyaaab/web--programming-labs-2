from flask import Flask, redirect, request, url_for, render_template
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from rgz import rgz
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(rgz)

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

        <p><a href="/lab1">Первая лабораторная</a></p>
        <p><a href="/lab2/">Вторая лабораторная</a></p>
        <p><a href="/lab3/">Третья лабораторная</a></p>
        <p><a href="/lab4/">Четвертая лабораторная</a></p>
        <p><a href="/lab5/">Пятая лабораторная</a></p>
        <p><a href="/lab6/">Шестая лабораторная</a></p>
        <p><a href="/lab7/">Седьмая лабораторная</a></p>
        <p><a href="/rgz">Расчетно-графическое задание</a></p>

        <footer>
            &copy; Софья Баранова, ФБИ-24, 3 курс, 2024
        </footer>
    </body>
</html>
"""

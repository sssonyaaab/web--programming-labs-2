from flask import Flask, redirect, url_for, render_template
app = Flask(__name__)

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

        <a href="http://127.0.0.1:5000/lab1">Первая лабораторная</a>

        <footer>
            &copy; Софья Баранова, ФБИ-24, 3 курс, 2024
        </footer>
    </body>
</html>
"""
@app.route("/lab1")
def lab1():
    return """
<!doctype html>
<html>
    <head>
        <title>Баранова Софья Сергеевна, Лабораторная 1</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, Лабораторная работа 1
        </header>

        <h1>web-сервер на flask</h1>

        Flask — фреймворк для создания веб-приложений на языке
        программирования Python, использующий набор инструментов
        Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
        называемых микрофреймворков — минималистичных каркасов
        веб-приложений, сознательно предоставляющих лишь самые базовые возможности.

        <a href="http://127.0.0.1:5000/menu">Меню</a>

        <h2>Реализованные роуты</h2>

        <ul>
            <li><a href="http://127.0.0.1:5000/lab1/oak">/lab1/oak-дуб</a></li>
            <li><a href="http://127.0.0.1:5000/lab1/student">/lab1/student-студент</a></li>
            <li><a href="http://127.0.0.1:5000/lab1/python">/lab1/python-python</a></li>
            <li><a href="http://127.0.0.1:5000/lab1/cinnabon">/lab1/cinnabon-cinnabon</a></li>
        </ul>

        <footer>
            &copy; Софья Баранова, ФБИ-24, 3 курс, 2024
        </footer>
    </body>
</html>
"""
@app.route('/lab1/oak')
def oak():
    return '''
<!doctype html>
<html>
    <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
    <body>
        <h1>Дуб</h1>
        <img src= "''' + url_for ('static', filename='oak.jpg') + '''" >
    </body>
</html>
'''
@app.route('/lab1/student')
def student():
    return '''
<!doctype html>
<html>
    <head>
        <title>Студент</title>
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <header>
            НГТУ, ФБ, Лабораторная работа 1
        </header>

        <h1>Информация о студенте</h1>

        <p>Фамилия: Баранова</p>
        <p>Имя: Софья</p>
        <p>Отчество: Сергеевна</p>

        <img src="''' + url_for('static', filename='nstu_logo.png') + '''" >

        <footer>
            &copy; Софья Баранова, ФБИ-24, 3 курс, 2024
        </footer>
    </body>
</html>
'''
@app.route('/lab1/python')
def python():
    return '''
<!doctype html>
<html>
    <head>
        <title>Python</title>
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <header>
            НГТУ, ФБ, Лабораторная работа 1
        </header>

        <h1>О языке Python</h1>

        <p>Python – это высокоуровневый язык программирования, который был разработан в конце 1980-х годов. 
        Его разработчик, Гвидо ван Россум, вложил в основу языка простоту и читабельность кода, что позволяет использовать Python для быстрой и эффективной разработки. 
        Много популярных веб-сайтов, компьютерных игр и программ, написанных на Python, вы используете ежедневно: Dropbox, Uber, Sims, Google, GIMP и другие.</p>
        <p>Язык отличается понятным синтаксисом, поэтому Python подходит для начинающих программистов. 
        Он широко используется во многих областях: веб-разработка, научные исследования, анализ данных, искусственный интеллект, машинное обучение, разработка игр. </p>
        <p>У Python большая библиотека сторонних модулей и инструментов, что делает его мощным инструментом. 
        Наличие активного сообщества разработчиков позволяет постоянно поддерживать и обновлять язык, 
        предоставлять достаточный объем обучающих материалов, документацию и форумы для программистов с любым уровнем знаний.</p>

        <img src="''' + url_for('static', filename='python.jpeg') + '''" >

        <footer>
            &copy; Софья Баранова, ФБИ-24, 3 курс, 2024
        </footer>
    </body>
</html>
'''
@app.route('/lab1/cinnabon')
def cinnabon():
    return '''
<!doctype html>
<html>
    <head>
        <title>Cinnabon</title>
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <header>
            НГТУ, ФБ, Лабораторная работа 1
        </header>

        <h1>Синнабон</h1>

        <p>Синнабон — всемирно известный бренд самых вкусных булочек с корицей! 
        Свежесть, аромат и аппетитный вид нашей выпечки вызывают неизменный восторг у людей всех возрастов в 50+ странах мира!</p>
        <p>Рецепт приготовления булочек «Синнабон» держится в строжайшем секрете, а над их созданием трудились лучшие кондитеры и технологи для того, 
        чтобы испечь самую вкусную булочку, нужно собрать уникальные ингредиенты со всего земного шара.</p>
        <p>Самая ароматная корица сорта «Макара» выращивается специально для «Синнабон» высоко в горах Индонезии. 
        Нашу корицу тщательно готовят с помощью специального процесса помола при определенной температуре, 
        это позволяет сохранить драгоценные эфирные масла и усилить сладкий аромат и вкус.</p>

        <img src="''' + url_for('static', filename='cinnabon.png') + '''" >

        <footer>
            &copy; Софья Баранова, ФБИ-24, 3 курс, 2024
        </footer>
    </body>
</html>
'''
@app.route('/lab2/a')
def a():
    return 'без слэша'
@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return "такого цветка нет", 404 
    else:
        return "цветок:" + flower_list[flower_id]

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок<h1>
    <p>Название нового цветка: {name} </p>
    <p>Всего цветов: {len(flower_list)}</p>
    <p>Полный список: {flower_list}</p>
    </body>
<html>
'''
@app.route('/lab2/example')
def example():
    name = 'Соня Баранова'
    lab_num = 2
    group = 'ФБИ-24'
    kurs = 3
    fruits = [
        {'name': 'яблоки', 'price': 100}, 
        {'name': 'груши', 'price': 120}, 
        {'name': 'апельсины', 'price': 80}, 
        {'name': 'мандарины', 'price': 95}, 
        {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html', name=name, lab_num=lab_num, 
                           group=group, kurs=kurs, fruits=fruits)
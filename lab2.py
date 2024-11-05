from flask import Blueprint, redirect, request, url_for, render_template
lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/a')
def a():
    return 'без слэша'


@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'


flower_list = [ {"name": "Роза", "price": 100},
    {"name": "Тюльпан", "price": 50},
    {"name": "Незабудка", "price": 70},
    {"name": "Ромашка", "price": 40}
]

@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return render_template('lab2/error.html', error_code=404, error_message="Такого цветка нет"), 404
    else:
        flower = flower_list[flower_id]
        return render_template('lab2/flower.html', flower=flower, flower_id=flower_id)


@lab2.route('/lab2/flowers')
def show_flowers():
    return render_template('lab2/flowers.html', flowers=flower_list, total=len(flower_list))


@lab2.route('/lab2/add_flower', methods=['POST'])
def add_flower():
    name = request.form.get('name')
    price = request.form.get('price')
    if not name or not price:
        return render_template('lab2/error.html', error_code=400, error_message="Вы не задали имя или цену цветка"), 400
    
    flower_list.append({"name": name, "price": int(price)})
    return redirect(url_for('lab2.show_flowers'))


@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return redirect(url_for('lab2.show_flowers'))


@lab2.route('/lab2/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id >= len(flower_list):
        return render_template('lab2/error.html', error_code=404, error_message="Такого цветка нет"), 404
    else:
        flower_list.pop(flower_id)
        return redirect(url_for('lab2.show_flowers'))


@lab2.route('/lab2/example')
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
    return render_template('lab2/example.html', name=name, lab_num=lab_num, 
                           group=group, kurs=kurs, fruits=fruits)


@lab2.route('/lab2/')
def lab():
    return render_template('lab2/lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('lab2/filter.html', phrase=phrase)


@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    sum_result = a + b
    diff_result = a - b
    prod_result = a * b
    if b != 0:
        div_result = a / b
    else:
        div_result = "Деление на 0 невозможно"
    pow_result = a ** b
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Расчеты с параметрами:</h1>
    <p>{a} + {b} = {sum_result}</p>
    <p>{a} - {b} = {diff_result}</p>
    <p>{a} * {b} = {prod_result}</p>
    <p>{a} / {b} = {div_result}</p>
    <p>{a}<sup>{b}</sup> = {pow_result}</p>
    </body>
</html>
'''


@lab2.route('/lab2/calc/')
def calc_():
    return redirect(url_for('calc', a=1, b=1))


@lab2.route('/lab2/calc/<int:a>')
def calc_one(b):
    return redirect(url_for('calc', a=a, b=1))


books = [
    {"author": "Джон Рональд Руэл Толкин", "title": "Хоббит", "genre": "Повесть", "pages": 256},
    {"author": "Михаил Булгаков", "title": "Мастер и Маргарита", "genre": "Роман", "pages": 480},
    {"author": "Джоан Роулинг", "title": "Гарри Поттер и философский камень", "genre": "Роман", "pages": 464},
    {"author": "Лев Толстой", "title": "Война и мир", "genre": "Роман", "pages": 1225},
    {"author": "Федор Достоевский", "title": "Преступление и наказание", "genre": "Роман", "pages": 671},
    {"author": "Дж. Р. Р. Толкин", "title": "Властелин колец", "genre": "Фэнтези", "pages": 1137},
    {"author": "Антуан де Сент-Экзюпери", "title": "Маленький принц", "genre": "Повесть-сказка", "pages": 112},
    {"author": "Мигель де Сервантес", "title": "Дон Кихот", "genre": "Роман", "pages": 1152},
    {"author": "Коллектив авторов", "title": "Библия", "genre": "Религиозная литература", "pages": 1520},
    {"author": "Рей Брэдбери", "title": "451 градус по Фаренгейту", "genre": "Научная фантастика", "pages": 249}
]

@lab2.route('/lab2/books')
def show_books():
    return render_template('lab2/books.html', books=books)


berries = [
    {"name": "Клубника", "description": "Ягоды обладают ярко выраженным красным цветом.", "image": "lab2/strawberry.jpeg"},
    {"name": "Малина", "description": "Плоды бывают красного, розового, желтого и черного цвета.", "image": "lab2/raspberry.webp"},
    {"name": "Голубика", "description": "Синевато-черная ягода, которую путают с черникой.", "image": "lab2/blueberry.jpeg"},
    {"name": "Ежевика", "description": "Сок плодов тёмно-красный, кислый со сладкими нотками.", "image": "lab2/blackberry.jpeg"},
    {"name": "Вишня", "description": "Темно-красная ягода с насыщенным вкусом и ароматом.", "image": "lab2/cherry.jpeg"}
]

@lab2.route('/lab2/berries')
def show_berries():
    return render_template('lab2/berries.html', berries=berries)
from flask import Blueprint, render_template, request, redirect, url_for, session

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/')
def main():
    return render_template('lab9/index.html')


@lab9.route('/lab9/name', methods=['GET', 'POST'])
def name():
    if request.method == 'POST':
        session['name'] = request.form.get('name')
        return redirect(url_for('lab9.age'))
    return render_template('lab9/name.html')


@lab9.route('/lab9/age', methods=['GET', 'POST'])
def age():
    if request.method == 'POST':
        session['age'] = request.form.get('age')
        return redirect(url_for('lab9.gender'))
    return render_template('lab9/age.html')


@lab9.route('/lab9/gender', methods=['GET', 'POST'])
def gender():
    if request.method == 'POST':
        session['gender'] = request.form.get('gender')
        return redirect(url_for('lab9.preference1'))
    return render_template('lab9/gender.html')


@lab9.route('/lab9/preference1', methods=['GET', 'POST'])
def preference1():
    if request.method == 'POST':
        session['preference1'] = request.form.get('preference1')
        return redirect(url_for('lab9.preference2'))
    return render_template('lab9/preference1.html')


@lab9.route('/lab9/preference2', methods=['GET', 'POST'])
def preference2():
    if request.method == 'POST':
        session['preference2'] = request.form.get('preference2')
        return redirect(url_for('lab9.result'))
    return render_template('lab9/preference2.html')


@lab9.route('/lab9/result')
def result():
    name = session.get('name')
    age = int(session.get('age'))
    gender = session.get('gender')
    preference1 = session.get('preference1')
    preference2 = session.get('preference2')

    if age < 18:
        if gender == 'male':
            greeting = f"Поздравляю тебя, {name}, желаю, чтобы ты быстро вырос, был умным и счастливым!"
        else:
            greeting = f"Поздравляю тебя, {name}, желаю, чтобы ты быстро выросла, была умной и счастливой!"
    else:
        if gender == 'male':
            greeting = f"Поздравляю тебя, {name}, желаю успехов, здоровья и счастья!"
        else:
            greeting = f"Поздравляю тебя, {name}, желаю успехов, здоровья и счастья!"

    if preference1 == 'tasty':
        if preference2 == 'sweet':
            image = 'lab9/candy.jpg'
            gift = "Вот тебе подарок — мешочек конфет!"
        else:
            image = 'lab9/dinner.webp'
            gift = "Вот тебе подарок — сытный ужин!"
    else:
        if preference2 == 'sweet':
            image = 'lab9/cake.png'
            gift = "Вот тебе подарок — красивый тортик!"
        else:
            image = 'lab9/images.jpeg'
            gift = "Вот тебе подарок — произведение искусства!"

    return render_template('lab9/result.html', greeting=greeting, image=image, gift=gift)
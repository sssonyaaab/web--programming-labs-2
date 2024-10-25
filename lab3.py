from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name', 'Аноним')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age', 'Неизвестный возраст')
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'

    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    # Пусть кофе стоит 120 рублей, черный чай - 80 рублей, зеленый - 70 рублей.
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80 
    else:
        price = 70
    
    # Добавка молока удорожает напиток на 30 рублей, а сахара - на 10.
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
    
    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    background = request.args.get('background')
    font_size = request.args.get('font_size')
    font_style = request.args.get('font_style')
    if color or background or font_size or font_style:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if background:
            resp.set_cookie('background', background)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if font_style:
            resp.set_cookie('font_style', font_style)
        return resp
    color = request.cookies.get('color')
    background = request.cookies.get('background')
    font_size = request.cookies.get('font_size')
    font_style = request.cookies.get('font_style')
    resp = make_response(render_template('lab3/settings.html', color=color, background=background, font_size=font_size, font_style=font_style))
    return resp


@lab3.route('/lab3/clear_cookies')
def clear_cookies():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('background_color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('text_style')
    return resp


@lab3.route('/lab3/ticket', methods=['GET', 'POST'])
def ticket():
    error_messages = {}
    if request.method == 'POST':
        name = request.form.get('name')
        bunk = request.form.get('bunk')
        with_bed = request.form.get('with_bed') == 'on'
        with_baggage = request.form.get('with_baggage') == 'on'
        age = request.form.get('age')
        departure = request.form.get('departure')
        destination = request.form.get('destination')
        travel_date = request.form.get('travel_date')
        insurance = request.form.get('insurance') == 'on'
        if not name:
            error_messages['name'] = "Укажите ФИО."
        if not bunk:
            error_messages['bunk'] = "Выберите тип полки."
        if not age or not age.isdigit() or not (1 <= int(age) <= 120):
            error_messages['age'] = "Возраст должен быть от 1 до 120 лет."
        if not departure:
            error_messages['departure'] = "Укажите пункт выезда."
        if not destination:
            error_messages['destination'] = "Укажите пункт назначения."
        if not travel_date:
            error_messages['travel_date'] = "Укажите дату поездки."
        if error_messages:
            return render_template('lab3/ticket.html', error_messages=error_messages)
        age = int(age)
        is_child = age < 18
        base_price = 700 if is_child else 1000
        if bunk in ['нижняя', 'нижняя боковая']:
            base_price += 100
        if with_bed:
            base_price += 75
        if with_baggage:
            base_price += 250
        if insurance:
            base_price += 150
        return render_template('lab3/ticket_result.html', 
                               name=name, age=age, is_child=is_child,
                               departure=departure, destination=destination,
                               travel_date=travel_date, bunk=bunk, 
                               with_bed=with_bed, with_baggage=with_baggage,
                               insurance=insurance, price=base_price)
    return render_template('lab3/ticket.html', error_messages={})
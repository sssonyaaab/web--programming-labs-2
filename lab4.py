from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    if x2 == '0':
         return render_template('lab4/div.html', error='На ноль делить нельзя!')
    
    x1 = int(x1)
    x2 = int(x2)
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/ymno')
def ymno():
    return render_template('lab4/ymno.html')


@lab4.route('/lab4/ymno-', methods=['POST'])
def ymno_():
    x1 = request.form.get('x1') or '1'
    x2 = request.form.get('x2') or '1'
    x1 = int(x1)
    x2 = int(x2)
    result = x1 * x2
    return render_template('lab4/ymno.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/summ')
def summ():
    return render_template('lab4/summ.html')


@lab4.route('/lab4/summ-', methods=['POST'])
def summ_():
    x1 = request.form.get('x1') or '0'
    x2 = request.form.get('x2') or '0'
    x1 = int(x1)
    x2 = int(x2)
    result = x1 + x2
    return render_template('lab4/summ.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/vich')
def vich():
    return render_template('lab4/vich.html')


@lab4.route('/lab4/vich-', methods=['POST'])
def vich_():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/vich.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/vich.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/step')
def step():
    return render_template('lab4/step.html')


@lab4.route('/lab4/step-', methods=['POST'])
def step_():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/step.html', error='Оба поля должны быть заполнены!')
    if x1 == '0' and x2 == '0':
        return render_template('lab4/step.html', error='Оба поля не должны быть равны 0!')
    
    x1 = int(x1)
    x2 = int(x2)
    result = x1 ** x2
    return render_template('lab4/step.html', x1=x1, x2=x2, result=result)


tree_count=0

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')
    
    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < 10:
        tree_count += 1

    return redirect('/lab4/tree')


users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр Финин', 'gender': 'male'},
    {'login': 'bob', 'password': '555', 'name': 'Боб Краснов', 'gender': 'male'},
    {'login': 'vadim', 'password': '666', 'name': 'Вадим Логинов', 'gender': 'male'},
    {'login': 'ignat', 'password': '444', 'name': 'Игнат Мартыненко', 'gender': 'male'},
]


@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            name = session['name']
        else:
            authorized = False
            login = ''
            name = ''
        return render_template('lab4/login.html', authorized=authorized, login=login, name=name)
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login:
        error = 'Не введён логин'
        return render_template('lab4/login.html', error=error, authorized=False, login=login)
    if not password:
        error = 'Не введён пароль'
        return render_template('lab4/login.html', error=error, authorized=False, login=login)

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            session['name'] = user['name']
            return redirect('/lab4/login')
    
    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login=login)


@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    error = None
    message = None
    snowflakes = 0

    if request.method == 'POST':
        temp = request.form.get('temperature')
        if temp is None or temp == '':
            error = "Ошибка: не задана температура"
        else:
            try:
                temp = float(temp)
                if temp < -12:
                    error = "Не удалось установить температуру — слишком низкое значение"
                elif temp > -1:
                    error = "Не удалось установить температуру — слишком высокое значение"
                elif -12 <= temp <= -9:
                    message = f"Установлена температура: {temp}°С"
                    snowflakes = 3
                elif -8 <= temp <= -5:
                    message = f"Установлена температура: {temp}°С"
                    snowflakes = 2
                elif -4 <= temp <= -1:
                    message = f"Установлена температура: {temp}°С"
                    snowflakes = 1
            except ValueError:
                error = "Ошибка: температура должна быть числом"

    return render_template('lab4/fridge.html', error=error, message=message, snowflakes=snowflakes)


prices = {
    'ячмень': 12345,
    'овёс': 8522,
    'пшеница': 8722,
    'рожь': 14111
}

@lab4.route('/lab4/order', methods=['GET', 'POST'])
def order():
    error = None
    message = None
    discount = None
    if request.method == 'POST':
        grain_type = request.form.get('grain_type')
        weight = request.form.get('weight')
        if not weight:
            error = "Ошибка: вес не указан"
        else:
            try:
                weight = float(weight)
                if weight <= 0:
                    error = "Ошибка: вес должен быть больше 0"
                elif weight > 500:
                    error = "Такого объёма сейчас нет в наличии"
                else:
                    price = prices.get(grain_type)
                    total_price = weight * price
                    if weight > 50:
                        discount = 0.10
                        total_price *= (1 - discount)
                    message = (f"Заказ успешно сформирован. Вы заказали {grain_type}. "
                                f"Вес: {weight} т. Сумма к оплате: {total_price:.2f} руб")
            except ValueError:
                error = "Ошибка: вес должен быть числом"
    return render_template('lab4/order.html', error=error, message=message, discount=discount)
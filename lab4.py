from flask import Blueprint, render_template, request, redirect
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


@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab4/login.html', authorized=False)
    
    login = request.form.get('login')
    password = request.form.get('password')

    if login == 'alex' and password == '123':
        return render_template('lab4/login.html', login=login, authorized=True)
    
    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False)
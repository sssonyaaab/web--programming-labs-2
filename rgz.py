from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

rgz = Blueprint('rgz', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='rgz',
            user='rgz',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database1.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def validate_login(login, password):
    if not login:
        return False, "Логин не может быть пустым."
    if not password:
        return False, "Пароль не может быть пустым."

    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-")
    if not all(char in allowed_chars for char in login):
        return False, "Логин должен состоять только из латинских букв, цифр и знаков препинания (_.-)."

    if len(password) < 6:
        return False, "Пароль должен быть не менее 6 символов."

    return True, ""

@rgz.route('/rgz')
def home():
    return render_template('rgz/home.html')

@rgz.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        if not login.isalnum() or len(password) < 6:
            message = "Логин должен содержать только буквы и цифры, пароль должен быть не менее 6 символов."
        else:
            hashed_password = generate_password_hash(password)
            try:
                conn, cur = db_connect()
                if current_app.config['DB_TYPE'] == 'postgres':
                    cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, hashed_password))
                else:
                    cur.execute("INSERT INTO users (login, password) VALUES (?, ?)", (login, hashed_password))
                conn.commit()
                conn.close()
                return redirect(url_for('rgz.login'))
            except Exception as e:
                message = f"Ошибка регистрации: {e}"
                conn.close()

    return render_template('rgz/register.html', message=message)

@rgz.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        if not login or not password:
            message = "Пожалуйста, заполните все поля."
            return render_template('rgz/login.html', message=message)

        try:
            conn, cur = db_connect()
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT * FROM users WHERE login = %s;", (login,))
            else:
                cur.execute("SELECT * FROM users WHERE login = ?", (login,))
            user = cur.fetchone()

            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                return redirect(url_for('rgz.profile'))
            else:
                message = "Неверный логин или пароль."
        except Exception as e:
            message = f"Ошибка авторизации: {e}"
        finally:
            conn.close()

    return render_template('rgz/login.html', message=message)

@rgz.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('rgz.login'))

    message = None
    try:
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM users WHERE id = %s;", (session['user_id'],))
        else:
            cur.execute("SELECT * FROM users WHERE id = ?;", (session['user_id'],))
        user = cur.fetchone()

        if request.method == 'POST':
            name = request.form.get('name', user['name'])
            age = request.form.get('age', user['age'])
            gender = request.form.get('gender', user['gender'])
            search_gender = request.form.get('search_gender', user['search_gender'])
            about = request.form.get('about', user['about'])
            photo = request.form.get('photo', user['photo'])

            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("""
                    UPDATE users
                    SET name = %s, age = %s, gender = %s, search_gender = %s, about = %s, photo = %s
                    WHERE id = %s;
                """, (name, age, gender, search_gender, about, photo, session['user_id']))
            else:
                cur.execute("""
                    UPDATE users
                    SET name = ?, age = ?, gender = ?, search_gender = ?, about = ?, photo = ?
                    WHERE id = ?
                """, (name, age, gender, search_gender, about, photo, session['user_id']))
            conn.commit()

            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT * FROM users WHERE id = %s;", (session['user_id'],))
            else:
                cur.execute("SELECT * FROM users WHERE id = ?", (session['user_id'],))
            user = cur.fetchone()

            message = "Профиль обновлен!"

        return render_template('rgz/profile.html', user=user, message=message)
    except Exception as e:
        message = f"Ошибка: {e}"
    finally:
        conn.close()

    return render_template('rgz/profile.html', message=message)

@rgz.route('/hide_profile', methods=['POST'])
def hide_profile():
    if 'user_id' not in session:
        return redirect(url_for('rgz.login'))

    message = None
    try:
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET hidden = TRUE WHERE id = %s;", (session['user_id'],))
        else:
            cur.execute("UPDATE users SET hidden = TRUE WHERE id = ?", (session['user_id'],))
        conn.commit()
        message = "Ваш профиль скрыт."
    except Exception as e:
        message = f"Ошибка: {e}"
    finally:
        conn.close()

    return redirect(url_for('rgz.profile', message=message))

@rgz.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        return redirect(url_for('rgz.login'))

    try:
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM users WHERE id = %s;", (session['user_id'],))
        else:
            cur.execute("DELETE FROM users WHERE id = ?", (session['user_id'],))
        conn.commit()
        conn.close()
        session.pop('user_id', None)
        return redirect(url_for('rgz.register'))
    except Exception as e:
        message = f"Ошибка: {e}"
        conn.close()
        return render_template('rgz/profile.html', message=message)

@rgz.route('/search', methods=['GET'])
def search():
    if 'user_id' not in session:
        return redirect(url_for('rgz.login'))

    message = None
    try:
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM users WHERE id = %s;", (session['user_id'],))
        else:
            cur.execute("SELECT * FROM users WHERE id = ?", (session['user_id'],))
        current_user = cur.fetchone()

        current_gender = current_user['gender']
        current_search_gender = current_user['search_gender']

        page = request.args.get('page', 1, type=int)
        per_page = 3
        offset = (page - 1) * per_page

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT * FROM users
                WHERE gender = %s AND search_gender = %s AND id != %s AND hidden = FALSE
                LIMIT %s OFFSET %s;
            """, (current_search_gender, current_gender, session['user_id'], per_page, offset))
        else:
            cur.execute("""
                SELECT * FROM users
                WHERE gender = ? AND search_gender = ? AND id != ? AND hidden = FALSE
                LIMIT ? OFFSET ?
            """, (current_search_gender, current_gender, session['user_id'], per_page, offset))
        users = cur.fetchall()

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT COUNT(*) FROM users
                WHERE gender = %s AND search_gender = %s AND id != %s AND hidden = FALSE;
            """, (current_search_gender, current_gender, session['user_id']))
        else:
            cur.execute("""
                SELECT COUNT(*) FROM users
                WHERE gender = ? AND search_gender = ? AND id != ? AND hidden = FALSE
            """, (current_search_gender, current_gender, session['user_id']))
        total_users = cur.fetchone()['count']
        total_pages = (total_users + per_page - 1) // per_page

        return render_template('rgz/search.html', users=users, page=page, total_pages=total_pages, message=message)
    except Exception as e:
        message = f"Ошибка: {e}"
        return render_template('rgz/search.html', users=[], page=1, total_pages=1, message=message)
    finally:
        conn.close()

@rgz.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('rgz.login'))
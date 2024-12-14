from flask import Blueprint, render_template, request, jsonify, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab7 = Blueprint('lab7', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='sonya_baranova_knowledge_base',
            user='sonya_baranova_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur


@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')


#films = [
    {
        "title": "Intouchables",
        "title_ru": "1+1",
        "year": 2011,
        "description": "Пострадав в результате несчастного случая,\
            богатый аристократ Филипп нанимает в помощники человека,\
            который менее всего подходит для этой работы, – молодого жителя предместья Дрисса,\
            только что освободившегося из тюрьмы. Несмотря на то, что Филипп прикован к инвалидному креслу,\
            Дриссу удается привнести в размеренную жизнь аристократа дух приключений."
    },
    {
        "title": "Interstellar",
        "title_ru": "Интерстеллар",
        "year": 2014,
        "description": "Когда засуха, пыльные бури и вымирание растений приводят человечество к продовольственному кризису,\
            коллектив исследователей и учёных отправляется сквозь червоточину (которая предположительно соединяет области\
            пространства-времени через большое расстояние) в путешествие,\
            чтобы превзойти прежние ограничения для космических путешествий человека и найти планету с подходящими для человечества условиями."
    },
    {
        "title": "The Shawshank Redemption",
        "title_ru": "Побег из Шоушенка",
        "year": 1994,
        "description": "Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника.  \
            Оказавшись в тюрьме под названием Шоушенк, он сталкивается с жестокостью и беззаконием, \
            царящими по обе стороны решётки. Каждый, кто попадает в эти стены, \
            становится их рабом до конца жизни. Но Энди, обладающий живым умом и доброй душой, \
            находит подход как к заключённым, так и к охранникам, добиваясь их особого к себе расположения."
    },
    {
        "title": "The Green Mile",
        "title_ru": "Зеленая миля",
        "year": 1999,
        "description": "Пол Эджкомб — начальник блока смертников в тюрьме «Холодная гора», \
            каждый из узников которого однажды проходит «зеленую милю» по пути к месту казни. \
            Пол повидал много заключённых и надзирателей за время работы. Однако гигант Джон Коффи, \
            обвинённый в страшном преступлении, стал одним из самых необычных обитателей блока."
    },
    {
        "title": "Shutter Island",
        "title_ru": "Остров проклятых",
        "year": 2009,
        "description": "Два американских судебных пристава отправляются на один из островов в штате Массачусетс, чтобы расследовать исчезновение пациентки клиники для умалишенных преступников. При проведении расследования им придется столкнуться с паутиной лжи, обрушившимся ураганом и смертельным бунтом обитателей клиники."
    },
#]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films")
    films = cur.fetchall()
    conn.close()
    return jsonify(films)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films WHERE id = %s", (id,))
    film = cur.fetchone()
    conn.close()
    if not film:
        return 'Номер выходит за пределы значений', 404
    return jsonify(film)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    cur.execute("DELETE FROM films WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return '', 204


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = request.get_json()
    if not film['title_ru']:
        return {'title_ru': 'Русское название не может быть пустым'}, 400
    if 'title' not in film or not film['title']:
        if not film['title_ru']:
            return {'title': 'Название на оригинальном языке не может быть пустым, если русское название пустое'}, 400
        film['title'] = film['title_ru']
    year_int = int(film['year'])
    now_year = 2024
    if not (1895 <= year_int <= now_year):
        return {'year': f'Год должен быть от 1895 до {now_year}'}, 400
    if not film['description']:
        return {'description': 'Описание не может быть пустым'}, 400
    if len(film['description']) > 2000:
        return {'description': 'Описание не может быть длиннее 2000 символов'}, 400
    conn, cur = db_connect()
    cur.execute("""
        UPDATE films
        SET title = %s, title_ru = %s, year = %s, description = %s
        WHERE id = %s
    """, (film['title'], film['title_ru'], film['year'], film['description'], id))
    conn.commit()
    conn.close()
    return '', 204


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    new_film = request.get_json()
    if not new_film['title_ru']:
        return {'title_ru': 'Русское название не может быть пустым'}, 400
    if 'title' not in new_film or not new_film['title']:
        if not new_film['title_ru']:
            return {'title': 'Название на оригинальном языке не может быть пустым, если русское название пустое'}, 400
        new_film['title'] = new_film['title_ru']
    year_int = int(new_film['year'])
    now_year = 2024
    if not (1895 <= year_int <= now_year):
        return {'year': f'Год должен быть от 1895 до {now_year}'}, 400
    if not new_film['description']:
        return {'description': 'Описание не может быть пустым'}, 400
    if len(new_film['description']) > 2000:
        return {'description': 'Описание не может быть длиннее 2000 символов'}, 400
    conn, cur = db_connect()
    cur.execute("""
        INSERT INTO films (title, title_ru, year, description)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (new_film['title'], new_film['title_ru'], new_film['year'], new_film['description']))
    new_id = cur.fetchone()['id']
    conn.commit()
    conn.close()
    return {'id': new_id}, 201
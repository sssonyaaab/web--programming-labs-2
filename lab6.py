from flask import Blueprint, render_template, request, redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab6 = Blueprint('lab6', __name__)

offices = []
for i in range(1,11):
    offices.append({"number": i, "tenant": "", "price":  900 + i % 3})

@lab6.route('/lab6/')
def lab():
    return render_template('lab6/lab6.html')

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'sonya_baranova_knowledge_base',
            user = 'sonya_baranova_knowledge_base',
            password = '123'
        )
        cur = conn.cursor(cursor_factory = RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def insert_offices_data():
    conn, cur = db_connect()
    for office in offices:
        cur.execute("INSERT INTO offices (number, tenant, price) VALUES (%s, %s, %s)",
                    (office['number'], office['tenant'], office['price']))
    conn.commit()
    cur.close()
    conn.close()

@lab6.route('/lab6/json-rpc-api/', methods = ['POST'])
def api():
    data = request.json
    id = data['id']
    conn, cur = db_connect()
    if data['method'] == 'info':
        cur.execute("SELECT * FROM offices")
        offices = cur.fetchall()
        cur.close()
        conn.close()
        return {
            'jsonrpc':'2.0',
            'result': offices,
            'id': id
        }
    
    login = session.get('login')
    if not login:
        cur.close()
        conn.close()
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }
    if data['method'] == 'booking':
        office_number = data['params']
        cur.execute("SELECT * FROM offices WHERE number = %s", (office_number,))
        office = cur.fetchone()
        if office['tenant'] != '':
            cur.close()
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 2,
                    'message': 'Already booked'
                },
                'id': id
            }
        cur.execute("UPDATE offices SET tenant = %s WHERE number = %s", (login, office_number))
        conn.commit()
        cur.close()
        conn.close()
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }

    if data['method'] == 'cancellation':
        office_number = data['params']
        cur.execute("SELECT * FROM offices WHERE number = %s", (office_number, ))
        office = cur.fetchone()
        if office['tenant'] == '':
            cur.close()
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 3,
                    'message': 'Office is not booked'
                },
                'id': id
            }
        if office['tenant'] != login:
            cur.close()
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 4,
                    'message': 'You are not the tenant of this office'
                },
                'id': id
            }
        cur.execute("UPDATE offices SET tenant = '' WHERE number = %s", (office_number,))
        conn.commit()
        cur.close()
        conn.close()
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }
    cur.close()
    conn.close()
    return {
        'jsonrpc': '2.0',
        'error': {
            'cove': -32601,
            'message': 'Method not found'
        },
        'id': id
    }
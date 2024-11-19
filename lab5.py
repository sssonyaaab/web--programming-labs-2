from flask import Blueprint, render_template, request, redirect, session, url_for
lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    name = 'Анонимус'
    return render_template('lab5/lab5.html', name=name)


@lab5.route('/lab5/login')
def login():
    return ''


@lab5.route('/lab5/register')
def register():
    return ''


@lab5.route('/lab5/list')
def list():
    return ''


@lab5.route('/lab5/create')
def create():
    return ''
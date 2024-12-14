from flask import Blueprint, render_template, request

lab7 = Blueprint('lab7', __name__)


@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')


films = [
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
]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        return 'Номер выходит за пределы значений', 404
    return films[id]

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        return 'Номер выходит за пределы значений', 404
    del films[id]
    return '', 204


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        return 'Номер выходит за пределы значений', 404
    film = request.get_json()
    if not film or 'title' not in film or 'title_ru' not in film or 'year' not in film or 'description' not in film:
        return 'Некорректные данные фильма', 400
    films[id] = film
    return films[id]


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    new_film = request.get_json()
    if not new_film or 'title' not in new_film or 'title_ru' not in new_film or 'year' not in new_film or 'description' not in new_film:
        return 'Некорректные данные фильма', 400
    films.append(new_film)
    return {'id': len(films) - 1}
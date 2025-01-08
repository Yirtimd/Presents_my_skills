import json
import sqlite3
from flask_socketio import SocketIO, emit
from flask import Flask, g, jsonify, request
from db import get_db_connection, init_db
from flask_cors import CORS
from generate_hero_yandex_gpt import request_text


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


@app.before_request
def before_request():
    """Открываем подключение к базе перед каждым запросом."""
    g.db = get_db_connection()


@app.teardown_request
def teardown_request(exception):
    """Закрываем подключение после обработки запроса."""
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def seed_data():
    conn = get_db_connection()
    heroes_exist = conn.execute('SELECT COUNT(*) FROM `heroes`').fetchone()[0]
    if heroes_exist == 0:
        data = [
            ("Superman", "Male", "Flight, Super Strength, Heat Vision", 95),
            ("Wonder Woman", "Female", "Combat Skills, Super Strength, Lasso of Truth", 90),
            ("Batman", "Male", "Intelligence, Martial Arts, Gadgets", 85),
            ("Spider-Man", "Male", "Wall Climbing, Web-Shooting, Agility", 80),
            ("Black Widow", "Female", "Espionage, Martial Arts, Hacking", 75),
            ("Iron Man", "Male", "Engineering, Powered Suit, Intelligence", 92),
            ("Captain Marvel", "Female", "Energy Manipulation, Super Strength, Flight", 93),
            ("Thor", "Male", "God of Thunder, Super Strength, Mjolnir", 94),
            ("Scarlet Witch", "Female", "Reality Manipulation, Telekinesis, Magic", 98),
            ("The Flash", "Male", "Super Speed, Time Travel, Quick Reflexes", 89)
        ]
        conn.executemany('INSERT INTO heroes (person_name, gender, skills, power_score) VALUES (?, ?, ?, ?)', data)
        conn.commit()
        print("Данные успешно добавлены!")
    else:
        print("Данные уже существуют, добавление пропущено.")
    conn.close()


def get_sql_data_all_hero():
    """Возвращает список всех полей"""
    cursor = g.db.execute("SELECT * FROM heroes")
    heroes = cursor.fetchall()
    cursor.close()
    return [dict(person) for person in heroes]


@app.route('/data', methods=['GET', 'POST'])
def get_all_hero():
    """Возвращает список всех полей"""
    data = get_sql_data_all_hero()
    return jsonify(data)


@app.route('/rang_score', methods=['GET'])
def get_score():
    filter_value = request.args.get('filter', 'all')
    if filter_value == 'rang_sort':
        cursor = g.db.execute("SELECT * FROM heroes WHERE power_score > 85")
        persons = cursor.fetchall()
        cursor.close()
        socketio.emit('update_data', [dict(hero) for hero in persons])
    else:
        data = get_sql_data_all_hero()
        socketio.emit('update_data', data)
    return '', 200


@app.route('/female', methods=['GET'])
def get_female():
    filter_value = request.args.get('filter', 'all')
    if filter_value == 'female':
        cursor = g.db.execute("SELECT * FROM heroes WHERE gender = 'Female'")
        persons = cursor.fetchall()
        cursor.close()
        socketio.emit('update_data', [dict(hero) for hero in persons])
    else:
        data = get_sql_data_all_hero()
        socketio.emit('update_data', data)
    return '', 200


@app.route('/male', methods=['GET'])
def get_male():
    filter_value = request.args.get('filter', 'all')
    if filter_value == 'male':
        cursor = g.db.execute("SELECT * FROM heroes WHERE gender = 'Male'")
        persons = cursor.fetchall()
        cursor.close()
        socketio.emit('update_data', [dict(hero) for hero in persons])
    else:
        data = get_sql_data_all_hero()
        socketio.emit('update_data', data)
    return '', 200


@app.route('/submit', methods=['GET', 'POST'])
def add_hero():
    data = request.json
    data['skills'] = ','.join(data['skills'])
    g.db.execute("""
        INSERT INTO heroes (person_name, gender, skills, power_score)
        VALUES (:person_name, :gender, :skills, :power_score)
    """, data)
    g.db.commit()
    print(f"данные получены: {data}")

    cursor = g.db.execute("SELECT * FROM heroes")
    heroes = cursor.fetchall()
    cursor.close()
    socketio.emit('update_data', [dict(hero) for hero in heroes])
    return jsonify({"message": "Hero added successfully"}), 201


@app.route('/delete', methods=['GET', 'POST'])
def delete_hero():
    data = request.json
    print(f"данные получены: {data}")
    g.db.execute('DELETE FROM heroes WHERE id=:id', data)
    g.db.commit()

    cursor = g.db.execute("SELECT * FROM heroes")
    heroes = cursor.fetchall()
    cursor.close()
    socketio.emit('update_data', [dict(hero) for hero in heroes])
    return jsonify({"message": "Hero delete successfully"}), 201


@app.route('/generate_hero', methods=['GET'])
def generate_hero():
    cursor = g.db.execute("SELECT person_name FROM heroes")
    heroes = cursor.fetchall()
    cursor.close()
    name_exist = [dict(person) for person in heroes]

    data_hero_generate = request_text(name_exist)

    gender = data_hero_generate.get('gender')
    person_name = data_hero_generate.get('person_name')
    skills = data_hero_generate.get('skills')
    power_score = data_hero_generate.get('power_score')

    g.db.execute("""
        INSERT INTO heroes (person_name, gender, skills, power_score)
        VALUES (?, ?, ?, ?)
    """, (person_name, gender, skills, power_score))
    g.db.commit()

    data = get_sql_data_all_hero()
    socketio.emit('update_data', data)
    return '', 200


if __name__ == "__main__":
    app.run(debug=True)
    seed_data()
    socketio.run(app, host="0.0.0.0", port=5000)


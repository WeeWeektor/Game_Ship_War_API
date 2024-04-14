from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
import json

app = Flask(__name__)

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'user'
# app.config['MYSQL_PASSWORD'] = '1234567890qwerty'
# app.config['MYSQL_PORT'] = 3306
# app.config['MYSQL_DB'] = 'War_ship_game'

# app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_HOST'] = 'host.docker.internal'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'my-secret-pw'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_DB'] = 'War_ship_game'

mysql = MySQL(app)


@app.route('/login', methods=['POST'])
def login():
    all_posts = []
    cur = mysql.connection.cursor()
    cur.execute('''SELECT post FROM User_registration''')
    get_post_db = cur.fetchall()
    for el in get_post_db:
        all_posts.append(el[0])

    data = json.loads(request.data)
    data_post = data['post']

    if data_post in all_posts:
        cur.execute(f'''SELECT id, password, name from User_registration WHERE post = '{data_post}' ''')
        get_all_db = cur.fetchone()
        data_password = data['password']
        if data_password == get_all_db[1]:
            cur.execute(f'''SELECT * FROM User_info where id = '{get_all_db[0]}' ''')
            get_all_info_db = cur.fetchone()
            get_info_db = list(get_all_info_db)
            cur.close()
            return jsonify({'message': 'Login successful', 'id': get_all_db[0], 'password': get_all_db[1],
                            'name': get_all_db[2], 'info': get_info_db}), 200
        else:
            return jsonify({'message': 'Password is wrong', 'id': None, 'password': None, 'name': None}), 200
    else:
        cur.close()
        return jsonify({'message': 'Email is wrong or you not registered', 'id': None, 'password': None,
                        'name': None}), 200


@app.route('/registration', methods=['POST'])
def registration():
    all_posts = []
    cur = mysql.connection.cursor()
    cur.execute('''SELECT post FROM User_registration''')
    get_post_db = cur.fetchall()
    for el in get_post_db:
        all_posts.append(el[0])

    data = json.loads(request.data)
    data_post = data['post']
    data_name = data['name']
    data_password = data['password']

    if data_post not in all_posts:
        insert_data_registration = f'''
                                        INSERT INTO 
                                            `User_registration` (`post`, `name`, `password`)
                                        VALUES 
                                             ('{data_post}', '{data_name}', '{data_password}')
                                        '''
        cur.execute(insert_data_registration)
        mysql.connection.commit()

        cur.execute(f'''SELECT LAST_INSERT_ID()''')
        get_id_db = cur.fetchone()

        all_id = []
        cur.execute('''SELECT id FROM User_info''')
        get_id_db_info = cur.fetchall()
        for el in get_id_db_info:
            all_id.append(el[0])

        if get_id_db[0] not in all_id:
            insert_data_info = f'''
                                 INSERT INTO
                                    `User_info` (`id`, `count`, `count_win`, `count_loos`, `col_10`, `col_9`, 
                                                     `col_8`, `col_7`, `col_6`, `col_5`, `col_4`, `col_3`, `col_2`, 
                                                     `col_1`)
                                    VALUES
                                        ('{get_id_db[0]}', 0, 0, 0, 'N10', 'N9', 'N8', 'N7', 'N6', 
                                        'N5', 'N4', 'N3', 'N2', 'N1')
                                    '''
            cur.execute(insert_data_info)
            mysql.connection.commit()
            cur.execute(f'''SELECT * FROM User_info where id = '{get_id_db[0]}' ''')
            get_all_info_db = cur.fetchone()
            get_info_db_r = list(get_all_info_db)
            cur.close()
            return jsonify({'message': 'Registration successful', 'id': get_id_db[0], 'info': get_info_db_r}), 200
    else:
        cur.close()
        return jsonify({'message': 'User with this email has been created'}), 200


@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = json.loads(request.data)
    data_post = data['post']
    data_name = data['name']
    data_password = data['password']
    cur = mysql.connection.cursor()
    cur.execute(f'''SELECT post, name, id from User_registration where post = '{data_post}' and 
                    name = '{data_name}' ''')
    get_all_db = cur.fetchone()

    if get_all_db is None or get_all_db[1] != data_name:
        cur.close()
        return jsonify({'message': 'User with this email has`t been fond'}), 200
    elif get_all_db[1] == data_name:
        cur.execute(f'''UPDATE User_registration SET password = '{data_password}' WHERE id = '{get_all_db[2]}' ''')
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'User has been new password'}), 200


@app.route('/history', methods=['POST'])
def history():
    data = json.loads(request.data)
    data_id = data['id']
    data_all_war = data['all_war']
    data_win_war = data['win_war']
    data_loss_war = data['loss_war']
    data_war_info = data['war_info']
    cur = mysql.connection.cursor()
    cur.execute(f'''UPDATE User_info SET 
                                    count = '{data_all_war}',
                                    count_win = '{data_win_war}',
                                    count_loos = '{data_loss_war}',
                                    col_10 = '{data_war_info[0]}',
                                    col_9 = '{data_war_info[1]}',
                                    col_8 = '{data_war_info[2]}',
                                    col_7 = '{data_war_info[3]}',
                                    col_6 = '{data_war_info[4]}',
                                    col_5 = '{data_war_info[5]}',
                                    col_4 = '{data_war_info[6]}',
                                    col_3 = '{data_war_info[7]}',
                                    col_2 = '{data_war_info[8]}',
                                    col_1 = '{data_war_info[9]}'
                                WHERE id = '{data_id}' ''')
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Data update'}), 200


if __name__ == '__main__':
    app.run()

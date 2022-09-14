import sqlite3
from flask import Response
from flask_restx import Resource, Namespace


USER = Namespace(name='USER')

@USER.route('/info')
class login(Resource):
    parser = USER.parser()
    parser.add_argument('user', type=str, location='form')
    parser.add_argument('passwd', type=str, location='form')

    @USER.response(200, 'Success')
    @USER.response(400, 'Bad Request')

    def put(self):
        args = self.parser.parse_args()
        user_name = args['user']
        passwd = args['passwd']
        conn = sqlite3.connect('database.db')
        try:
            cur = conn.cursor()
            cur.execute(f"SELECT user FROM users WHERE user = '{user_name}'")
            user_list = cur.fetchall()
            if len(user_list) == 0:
                cur.execute(f"INSERT into users (user, passwd, type) values('{user_name}','{passwd}','local')")
            else:
                return Response('already exist user')
            conn.commit()
            return Response('success')
        except Exception as e:
            conn.rollback()
            conn.close()
            return Response(f'Fail:{str(e)}')

@USER.route('/info/<string:user_name>')
class login(Resource):
    @USER.response(200, 'Success')
    @USER.response(400, 'Bad Request')

    def delete(self, user_name):
        conn = sqlite3.connect('database.db')
        try:
            cur = conn.cursor()
            cur.execute(f"SELECT user FROM users WHERE user = '{user_name}'")
            user_list = cur.fetchall()
            if len(user_list) != 0:
                cur.execute(f"DELETE FROM users WHERE USER = '{user_name}'")
            else:
                return Response('does not exists user')
            conn.commit()
            return Response('success')

        except Exception as e:
            conn.rollback()
            conn.close()
            return Response(f'Fail:{str(e)}')

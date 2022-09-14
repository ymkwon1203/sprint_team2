import sqlite3
from flask import request, Response, json, session, redirect, url_for
from flask_restx import Resource, Namespace
import requests
import key.oauth_key as key


LOGIN = Namespace(name='LOGIN')


@LOGIN.route('/')
class login(Resource):
    parser = LOGIN.parser()
    parser.add_argument('user', type=str, location='form')
    parser.add_argument('passwd', type=str, location='form')
    @LOGIN.response(200, 'Success')
    @LOGIN.response(400, 'Bad Request')
    def post(self):
        conn = sqlite3.connect('database.db')
        args = self.parser.parse_args()
        user_id = args['user']
        passwd = args['passwd']
        try:
            cur = conn.cursor()
            cur.execute(f"select * from users where user = '{user_id}'")
            data = cur.fetchall()
            if len(data) == 0:
                return Response('incorrect user name')
            cur.execute(f"select passwd from users where user = '{user_id}'")
            check_pass = cur.fetchall()
            conn.commit()
            if check_pass[0][0] == passwd:
                session['user_id'] = user_id
                return Response('success')
            else:
                return Response('invalid user or password')

        except Exception as e:
            conn.rollback()
            conn.close()
            return Response(f'Fail:{str(e)}')


@LOGIN.route('/google')
class googleLoginPost(Resource):
    def get(self):
        google_provider_cfg = key.get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        request_uri = key.google_client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url+"/callback",
            scope=["openid", "email"],
        )
        return redirect(request_uri)


@LOGIN.route('/google/callback')
class googleLoginCallback(Resource):
    def get(self):
        # Get authorization code Google sent back to you
        try:
            code = request.args.get("code")

            # Find out what URL to hit to get tokens that allow you to ask for
            # things on behalf of a user
            google_provider_cfg = key.get_google_provider_cfg()
            token_endpoint = google_provider_cfg["token_endpoint"]

            # Prepare and send request to get tokens! Yay tokens!
            token_url, headers, body = key.google_client.prepare_token_request(
                token_endpoint,
                authorization_response=request.url,
                redirect_url=request.base_url,
                code=code,
            )
            token_response = requests.post(
                token_url,
                headers=headers,
                data=body,
                auth=(key.GOOGLE_CLIENT_ID, key.GOOGLE_CLIENT_SECRET),
            )

            # Parse the tokens!
            key.google_client.parse_request_body_response(json.dumps(token_response.json()))

            # Now that we have tokens (yay) let's find and hit URL
            # from Google that gives you user's profile information,
            # including their Google Profile Image and Email
            userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
            uri, headers, body = key.google_client.add_token(userinfo_endpoint)
            userinfo_response = requests.get(uri, headers=headers, data=body)

            # We want to make sure their email is verified.
            # The user authenticated with Google, authorized our
            # app, and now we've verified their email through Google!
            if userinfo_response.json().get("email_verified"):
                unique_id = userinfo_response.json()["sub"]
                users_email = userinfo_response.json()["email"]
            else:
                return "User email not available or not verified by Google.", 400

            # Create a user in our db with the information provided
            # by Google
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute(f"SELECT user_id FROM users WHERE user_id = '{unique_id}'")
            user_list = cur.fetchall()
            if len(user_list) == 0:
                cur.execute(f"INSERT into users (user_id, user_name, email, type, permission) values('{unique_id}','{users_email}','{users_email}', 'google', 'user')")
            conn.commit()

            # Begin user session by logging the user in
            session['user_id'] = unique_id

            # Send user back to homepage
            return Response('success')

        except Exception as e:
            return Response(f'Fail:{str(e)}')


@LOGIN.route('/kakao/')
class kakaoLoginPost(Resource):
    def get(self):
        CLIENT_ID = key.KAKAO_CLIENT_ID
        REDIRECT_URI = key.KAKAO_REDIRECT_URI
        request_uri = f"https://kauth.kakao.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code"
        return redirect(request_uri)

@LOGIN.route('/kakao/callback')
class kakaoLoginCallBack(Resource):
    def get(self):
        # Get authorization code Google sent back to you
        try:
            code = request.args["code"]
            CLIENT_ID = key.KAKAO_CLIENT_ID
            REDIRECT_URI = key.KAKAO_REDIRECT_URI
            CLIENT_SECRET = key.KAKAO_CLIENT_SECRET
            auth_server = "https://kauth.kakao.com%s"
            api_server = "https://kapi.kakao.com%s"
            def_header ={
                "Content-Type": "application/x-www-form-urlencoded",
                "Cache-Control": "no-cache",
            }

            auth_info = requests.post(
                url= auth_server % "/oauth/token",
                headers = def_header,
                data={
                    "grant_type": "authorization_code",
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "redirect_uri": REDIRECT_URI,
                    "code": code,
                },
            ).json()

            if "error" in auth_info:
                print("에러가 발생했습니다.")
                return {'message': '인증 실패'}, 404

            user = requests.post(
                url=api_server % "/v2/user/me",
                headers={
                    **def_header,
                    **{"Authorization": "Bearer " + auth_info['access_token']}
                },
                # "property_keys":'["kakao_account.profile_image_url"]'
                data={}
            ).json()

            id = user["id"]
            kakao_account = user["kakao_account"]
            profile = kakao_account["profile"]
            name = profile["nickname"]

            if "email" in kakao_account.keys():
                email = kakao_account["email"]
            else:
                email = f"{name}@kakao.com"


            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute(f"SELECT user_id FROM users WHERE user_id = '{id}'")
            user_list = cur.fetchall()
            if len(user_list) == 0:
                cur.execute(f"INSERT into users (user_id, user_name, email, type, permission) values('{id}','{name}','{email}', 'kakao', 'user')")
            conn.commit()

            session['user_id'] = id

            # Send user back to homepage
            return Response('success')

        except Exception as e:
            return Response(f'Fail:{str(e)}')
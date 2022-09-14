import importlib
import sqlite3
import ssl


if __name__ == '__main__':
    module_name = 'flaskapp.app'
    module = importlib.import_module(module_name)
    creator = getattr(module, 'create_app')
    app = creator()
    conn = sqlite3.connect('database.db')
    conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS users (
        id integer PRIMARY KEY autoincrement default 1,
        user_id TEXT UNIQUE NOT NULL, user_name TEXT NOT NULL, 
        email TEXT UNIQUE NOT NULL, passwd TEXT, type TEXT NOT NULL, permission TEXT NOT NULL);
        '''
    )
    conn.close()

    # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    # ssl_context.load_cert_chain(certfile='../cert/cert.pem', keyfile='../cert/key.pem', password='asdf1234!!')
    # app.run(threaded=True, host='0.0.0.0', ssl_context=ssl_context)
    app.run(threaded=True, host='0.0.0.0', ssl_context='adhoc')
    # app.run(host='0.0.0.0')


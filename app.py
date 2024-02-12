from api.routes import app
from utils import set_env

set_env.set_env_variables()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=8000, threaded=True)

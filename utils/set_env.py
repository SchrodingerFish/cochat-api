# set_env.py
import os

env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')


def set_env_variables():
    with open(env_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip() and '=' in line:  # ignore empty lines and lines without '='
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

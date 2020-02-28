1. Install Python 3.6 or higher.
2. Create Virtual Environment (replace X with ur version):
```shell script
virtualenv --python=python3.X venv
```
Alternative if above doesn't work:
```shell script
pip3.X install virtualenv
python3.X -m virtualenv venv
```
3. Activate Virtual Environment:
```shell script
. venv/bin/activate
```
4. Install requirements:
```shell script
pip install -r pip_requirements.txt
```

5. Migrate applications:
```shell script
./manage.py makemigrations
./manage.py migrate
```

6. Run server (default port is 8000):
```shell script
./manage.py runserver [port]
```

Open http://127.0.0.1:[port] in your browser.

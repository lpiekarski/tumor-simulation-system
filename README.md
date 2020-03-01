## Installation
1. Install Python 3.6 or higher.
2. Create Virtual Environment (replace X with your version):
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

## Google reCAPTCHA site registration
1. Visit link https://www.google.com/recaptcha/, look at the top right corner you will see Get reCAPTCHA link, click on it.

2. Scroll down to Register a new site.

3. Choose the type of reCAPTCHA: reCAPTCHA V2
Enter your domain in Domains setting. In case, you want to test on your localhost, enter in 127.0.0.1

4. check Accept the reCAPTCHA Terms of Service and click Register button

5. Once you have clicked on the Register button, Google will generate two keys:  Site Key and Secret Key. Now log into your site -> Click on Appearance -> Theme Options -> Sign Up, Sign In, Review -> Using the above keys to complete all settings there.

6. Edit file `settings\settings_local.py` - Replace `GOOGLE_RECAPTCHA_SECRET_KEY` and `GOOGLE_RECAPTCHA_PUBLIC_KEY` values with the values generated for your site.

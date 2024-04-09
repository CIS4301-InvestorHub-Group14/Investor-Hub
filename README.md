# Investor-Hub

# Requirements
* Python 3.12
* Django 5.0.4

# To Run
`python manage.py runserver`

Make sure you change the DATABASE 'USER' and 'PASSWORD' to your own respective Oracle DB credentials so there aren't any conflicts. You can find the DATABASE section in settings.py. If the console prompts you to migrate, do it.

NOTE: You will need to be connected to the GatorLink VPN to access the database, otherwise running the project will cause errors.

# Admin Page

To create a superuser: `python manage.py createsuperuser` and follow instructions

# Anaconda

If you want to use Anaconda to setup your virtual environment/interpreter. You can do this by installing it here[https://www.anaconda.com/] by setting up the following commands:
`conda create --name myenv python=3.12`
Activate the virtual environment with `conda activate myenv`

If you are using PyCharm, you can create a Django project where you can select your own python interpreter.

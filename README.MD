## Steps to get your project started:

* Create a new repo in your chohort's github org:

  * `bangazon_workforce_mgt_<your-team-name>`

* Clone this repo and cd into it
* Change your local repo's remote repo:

  * `git remote remove origin`
  * `git remote add origin <url of your team's repo>`

* Create your virtual environment:

  * `python -m venv workforceenv`
  * `source ./workforceenv/bin/activate`

* Install the app's dependencies:

  * `pip install -r requirements.txt`

* Build your database from the existing models:

  * `python manage.py makemigrations hrapp`
  * `python manage.py migrate`

* create a superuser for your local version of the app:

  * pyman createsuperuser <your_username>

* Populate your database with initial data from fixtures files: (_NOTE: every time you run this it will remove exisiting data and repopulate the tables_)

  * `python manage.py loaddata computers`
  * `python manage.py loaddata users`

* Fire up your dev server and get to work!

  * `python manage.py runserver`

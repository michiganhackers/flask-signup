MH Attendance 
======

This repository contains the source code for [Michigan Hackers](http://wwww.michiganhackers.org)' attendance app.

The app uses Twilio to check-in attendees to MH events. It comes with an admin interface so MHers can set-up event-based check-in "sessions", an API for querying and a conversation framework so we can register new members quickly and get to know more about them.

Installation
===
Getting started is easy. We suggest installing [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/). Once you've got that taken care of, take the following steps in your terminal:

1) Create a virtual environment where the app's dependencies will reside
```sh
mkvirtualenv mh-attendance-venv
```
You should now be working in this virtual environment. To check, make sure your terminal shows the following:
```sh
(mh-attendance-venv)username$
```
If not, simply type ```workon mh-attendance-venv```

2) After you've created your env, CD to the directory you want the app to be in and clone the Git repo for the app
```sh
cd Developer
git clone https://github.com/michiganhackers/mh-attendance.git
```
3) Navigate to the app
```sh
cd mh-attendance
```
4) Pip install of the project dependencies by running the following:
```sh
pip install -r requirements/dev.txt
```

5) Set-up your environment variables. Refer to Envs/.env-example for an example. You'll need .env-dev file to get rolling.

6) Set up the development database. To do so, you'll have to apply all of the migrations created thus far.
```sh
python manage.py db upgrade
```

7) You'll need an smtp server set-up for email handling (or use [Gmail credentials](http://flask.pocoo.org/snippets/85/)). Mail is handled by [flask-mail](https://pythonhosted.org/flask-mail/). If you're on a Mac, the smtp server postfix should come built in. You can start it by running:
```sh
sudo postfix start
```

8) Download [ngrok](https://ngrok.com/download) to test your Twilio app while running a localserver. An excellent guide on doing so can be found [here](https://www.twilio.com/blog/2013/10/test-your-webhooks-locally-with-ngrok.html). Essentially, set-up your Twilio messages URL to point to your Ngrok tunnel url.

Usage
===

To run the tests with coverage:
```sh
python manage.py test --coverage
```

To start your local development server, run:
```sh
python manage.py deploy
```
Navigate to 127.0.0.1:5000 and you should see the app.

Next, start up Ngrok so that Twilio messages can be routed properly.
```sh
/path/to/ngrok 5000
```
OR
```sh
/path/to/ngrok -authtoken="authtoken" -subdomain="specificy subdomain" 5000
```
Navigate your browser to the url it lists in your terminal, and there you have it! 
Make sure your Twilio messages url matches your ngrok url.

Current Version
===
0.01

Tech
===
mh-attendance uses a number of open source projects to work properly:

# FLASK REST API

_README under construction._
_TODO: fill in more helpful `README`._

This project contains files created while following the Pluralsight [Python Flask Rest API](https://app.pluralsight.com/library/courses/python-flask-rest-api/table-of-contents) course.  From the description:

> Flask is rapidly growing in popularity due to its ease of use. This course will teach you how to build a REST API using Flask, including how to use all the different HTTP methods, connect Flask to a database, and add authentication to your APIs.

**WARNING:** Do not use in production.  A password encoding / decoding library is not included in this project, which uses plain text password storage.

**Run the App**:
```bash
$ python app.py
```

```bash
// To create db table from Python intepreter:
>>> from book_model import *
>>> db.create_all()

>>> from user_model import *
>>> db.create_all()
```

To set this project up locally:

```bash
# create new virtual environment, if needed
$ virtualenv venv -p $(which python3)

# activate virtual environment
$ source venv/bin/activate

# install project dependencies
$ pip install -r requirements.txt

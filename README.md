# Women Who Code - CONNECT Conference Workshop

## Setup
The following steps will help you setup a development environment.

### Install pip
```
$ sudo easy_install pip
```

### Install virtualenv
```
$ sudo pip install virtualenv
```

### Activate virtual environment
```
$ virtualenv venv
$ source venv/bin/activate
```

### install python packages
```
$ pip install -r requirements.txt
```

## Running the server
```
python manage.py runserver
```
This will launch a server on localhost at port 5000. Hit up the index page at ```http://localhost:5000/```


## Testing
### Run unit tests
```
$ pytest -v -s tests/unit/utils/test_utils.py
```
# Women Who Codes - CONNECT Conference Workshop

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
$ pip install -r requirements.py
```


## Testing
### Run unit tests
```
$ pytest -v -s tests/unit/utils/test_utils.py
```



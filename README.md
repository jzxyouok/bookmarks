# bookmarks

A bookmark app built with django.

## Quick Start

### Build

You can build with [pipenv](https://github.com/pypa/pipenv)

``` bash
git clone https://github.com/alphardex/bookmarks
cd bookmarks
pipenv install --dev
pipenv shell
```

### Run

``` bash
python manage.py runserver_plus
```

During local development, ensure DEBUG = True

### Test

``` bash
python manage.py test
```

### Deploy to Heroku

Ensure DEBUG = False

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/alphardex/bookmarks)

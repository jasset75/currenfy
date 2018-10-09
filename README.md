# currenfy
Currency Conversion

## Install recipe

* Download git repository
```sh
git clone https://github.com/jasset75/currenfy.git
cd currenfy
pip install .
```
> this will install required python packages.
> virtualenv recommended.


* Installing django app
```sh
git clone https://github.com/jasset75/currenfy.git
cd currenfy
cp local_settings.py settings.py
pip install .
```
> change `Debug=False
> change `SECRET_KEY` to a production enviroment key


* Running tests
```sh
python manage.py migrate
python manage.py test
```



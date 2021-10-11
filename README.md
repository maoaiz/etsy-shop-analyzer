# etsy-shop-analyzer

This project read the data from some Etsy shops and shows the top 5 meaningful terms for each one.


## Instalation

1. Install python +3.8 and create an environment.

2. Clone the project:
```shell
git clone https://github.com/maoaiz/etsy-shop-analyzer.git
```

3. Install the dependencies:

```shell
pip install -r requirements.txt
```

4. Configure your var environments creating a file called `.env`, you can use the `sample.env` file.

5. Migrate the database:

```shell
python manage.py migrate
```

6. Create a superuser (optional, to check the data in the django admin):

```shell
python manage.py createsuperuser
```

7. Sync the data from Etsy (please be sure you already configured an Etsy app and you have the credentials):

```shell
python manage.py sync_data
```

8. Run your server and check your browser. Please wait until sync_data finish.

```shell
python manage.py runserver
```


## Tests
To run the test install the dev dependencies and run `pytest`:

```shell
pip install -r requirements-dev.txt
pytest
# or with reports:
pytest --cov-report term-missing
```

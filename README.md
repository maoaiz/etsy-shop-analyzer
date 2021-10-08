# etsy-shop-analyzer

This project read the data from some Etsy shops and shows the top 5 meaningful terms for each one.


## Instalation

1. Install python +3.8 and create an environment

2. Install the dependencies:

```shell
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

3. Configure your var environments creating a file called `.env`, you can use the `sample.env` file.

4. Migrate the database:

```shell
python manage.py migrate
```

5. Create a superuser (optional):

```shell
python manage.py createsuperuser
```

6. Sync the data from Etsy (please be sure you already configured an Etsy app and you have the credentials):

```shell
python manage.py sync_data
```

7. Run your server and check your browser. Please wait until sync_data finish.

```shell
python manage.py runserver
```


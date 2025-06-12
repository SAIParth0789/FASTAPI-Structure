### How to Setup the project

#### Steps.
* Change the `project_name` package or folder with your project name
* Replace project_name with your project name in the `imports`
* Setup Your .env file at `env/.env`
* In `.env` file change your Database url(Currently mysql container is using)
* Inside the `docker compose` file if you don't need the database remove the database service
* Change the `config.py` according to the `.env` file
* If you need to see the logs all the logs save into the logs folder.
* For testing the route you can visit to the `Swagger` or just create your `curl` inside the test_main.http file and run and check the response.

 ---

#### For Update the table columns use this commands

Set up Alembic:
* Initialize Alembic:
Run the following command in the root of your project to initialize Alembic:
```bash
alembic init alembic
```
* alembic.ini:
Update the `sqlalchemy.url` in alembic.ini to match your database URL.
```bash
sqlalchemy.url = mysql+pymysql://{details}
```
---
Change the table in the code, after that `docker-compose up` run this command:
```bash
docker-compose run backend alembic revision --autogenerate -m "remove test columns"
```
###### Update Table Command:
``` bash
docker-compose run backend alembic upgrade head
```
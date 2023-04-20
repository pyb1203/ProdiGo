# ProdiGo
ProdiGo could be interpreted as a combination of "product" and "amigo," which implies a friendly, helpful assistant for finding right products. It is Product Recommendation Engine.

# Steps to setup this project (All these steps are for windows system)

1. First download and install python 3.11 on your local system from its official website https://www.python.org/downloads/.

2. Then, open the terminal where you want to clone this repository on your local system and clone it using git clone command.

git clone https://github.com/pyb1203/ProdiGo.git

3. Now, create a virtual environment outside this project folder by executing this command from the terminal.

py -m venv <venv_name>

4. Activate, the virtual environment by command.

<venv_name>\Scripts\activate

5. Then, go inside this project directory by using cd command.

cd ProdiGo

6. Now, install the requirements by running this command.

pip install -r requirements.txt

7. Now, download the erlang and rabbitmq server from their respective websites https://www.erlang.org/downloads and https://www.rabbitmq.com/download.html and follow the instructions there to install them.

8. Then, run the migrate command to migrate the migrations to the database.

py manage.py migrate

9. Now, create the superuser by executing command.

py manage.py createsuperuser

(provide the username, email and password in this)

10. Then, run celery worker and beat in two separarte terminals using commands.

celery -A ProdiGo worker -P gevent -l info

celery -A ProdiGo beat -l info

10. Now the run the django server in another separate terminal different from terminals running celery worker and beat.

py manage.py runserver

11. Now, open a another separate terminal to run the two scripts file to create random products and place random orders.

py manage.py create_products_script

py manage.py place_orders_script

12. Finally, download and install the postman from its official website https://www.postman.com/downloads/ and import my postman colection which is the json file in the postman to the test the APIs.

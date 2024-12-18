<!-- ABOUT THE PROJECT -->
## About The Project

A social-media application implemented with Django. 


<!-- GETTING STARTED -->
## Getting Started

To get this repository, run the following command inside your git enabled terminal.
  ```sh
  git clone https://github.com/mirrzad/Django-Blog
  ```

<!-- Setup -->
## Setup

in order to run and use the application with docker-compose, all you have to do is to run the 
command bellow in the same directory of docker-compose.yml file.

 ```sh
  docker-compose up --build
  ```
then run the following command to apply database migrations.

 ```sh
  docker-compose exec backend sh -c "python manage.py migrate"
  ```

Now open the url below and you can reach the index page of the app.

* http://127.0.0.1:8000


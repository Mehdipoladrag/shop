
<p align="center">
  <a>
    <img src="https://skillicons.dev/icons?i=python,django,postgresql,redis,docker,rabbitmq,postman,css,js,html&=3" />
  </a>
</p>
<p align="center">
  <a href="mailto:mehdipoladrag1382@gmail.com">
    <img src="https://skillicons.dev/icons?i=gmail&=1" />
  </a>
  <a href="https://www.linkedin.com/in/mehdi-poladrag">
    <img src="https://skillicons.dev/icons?i=linkedin&=1" />
  </a>
  <a href="https://instagram.com/mehdipoladrag">
    <img src="https://skillicons.dev/icons?i=instagram&=1" />
  </a>
</p>

## Table of Contents
- [Installation](#installation)
- [Usage](#Usage)
- [Project](#Project).
- [Technologies](#Technologies)
- [Refrence](#Refrence)

## Installation
1. Clone the repository:
```bash
 git clone https://github.com/Mehdipoladrag/shop.git
```

2. Create and start the containers:
```
 docker-compose up -d --build
```

3. Start the containers:
```bash
 docker-compose up -d
```

4. Stop and remove the containers:
```bash
 docker-compose down
```


## usage

### How to use a shell for django project

##### How to Makemigrations
1. ```bash
   docker-compose exec web sh -c "python manage.py makemigrations"
   ```
##### How to Migrate
2. ```bash
   docker-compose exec web sh -c "python manage.py migrate"
   ```
##### How to Createsuperuser
3. ```bash
   docker-compose exec web sh -c "python manage.py createsuperuser"
   ```


## Project

#### User Section
This project was written by me to showcase my skills on GitHub as part of my resume. This project is a shopping platform where users can register and log in. They can also make purchases and add products to their shopping cart.

Users can complete their profile to gain full access to their information for purchasing products. Once the user finalizes their purchase, they receive a tracking code.

#### Admin Section
An admin panel has been created that allows the admin to have specific access permissions. The admin can manage information using Celery Beat to run tasks for each section, which are executed automatically.
The superuser can easily access all information, although users can be restricted in certain cases.

#### REST Framework Section
A separate folder named api/v1/ has been created for each app, categorizing all the site's APIs and separating them for each app. For quick access during testing, I have left it open to everyone, but I will restrict access in the future.

#### Database Section
I have created a separate panel from Docker Hub for this project, making the database accessible on a completely separate port but with restricted access.

### Celery Section 
Use Celery to manage the database, allowing us to handle and clean up excess data efficiently. Celery Beat helps us schedule tasks, enabling time-based management of these tasks. Specifically, we add the necessary arguments for a task through the admin panel, and the task is executed automatically. The results of the task can be monitored using the Flower tool. In summary, we utilize Celery for effective database management.

## Technologies
Project is created with:
* Python,Django,DjangoRest,CeleryBeat,Celery,Jwt
* Postgresql,Pgadmin,Redis,RabbitMq,Flower
* Docker,Postman
* Html,Css,Js
* Swagger
* flake8,black,pylint,pycodestyle



## Refrence
* See Django  [Reference](https://www.djangoproject.com/)
* See Django RestFramework [Reference](https://www.django-rest-framework.org/)
* See Celery Beat [Reference](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html)
* See DockerHub [Refernce](https://hub.docker.com/) 



	





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
- [Frontend](#Frontend)
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


## Frontend

The user interface is a React (Vite) app in `frontend/`: the shop at `/` and the admin
panel at `/panel`. Django only serves the API, `/admin/` and the media and static files.

```bash
cd frontend
npm install
npm run dev        # http://127.0.0.1:5173, proxies the API to Django on port 8001
```

See [frontend/README.md](frontend/README.md) for the pages and the build, and
[docs/design-colors.md](docs/design-colors.md) for the color palette. The IRANYekan font is
licensed and not included; see `shop/static/assets/fonts/iranyekan/README.md`.

### Run the backend without Docker
Needs Python 3.12 (or 3.11), PostgreSQL and Redis. Use the same database values as
`docker-compose.yml` (user `root`, password `root`, database `shop_db`).

```bash
cd shop
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt   # skip djangorestframework-jwt: it is unused and conflicts with PyJWT
export DEBUG=True PG_HOST=127.0.0.1 REDIS_URL=redis://127.0.0.1:6379/1
python manage.py migrate
python manage.py runserver 8001
```

### Tests
```bash
cd shop && python -m pytest
```

## Demo data

Two management commands fill an empty TechShop with demo content. Run them from the `shop/` folder
with the same environment as the dev server; both are safe to run repeatedly.

```bash
python manage.py seed_demo_catalog              # the 2023+ product catalog
python manage.py seed_demo_catalog --prune-old  # same, and also remove the previous seed's products
python manage.py seed_demo_blog                 # three blog posts by the editor account "techshop_editor"
```

**`seed_demo_catalog`** creates about 40 products released in 2023 or later: iPhone 15 to 17 (including
16e and Air), Galaxy S24 Ultra and S25 Ultra, iPad Pro (M4 and M5), iPad Air, iPad mini and iPad (A16),
and AirPods Pro 2 and 3, AirPods 4 and AirPods Max. The categories are phones, tablets and headphones
(`mobile`, `tablet`, `audio`) and the brands are Apple and Samsung. The newest models are listed first.

- Model names and specifications follow the manufacturers' public information; every product links to
  the official page. Prices (in toman), stock, discounts, ratings and delivery times are **sample data**,
  and the product notice says so.
- The pictures are **original illustrations, not photographs**. They are drawn by
  `scripts/generate_demo_art.py` (Pillow only) into `shop/static/assets/img/product_img/new/`; see the
  README in that folder. Regenerate them with `python scripts/generate_demo_art.py`, or replace any file
  with a real photo by keeping the same file name (check the photo's license first). The seed copies the
  pictures to `MEDIA_ROOT/images/demo-catalog/`.
- Existing slugs are skipped, so a second run creates nothing. The seed never deletes anything unless
  you pass `--prune-old`, which removes only the products created by the previous version of this seed
  (iPhone 12/13/14, Galaxy A52 and S21 Ultra, POCO X4 Pro, PlayStation 5) together with their pictures.
  Categories, brands, other products and users are left alone.

**`seed_demo_blog`** adds three Persian blog posts with local images. An editor account created under the
shop's old name is renamed to `techshop_editor` instead of being duplicated.

## Project

#### User Section
This project was written by me to showcase my skills on GitHub as part of my resume. This project is a shopping platform where users can register and log in. They can also make purchases and add products to their shopping cart. The pages are built in React and talk to the REST API with a session login (CSRF protected).

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
* React,Vite,Html,Css,Js
* Swagger
* flake8,black,pylint,pycodestyle



## Refrence
* See Django  [Reference](https://www.djangoproject.com/)
* See Django RestFramework [Reference](https://www.django-rest-framework.org/)
* See Celery Beat [Reference](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html)
* See DockerHub [Refernce](https://hub.docker.com/) 



	




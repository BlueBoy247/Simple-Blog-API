# Simple Blog API
[繁體中文](./README.md) | English

## Architecture
```
blog-api/
├── app/
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── blog.py
│   │   └── login.py
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
├── sql/
│   └── init.sql
├── .dockerignore
├── .env.template
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
└── run.py
```

## API Description
### login
- `POST /login` : User login. The parameters are `email` and `password`, representing the user's email address and password, respectively. After successful login, a JWT which expires in 30 days will be returned. The JWT contains user's email, token issuer, expiration time, and not before.

### blog
- `GET /blog/all` : List all posts (title, content, tags).
- `GET /blog/page/{page}` : List posts by page (title, content, tags). The number of posts per page can be controlled with the `pagesize` query parameter, the default value is 10.
- `POST /blog/create` : Create a new post. The JWT will be validated, and if the validation fails, a HTTP 401 status will be returned. The request body must be JSON containing `title` (string), `content` (string), and `tags` (array of strings), representing the post's title, content, and tags, respectively.

## How to Run
### Local
#### Requirements
* Python 3.10+
* MySQL 8.0+

#### FastAPI
1. Install dependencies
```bash
pip install -r requirements.txt
```
2. Run the application
```bash
uvicorn app:app --reload
```
After the backend is running, the API service will run on [http://127.0.0.1:8000](http://127.0.0.1:8000), and you can access it through [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to view the Swagger UI documentation.

#### MySQL
1. Open MySQL Command Line and log in.
2. Execute SQL Script.
```bash
source D://Simple-Blog-API/sql/init.sql
```
> Note: `D://Simple-Blog-API/sql/init.sql` should be replaced with the actual absolute path of `init.sql`.

### Docker
Start Docker Compose containers.
```bash
docker compose up -d --build
```
After the containers are running, the API service will run on [http://localhost:8000](http://localhost:8000), and you can access it through [http://localhost:8000/docs](http://localhost:8000/docs) to view the Swagger UI documentation. Besides, MySQL service will run on [http://localhost:3307](http://localhost:3307).

## Environment Variables
This service requires the following environment variables:
- `DATABASE_URL` : MySQL database connection string.
- `JWT_ISSUER` : JWT issuer (optional，if not set, the default value is `fastapi`).
- `SECRET_KEY` : JWT secret key (optional，if not set, it will be automatically generated when the service starts).

### Run on Local
Please copy `.env.template` file and rename it to `.env`, and then modify the values of the above environment variables in the `.env` file.

### Run on Docker
Please modify the `environment` field in `docker-compose.yml` file. The `DATABASE_URL` has been set, so if no need to change, it is recommended not to change to avoid the API service cannot connect to the database.

Discount Service
================
![Discount](discount-header.png)

### Future Improvements
- permission classes
- brand dashboard apis
  - discount codes list
  - filter on discount fields (user, redeemed, ...)
- schema and models unit tests

---

Deployment
-----------------

### Run App
```shell
docker-compose up
```
> Documentation URL: [http://localhost:8080/docs](http://localhost:8080/docs)

### Stop App
```shell
docker-compose down
```

### Run tests
```shell
docker-compose run app bash scripts/run_tests.sh
```
---

Local development
-----------------

### Server

To run the server: `./scripts/local_server.sh`

### Run tests

To run the test: `./scripts/run_tests.sh`

### Migrations

*Run migrations*

```shell
alembic upgrade head
```

*Autogenerate migration*

Alembic can autogenerate the migration file by comparing your SQLAlchemy models and the migration files!

```bash
alembic revision --autogenerate -m "description of migration"
```
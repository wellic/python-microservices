# Sources:

- https://www.freecodecamp.org/news/python-microservices-course/
- https://www.youtube.com/watch?v=0iB5IPoTDts&feature=youtu.be
- https://github.com/scalablescripts/python-microservices

Thanks authors.

# First up
- up rabbitmq and add vhost http://localhost:15672/#/vhosts (user/password)

```
cd rabbit
docker-compose up -d
```

- Init db in `admin_backend` and `main_backend` container:
```
cd admin
docker-compose up -d
docker exec -it admin_backend_1 python manage.py migrate
```

- Init db in `admin_backend` and `main_backend` container:
cd main
docker-compose up -d
docker exec -it main_backend_1 python manager.py db upgrade
```

- restart all
```
./_down_all.sh;./_up_all.sh
```


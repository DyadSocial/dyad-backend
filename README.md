# dyad-backend

### Docker Compose for creating the images
```bash
sudo docker-compose run web django-admin {name} .
sudo chown -R $USER:$USER .
```
Change Django settings to postgres defined in ./docker-compose.yml:
Edit: ./{name}/settings.py
```py
# settings.py
DATABASE = {
  'default': {
     'ENGINE': 'django.db.backends.postgresql',
     'NAME': 'postgres',
     'USER': 'postgres',
     'PASSWORD': 'postgres',
     'HOST': 'db',
     'PORT': 5432,
  }
}
```

### Run Docker Compose
```bash
# Starting
docker-compose up

# Ending
docker-compose down
```

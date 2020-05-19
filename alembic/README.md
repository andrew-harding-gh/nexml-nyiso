# Local setup
If needed, create a local postgres database for first time setup (linux):
```
sudo -u postgres createuser -D -A -P elec
sudo -u postgres createdb -O elec elec_db
```

To allow our db url to be built, set/export the following local environmental variables; defaults to values in above commands:
```
 DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
```
 
Now, within our project venv, bring the db up to speed to our latest revision
```
alembic upgrade head
```


# Development
 
### ORM
lives in `model.py`

### Revisioning
easy way to revision is `alembic revision --autogenerate -m "{Your Message}"`.

This takes into account the current state of the connected db and the ORM file's current state

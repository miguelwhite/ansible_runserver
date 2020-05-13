# ansible_runserver
A server endpoint that runs predfined playbooks.

## Development

### Docker
Build the images in the docker-compose.yaml file
```
docker-compose build
```

Start the application stack
```
docker-compose up
```

The application should now be reachable at http://localhost:8000

### Local Dev
Use the local settings module in `ansible_runserver/settings/local
```
export DJANGO_SETTINGS_MODULE=ansible_runserver.settings.local
```

Initialize your local db
```
./manage.py makemigrations
./manage.py migrate
```

Run the server
```
./manage.py runserver
```

The application should now be reachable at http://localhost:8000

#### Testing
Tests are located in the individual app subdirectories. Ex: `run/tests/test_mytest.py`

You can run tests with the following command. If `app_dir` is not specified then it will run all tests.
```
./manage.py tests [app_dir]
```

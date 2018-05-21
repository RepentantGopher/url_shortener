One more URL shortener
==========================

To run this app in docker you need to install docker-compose:
```bash
    pip install docker-compose
```
then just run it from root
```bash
    docker-compose up
```

To run this app on local system you must have installed redis database in your system 
```bash
    pip install -r requirements.txt
    PYTHONPATH=. python app/main.py
```

Don't forget to change URL_ROOT environment variable if changing BIND_HOST or BIND_PORT!

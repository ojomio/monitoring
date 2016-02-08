
    pip install -r  ./requirements.txt
    python3 ./manage.py syncdb
    python3 ./manage.py runserver 0.0.0.0:8000&
    python3 ./query_devices.py

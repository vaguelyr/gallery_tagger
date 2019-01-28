#!/bin/bash

/usr/local/bin/gunicorn -w 4 myapp:app 

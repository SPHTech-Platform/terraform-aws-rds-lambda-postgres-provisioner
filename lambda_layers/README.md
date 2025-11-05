# Steps to create lambda layer of psycopg2 module

1) Create folder, psycopg2_layer

2) python3.12 -m venv .myenv

3) source .myenv/bin/activate

4) Create folder python and install

pip install \
  --platform manylinux2014_x86_64 \
  --target ./python \
  --implementation cp \
  --python-version 3.12 \
  --only-binary=:all: \
  psycopg2-binary

5) zip -r psycopg2_python3.12.zip python

6) Add zip file in this folder (/lambda_layer)

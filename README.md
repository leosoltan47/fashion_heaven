# Setting up dev environment

Get the repo
```bash
git clone https://github.com/leosoltan47/fashion_heaven.git

Create a virtual env
```
python -m venv .venv

Activate virtual env on bash
```bash
source .venv/bin/activate
```
Activate virtual env on Windows
```cmd
.venv\Scripts\activate
```
Install dependencies into virtualenv
```
python -m pip install -r requirements.txt
python manage.py collectstatic
```

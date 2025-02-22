# Setting up dev environment

Get the repo
```bash
git clone https://github.com/leosoltan47/fashion_heaven.git
```
Create a virtual environment
```bash
python -m venv .venv
```
Activate virtual environment on bash
```bash
source .venv/bin/activate
```
Activate virtual virtual environment on cmd
```bash
.venv\Scripts\activate
```
Install dependencies into virtual environment
```bash
python -m pip install -r requirements.txt
python manage.py collectstatic
```

## Development Environment
Its super easy to set up our development environment

## Installing GNU/Linux requirements
Install `python-pip`, `python-dev` and `virtualenvwrapper`
```bash
sudo apt-get install git binutils libpq-dev python-dev python-setuptools
sudo apt-get install memcached python-pip sqlite3
sudo pip install virtualenvwrapper
```

## Clone the repository
You can clone it directly from
[TitliSarkar/TSR3DSystem](https://github.com/TitliSarkar/TSR3DSystem)
```bash
git clone https://github.com/TitliSarkar/TSR3DSystem.git
```

## Setup development environment
First, some initialization steps. Most of this only needs to be done
one time. You will want to add the command to source
`/usr/local/bin/virtualenvwrapper.sh` to your shell startup file
(`.bashrc` or `.zshrc`) changing the path to `virtualenvwrapper.sh`
depending on where it was installed by `pip`.
```bash
export WORKON_HOME=~/Envs
mkdir -p $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh
```
Lets create a virtual environment for our project
```bash
mkvirtualenv protein
workon protein
```

## Install requirements
All the requirements are mentioned in the file `requirements.txt`.
```bash
pip install -r requirements.txt
```

## Local settings
Copy the `local-settings-development.py` from `conffiles` to `protein/protein`
directory.
```bash
cp conffiles/local-settings-development.py protein/protien/local_settings.py
```
Also in `protein/protein/local_settings.py` set `SESSION_COOKIE_SECURE` as
`False`. This disables SSL cookies.

## Setup database
App development is done using `sqlite` database.
Assuming you are inside the directory where `manage.py` also present
```bash
python manage.py makemigrations
python manage.py migrate
```
Collect all the static files for fast serving
```bash
python manage.py collectstatic
```

## Run server
```bash
python manage.py runserver
```

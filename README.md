# fs-curl-directory
CGI script for Freeswitch mod_xml_curl directory binding from Mysql database.

# Mac requirements
brew install mysql-connector-odbc

# Debian requirements
aptitude install python-pip python-dev build-essential libxml2-dev \
libxslt1-dev libmyodbc unixODBC unixODBC-dev supervisor

pip install virtualenv virtualenvwrapper
pip install --upgrade pip

# Setup virtualenvwrapper in ~/.bashrc.
printf '\n%s\n%s\n%s' '# virtualenv' 'export WORKON_HOME=~/virtualenvs' \
'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc

# Enable the virtual environment.
source ~/.bashrc
mkdir -p $WORKON_HOME
mkvirtualenv freeswitch

pip install -r requirements.txt

## configure uwsgi with cgi plugin
http://uwsgi-docs.readthedocs.org/en/latest/CGI.html

curl http://uwsgi.it/install | bash -s cgi /home/webuser/uwsgi
cd uwsgi_latest_from_installer/
python uwsgiconfig.py --plugin plugins/cgi

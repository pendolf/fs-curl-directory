# fs-curl-directory
CGI script for Freeswitch mod_xml_curl directory binding from Mysql database.


## Requirements
```shell
aptitude install python-pip python-dev build-essential libxml2-dev freeswitch-mod-xml-curl \
libxslt1-dev libmyodbc unixODBC unixODBC-dev supervisor
```

```shell
pip install virtualenv virtualenvwrapper
pip install --upgrade pip
```

Setup virtualenvwrapper in ~/.bashrc.
```shell
printf '\n%s\n%s\n%s' '# virtualenv' 'export WORKON_HOME=~/virtualenvs' \
'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc
```

Enable the virtual environment.
```shell
source ~/.bashrc
mkdir -p $WORKON_HOME
mkvirtualenv freeswitch
pip install -r requirements.txt
```

[Configure uwsgi with cgi plugin](http://uwsgi-docs.readthedocs.org/en/latest/CGI.html)

```shell
curl http://uwsgi.it/install | bash -s cgi /tmp/uwsgi
uwsgi --build-plugin uwsgi_latest_from_installer/plugins/cgi
mkdir -p /usr/local/lib/uWSGI-2.0.11.1/plugins
cp /home/webuser/cgi_plugin.so /usr/local/lib/uWSGI-2.0.11.1/plugins
ln -sf /home/webuser/fs-curl-directory/fs_curl.conf /etc/supervisor/conf.d/fs_curl.conf
```

Check url
```shell
curl -D- http://127.0.0.1:9011/directories.py -d 'user=pendolfNambaTaxi&domain=default'
```
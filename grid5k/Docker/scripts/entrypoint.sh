#!/bin/bash

echo "Starting DB"
sudo service mariadb start

echo "Building DB"

mysql -h localhost -u root -pr00t -e "CREATE DATABASE deploy3;" 

mysql -h localhost -u root -pr00t -e "GRANT select, insert, update, delete, create, drop, alter, create temporary tables, lock tables ON deploy3.* TO 'deploy'@'kadeploy.site.grid5000.fr';"

echo "Done!"

echo "Starting kadeploy ... "

service kadeploy start

sleep infinity
#! /bin/bash

docker-compose -f lab1.yml down

docker-compose -f lab1.yml up -d

echo "If you have error -> Access Denied for User 'root'@'localhost' (using password: YES)"
echo "Increase sleep value. Current value is 30 sec"
echo ""
echo "Waiting for databases..."
sleep 30

echo 'Creating database...'
docker exec -i mariadb mysql -uroot -ppassword mysql < copier/lab1.sql
echo 'Records has been added'

echo 'Running script...'
docker exec -i python python3 lab1.py
echo 'End'

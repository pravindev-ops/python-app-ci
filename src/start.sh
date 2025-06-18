#!/bin/bash
set -e

export DB_USER="root"
export DB_PASSWORD=$(cat /var/secrets/MYSQL_ROOT_PASSWORD)
export DB_NAME=$(cat /var/secrets/MYSQL_DATABASE)
export DB_HOST="mysql-service.app"

exec python app.py

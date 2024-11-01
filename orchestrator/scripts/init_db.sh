export AIRFLOW_HOME=$(pwd)/airflow_home

# Initialize Airflow database if not already done
echo "Initializing database..."
airflow db migrate

echo "Creating default admin user..."
airflow users create \
    --username admin \
    --password admin \
    --firstname admin \
    --lastname user \
    --role Admin \
    --email admin@example.com
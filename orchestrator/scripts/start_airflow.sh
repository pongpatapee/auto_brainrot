#!/bin/bash

# Define the Airflow home directory (optional)
export AIRFLOW_HOME=$(pwd)/airflow_home

# Function to stop all Airflow processes
cleanup() {
    echo "Stopping Airflow processes..."
    pkill -f "airflow webserver"
    pkill -f "airflow scheduler"
    echo "All Airflow processes stopped."
    exit 0
}

# Trap SIGINT (CTRL+C) and SIGTERM signals to run the cleanup function
trap cleanup SIGINT SIGTERM

# Start the Airflow scheduler in the background

airflow scheduler > /dev/null 2>&1 &
echo "Succesfully launched the airflow scheduler in the background..."

# Start the Airflow webserver in the background
airflow webserver -p 8080 > /dev/null 2>&1 &
echo "Succesfully launched the airflow webserver (http://localhost:8080) in the background..."

echo "write "c" then ENTER to shut everything down"

# Monitor for the input 'c' to stop the processes
while true; do
    read -r input
    if [ "$input" == "c" ]; then
        cleanup
    fi
done
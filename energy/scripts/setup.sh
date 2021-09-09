#!/bin/bash

# Start of script
SECONDS=0
printf "Starting creation of workspace, loading of datasets, creation of environments and clusters..."
printf "\n"
sleep 2

# Create resources
printf "Beginning create of workspace, and resources..."
printf "\n"
./createWorkspaceAndSpRbac.sh
sleep 20

# Data prep
printf "Data preparation on local compute..."
printf "\n"
python ~/GithubProjects/azure-automl-timeseries/energy/data-prep/align_dates.py
sleep 5

# Upload datasets, and register them
printf "Uploading datasets and registering them..."
printf "\n"
python datasets.py
sleep 5

# Create compute cluster
printf "Creating cluster..."
printf "\n"
python clusterCreation.py
sleep 5

duration=$SECONDS
printf "$duration seconds elapsed since datasets were uploaded, registered and cluster created.\n"

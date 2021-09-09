#!/bin/bash
#Script to provision a new Azure ML workspace

# Source subscription ID, and prep config file
source sub.env
sub_id=$SUB_ID

# Set the default subscription to MSDN/VS Subscription
#az account set -s 0c6e5df5-ac69-49ab-a6f4-18a10744e316
az account set -s $sub_id

# Start of script
SECONDS=0

# how to get the full list of available SKUS?
number=$[ ( $RANDOM % 10000 ) + 1 ]
resourcegroup='automl'$number
workspacename='automlworkspace'$number
deploymentname='automldeployment'$number
location='westus2'

# Create a resource group
duration=$SECONDS
printf "Starting resource group creation...\n"
printf "$duration seconds elapsed.\n"
az group create --name $resourcegroup --location $location

# Deploy the ARM template
duration=$SECONDS
printf "Starting ARM template deployment...\n"
printf "$duration seconds elapsed.\n"
az deployment group create \
    --name $deploymentname \
    --resource-group $resourcegroup \
    --template-uri "https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/quickstarts/microsoft.machinelearningservices/machine-learning-advanced/azuredeploy.json" \
    --parameters workspaceName=$workspacename \
    location=$location

# Print statements to log
printf -- "------------------------------------------------\n"
printf "Your resource group is called: $resourcegroup \n"
printf "Your location is called: $location \n"
printf "Your AML workspace name is called: $workspacename \n"

# Create config file
# Format of config.json
#{
#    "subscription_id": "0c6e5df5-ac69-49ab-a6f4-18a10744e316",
#    "resource_group": "amlWorkspace6047",
#    "workspace_name": "workspace6047"
#}
configFile='config.json'
printf "{\n" > $configFile
printf "\t \"subscription_id\":\"$sub_id\", \n">> $configFile
printf "\t \"resource_group\":\"$resourcegroup\", \n">> $configFile
printf "\t \"workspace_name\":\"$workspacename\" \n">> $configFile
printf "}\n" >> $configFile

# Generate service principal credentials
credentials=$(az ad sp create-for-rbac --name "sp$resourcegroup" \
	--scopes /subscriptions/$sub_id/resourcegroups/$resourcegroup \
	--role Contributor \
	--sdk-auth)

# Quick capture of credentials
sleep 5
credFile='cred.json'
printf "$credentials" > $credFile
clientID=$(cat $credFile | jq '.clientId')
clientSecret=$(cat $credFile | jq '.clientSecret')
tenantID=$(cat $credFile | jq '.tenantId')
rm $credFile

# Create variables file
env_variable_file='variables.env'
printf "CLIENT_ID=$clientID \n" > $env_variable_file
printf "CLIENT_SECRET=$clientSecret \n" >> $env_variable_file
printf "TENANT_ID=$tenantID \n" >> $env_variable_file
printf "SUB_ID=$sub_id \n" >> $env_variable_file
printf "RESOURCE_GROUP=$resourcegroup \n" >> $env_variable_file
printf "WORKSPACE_NAME=$workspacename \n" >> $env_variable_file

sleep 20 # just to give time for following scripts to access above credentials

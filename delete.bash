#!/bin/bash

# Exit on any error
set -e

# Confirm before deleting the Minikube cluster
echo "This will delete the 'lpdl' Minikube cluster. This operation cannot be undone."
read -p "Are you sure you want to continue? (y/n): " answer

if [[ $answer =~ ^[Yy]$ ]]
then
    echo "Deleting 'lpdl' Minikube cluster..."
    minikube delete -p lpdl
    echo "'lpdl' Minikube cluster has been deleted."
else
    echo "Deletion cancelled."
fi

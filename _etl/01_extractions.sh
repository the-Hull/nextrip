#!/bin/bash
cd "$(dirname "$0")"
pd=$(pwd)
echo "Working dir is $pd"
echo ""
echo "Extractable files are:"
unrar v ./tripadvisor/TripAdvisor_dataset_2015.rar 
unrar e -r ./tripadvisor/TripAdvisor_dataset_2015.rar ./tripadvisor/


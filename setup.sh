#!/bin/bash


function parameter_handler {
   if [ "$1" = "--clean" ] || [ "$1" = "-c" ]; then
      rm -rf artifactory-cpp-ce-7.3.2 | rm -rf volumes | rm .env
      exit
   fi
}

function check_sudo {
   # Check for root
   # It is needed for the artifactory configuration script to complete
   if [ $(id -u) != 0 ]; then
      echo "This script requires root permissions"
      exit
   fi
}


check_sudo

parameter_handler $1

# Unzip artifactory package
tar -xvf jfrog-artifactory-cpp-ce-7.3.2-compose.tar.gz 

# If the mounted directory (./volumes) gets changed, the script directory has to be updated as well because it checks against a literal string
# The following script passes arguemnts to Artifactory's interactive configuration script 
./script.exp

# The hidden env file is required to provide global variables to the docker-compose file
mv artifactory-cpp-ce-7.3.2/.env ./

# Permissions are set manually because the configuration script doesn't do it. 1030 is the artifactory user and group
chown -R 1030:1030 volumes

# The IP address for the websites themselves point to 127.0.1.1 for some reason. 
# Not important to figure out why at the moment, the adress is replaced by the docker host IP found in 'ifconfig'.
sed -i 's/127.0.1.1/172.17.0.1/g' volumes/var/etc/system.yaml
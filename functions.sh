#!/bin/sh

function create_dev_server_image {
  echo "##############################################"
  echo "# Creating application docker image"
  echo "##############################################"
  echo ""
  docker-compose -f dev_scripts/docker-compose.yml build
}

function start_dev_server {
  echo "##############################################"
  echo "# Starting dev server -- http://localhost:9999"
  echo "##############################################"
  echo ""
  docker-compose -f dev_scripts/docker-compose.yml up
}

function create_test_server_image {
  echo "##############################################"
  echo "# Creating application docker image for tests"
  echo "##############################################"
  echo ""
  docker-compose -f dev_scripts/docker-compose.yml -f dev_scripts/docker-compose-tests.yaml build
}

function start_test_server {
  echo "##############################################"
  echo "# Starting tests server "
  echo "##############################################"
  echo ""
  docker-compose -f dev_scripts/docker-compose.yml -f dev_scripts/docker-compose-tests.yaml up --abort-on-container-exit
}

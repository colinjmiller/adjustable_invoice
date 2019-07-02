#!/bin/sh

function create_dev_server_image {
  echo "##############################################"
  echo "# Creating application docker image"
  echo "##############################################"
  echo ""
  docker-compose -f dev-scripts/docker-compose.yml build
}

function start_dev_server {
  echo "##############################################"
  echo "# Starting dev server -- http://localhost:9999"
  echo "##############################################"
  echo ""
  docker-compose -f dev-scripts/docker-compose.yml up
}

create_dev_server_image
start_dev_server

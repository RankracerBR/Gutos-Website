#!/bin/bash

echo ">>Instalando o Docker"

sudo snap install docker         # version 20.10.17, or
sudo apt  install docker.io      # version 20.10.12-0ubuntu4
sudo apt  install podman-docker  # version 3.4.4+ds1-1ubuntu1

echo ">>Instalação Finalizada"

#!/usr/bin/env bash

set -u

_down() {
    cd $1
    docker-compose down
    cd ..
}

set -v

_down main

_down admin

_down rabbit

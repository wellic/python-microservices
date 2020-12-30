#!/usr/bin/env bash

set -u

_up() {
    cd $1
    docker-compose up -d --build
    cd ..
}

set -v

_up rabbit

_up admin

_up main

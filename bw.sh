#!/usr/bin/env bash

set -ex

make check-poetry

poetry run bw $*
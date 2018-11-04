#!/bin/sh
cd .. && rm -rf BagelSpace/src/__pycache__/ && zip -r /tmp/BagelSpace.zip BagelSpace/img/*png BagelSpace/LICENSE BagelSpace/README.md BagelSpace/setup.py BagelSpace/src BagelSpace/sounds/

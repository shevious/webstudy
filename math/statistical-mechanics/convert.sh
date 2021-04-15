#!/bin/bash
for f in *.py; do 2to3 -w $f; done

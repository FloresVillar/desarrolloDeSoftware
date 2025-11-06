!#/usr/bin/env bash

if git diff --quiet HEAD -- modules/simulated_app/;then
    echo "sin cambios"
else 
    echo "cambios regenerando"
    python3 generate_envs.py
    echo "actualiza environments"
fi
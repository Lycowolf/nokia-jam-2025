#!/bin/bash

rm -r the-grind-2025.zip build/
find the-grind-2025 -name "*.pyc" -delete
#mkdir build
#pyxel package the-grind-2025/ the-grind-2025/main.py
#unzip -d build the-grind-2025.pyxapp
#zip -r the-grind-2025.zip index.html build
zip -r the-grind-2025.zip index.html the-grind-2025/assets the-grind-2025/scenario the-grind-2025/screen the-grind-2025/*.py
#zip the-grind-2025.zip the-grind-2025.pyxapp

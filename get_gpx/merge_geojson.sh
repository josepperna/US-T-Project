#!/bin/bash

for entry in `ls geojson`; do
    geojson-merge geojson/$entry/*.geojson > merged_geojson/$entry.geojson
done
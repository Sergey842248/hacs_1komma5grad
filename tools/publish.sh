#!/bin/bash

if [ $# -ne 4 ]; then
  echo "Verwendung: $0 <nextRelease.version> <branch.name> <commits.length> <Date.now()>"
  exit 1
fi

nextReleaseVersion="$1"
branchName="$2"
commitsLength="$3"
timestamp="$4"

mkdir dist

zipCommand="zip ../../dist/einskomma5grad-homeassistant_${nextReleaseVersion}.zip . -r"
echo "Führe folgenden Befehl aus: $zipCommand"

(cd ./custom_components/einskomma5grad && ls -la && $zipCommand)

jsonFile="hacs.json"

if [ -f "$jsonFile" ]; then
  jq ".filename = \"einskomma5grad-homeassistant_${nextReleaseVersion}.zip\"" "$jsonFile" > temp.json
  mv temp.json "$jsonFile"
  echo "Die Eigenschaft 'filename' in '$jsonFile' wurde auf 'einskomma5grad-homeassistant_${nextReleaseVersion}.zip' aktualisiert."
else
  echo "Die Datei '$jsonFile' wurde nicht gefunden."
fi

echo "nextRelease.version: $nextReleaseVersion"
echo "branch.name: $branchName"
echo "commits.length: $commitsLength"
echo "Date.now(): $timestamp"
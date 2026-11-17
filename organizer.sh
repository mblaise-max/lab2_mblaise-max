#!/bin/bash

CSV="grades.csv"
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"

if [ ! -f "$CSV" ]; then
    echo "Error: $CSV not found, nothing to archive."
    exit 1
fi

mkdir -p "$ARCHIVE_DIR"

timestamp=$(date +%Y%m%d-%H%M%S)
new_name="grades_${timestamp}.csv"

mv "$CSV" "$ARCHIVE_DIR/$new_name"
touch "$CSV"

echo "[$timestamp] $CSV archived as $ARCHIVE_DIR/$new_name" >> "$LOG_FILE"
echo "Archived $CSV to $ARCHIVE_DIR/$new_name and created a fresh $CSV."

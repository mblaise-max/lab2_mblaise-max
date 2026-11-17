# Lab 2: Grade Evaluator

Python and shell tools for checking a student's course grades and archiving the grade file.

## Files

- `grade-evaluator.py`: reads a CSV of grades, validates it, calculates the result and prints a decision.
- `organizer.sh`: archives `grades.csv` with a timestamp, creates a fresh empty `grades.csv` and logs the action.
- `grades.csv`: sample data (columns: assignment, group, score, weight).
- `organizer.log`: log written by `organizer.sh`. Each run adds one line.
- `archive/`: timestamped copies of old grade files.

## How to run the grade evaluator

    python3 grade-evaluator.py

Enter the CSV file name when prompted (for example `grades.csv`).

## What it does

1. Checks that every score is between 0 and 100.
2. Checks that the weights total 100, with Formative = 60 and Summative = 40.
3. Calculates the final grade (sum of score x weight / 100) and the GPA (final grade / 100 x 5.0).
4. Applies the pass rule: at least 50% in BOTH Formative and Summative.
5. Finds failed Formative assignments (score below 50) and lists the ones with the highest weight for resubmission. Ties are all listed.
6. Prints PASSED or FAILED with the resubmission options.

## Error handling

The program stops with a clear message, and no crash, for: a missing file, an empty file, a missing column, non-numeric values, a missing value, an invalid group, scores outside 0-100, and weights that do not add up correctly. Blank rows are skipped.

## How to run the organizer

    chmod +x organizer.sh
    ./organizer.sh

Each run moves `grades.csv` to `archive/grades_<timestamp>.csv`, creates a new empty `grades.csv` and appends a line to `organizer.log`.

## Sample result (grades.csv)

Formative 34/60, Summative 26/40, final grade 60/100, GPA 3.00, status PASSED. Resubmission options: Group Exercise and Functions and Debugging Lab (tied at weight 20).

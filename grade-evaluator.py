import csv
import sys
import os


def load_csv_data():
    """
    Prompts the user for a filename, checks the file, and extracts
    all fields into a list of dictionaries. Bad input stops the
    program with a clear message instead of a crash.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ").strip()

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    if os.path.getsize(filename) == 0:
        print(f"Error: The file '{filename}' is empty.")
        sys.exit(1)

    required = ['assignment', 'group', 'score', 'weight']
    assignments = []
    bad_rows = []

    try:
        with open(filename, mode='r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                print(f"Error: The file '{filename}' has no header row.")
                sys.exit(1)

            reader.fieldnames = [name.strip() for name in reader.fieldnames]
            missing = [name for name in required if name not in reader.fieldnames]
            if missing:
                print(f"Error: missing column(s) in the CSV header: {', '.join(missing)}")
                sys.exit(1)

            for row in reader:
                line = reader.line_num
                values = [v for v in row.values() if isinstance(v, str)]
                if not any(v.strip() for v in values):
                    continue  # skip empty rows

                name = (row['assignment'] or '').strip()
                group = (row['group'] or '').strip().capitalize()
                score_text = (row['score'] or '').strip()
                weight_text = (row['weight'] or '').strip()

                if name == '' or score_text == '' or weight_text == '':
                    bad_rows.append(f"line {line}: a required value is missing")
                    continue

                if group not in ('Formative', 'Summative'):
                    bad_rows.append(f"line {line}: group must be Formative or Summative, got '{row['group']}'")
                    continue

                try:
                    score = float(score_text)
                    weight = float(weight_text)
                except ValueError:
                    bad_rows.append(f"line {line}: score and weight must be numbers (got '{score_text}' and '{weight_text}')")
                    continue

                if weight < 0:
                    bad_rows.append(f"line {line}: weight cannot be negative")
                    continue

                assignments.append({
                    'assignment': name,
                    'group': group,
                    'score': score,
                    'weight': weight
                })
    except (OSError, UnicodeDecodeError, csv.Error) as e:
        print(f"Error: could not read the file: {e}")
        sys.exit(1)

    if len(bad_rows) > 0:
        print(f"Error: {len(bad_rows)} bad row(s) found in '{filename}':")
        for message in bad_rows:
            print(f"  - {message}")
        sys.exit(1)

    if len(assignments) == 0:
        print(f"Error: '{filename}' has a header but no data rows.")
        sys.exit(1)

    return assignments


def validate_scores(data):
    """Return True if every score is between 0 and 100, otherwise False."""
    for item in data:
        if not (0 <= item['score'] <= 100):
            print(f"Error: score for '{item['assignment']}' is {item['score']}, it must be between 0 and 100.")
            return False
    return True


def validate_weights(data):
    """Return True if total=100, Formative=60 and Summative=40, otherwise False."""
    total = 0
    formative = 0
    summative = 0
    for item in data:
        total = total + item['weight']
        if item['group'] == 'Formative':
            formative = formative + item['weight']
        elif item['group'] == 'Summative':
            summative = summative + item['weight']

    if abs(total - 100) > 0.001:
        print(f"Error: total weight is {total}, it must be exactly 100.")
        return False
    if abs(formative - 60) > 0.001:
        print(f"Error: Formative weight is {formative}, it must be exactly 60.")
        return False
    if abs(summative - 40) > 0.001:
        print(f"Error: Summative weight is {summative}, it must be exactly 40.")
        return False
    return True


def calculate_totals(data):
    """Return (total_points, formative_points, summative_points)."""
    formative_points = 0
    summative_points = 0
    for item in data:
        points = item['score'] * item['weight'] / 100
        if item['group'] == 'Formative':
            formative_points = formative_points + points
        elif item['group'] == 'Summative':
            summative_points = summative_points + points
    total_points = formative_points + summative_points
    return total_points, formative_points, summative_points


def find_resubmissions(data):
    """
    Return the failed Formative assignments (score < 50) that share
    the highest weight. Returns an empty list if none failed.
    """
    failed = []
    for item in data:
        if item['group'] == 'Formative' and item['score'] < 50:
            failed.append(item)

    if len(failed) == 0:
        return []

    highest = failed[0]['weight']
    for item in failed:
        if item['weight'] > highest:
            highest = item['weight']

    targets = []
    for item in failed:
        if abs(item['weight'] - highest) < 0.001:
            targets.append(item)
    return targets


def evaluate_grades(data):
    """
    Implement your logic here.
    'data' is a list of dictionaries containing the assignment records.
    """
    print("\n--- Processing Grades ---")

    # a) Check if all scores are percentage based (0-100)
    if not validate_scores(data):
        return

    # b) Validate total weights (Total=100, Summative=40, Formative=60)
    if not validate_weights(data):
        return

    # c) Calculate the Final Grade and GPA
    total_points, formative_points, summative_points = calculate_totals(data)
    gpa = (total_points / 100) * 5.0
    print(f"Formative: {formative_points:.1f} / 60")
    print(f"Summative: {summative_points:.1f} / 40")
    print(f"Final grade: {total_points:.1f} / 100")
    print(f"GPA: {gpa:.2f}")

    # d) Determine Pass/Fail status (>= 50% in BOTH categories)
    formative_pct = (formative_points / 60) * 100
    summative_pct = (summative_points / 40) * 100
    print(f"Formative percentage: {formative_pct:.1f}%")
    print(f"Summative percentage: {summative_pct:.1f}%")
    passed = formative_pct >= 50 and summative_pct >= 50

    # e) Check for failed formative assignments (< 50%)
    #    and determine which one(s) have the highest weight for resubmission.
    resubmissions = find_resubmissions(data)

    # f) Print the final decision (PASSED / FAILED) and resubmission options
    print("\n--- Final Decision ---")
    if passed:
        print("Status: PASSED")
    else:
        print("Status: FAILED")

    if len(resubmissions) > 0:
        print("Resubmission options (failed Formative with the highest weight):")
        for item in resubmissions:
            print(f"  - {item['assignment']} (score {item['score']:.0f}, weight {item['weight']:.0f})")
    else:
        print("No failed Formative assignments to resubmit.")


if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()

    # 2. Process the features
    evaluate_grades(course_data)

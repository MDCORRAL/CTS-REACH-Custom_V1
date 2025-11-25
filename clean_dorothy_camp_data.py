#!/usr/bin/env python3
"""
Clean Dorothy Camp Kirby School suspension data for dashboard visualization
"""

import csv
import json
from pathlib import Path

def clean_value(value):
    """Convert value to appropriate type, handling '*' as null"""
    if value == '*' or value.strip() == '':
        return None
    try:
        # Try to convert to float for numeric values
        if '.' in value:
            return float(value)
        else:
            return int(value)
    except ValueError:
        # Return as string if not numeric
        return value

def clean_reporting_category(description):
    """Fix encoding issues in reporting category descriptions"""
    # Fix the encoding issue with Non-Binary Gender
    if '�' in description or 'Ð' in description:
        description = description.replace('2019�20', '2019-20').replace('2019Ð20', '2019-20')
    return description

def load_csv_rows(path):
    with open(path, 'r', encoding='latin-1') as f:
        reader = csv.DictReader(f)
        return list(reader)


def main():
    input_files = [
        Path('ev2_DorothyCamp_DataSummary.csv'),
        Path('ev2_DorothyCamp_DataSummary-RACE.csv')
    ]
    output_file = 'dorothy_camp_clean_data.json'

    cleaned_data = []
    missing_sources = []

    for path in input_files:
        if not path.exists():
            missing_sources.append(path.name)
            continue

        for row in load_csv_rows(path):
            cleaned_row = {
                'academicYear': row['AcademicYear'],
                'schoolName': row['SchoolName'],
                'reportingCategory': row['ReportingCategory'],
                'reportingCategoryDescription': clean_reporting_category(row['ReportingCategory_Description']),
                'cumulativeEnrollment': clean_value(row['CumulativeEnrollment']),
                'totalSuspensions': clean_value(row['Total Suspensions']),
                'uniqueStudentsSuspended': clean_value(row['Unduplicated Count of Students Suspended (Total)']),
                'uniqueStudentsSuspendedDefianceOnly': clean_value(row['Unduplicated Count of Students Suspended (Defiance-Only)']),
                'suspensionRate': clean_value(row['Suspension Rate (Total)']),
                'suspensionsViolentWithInjury': clean_value(row['Suspension Count Violent Incident (Injury)']),
                'suspensionsViolentNoInjury': clean_value(row['Suspension Count Violent Incident (No Injury)']),
                'suspensionsWeapons': clean_value(row['Suspension Count Weapons Possession']),
                'suspensionsDrugs': clean_value(row['Suspension Count Illicit Drug-Related']),
                'suspensionsDefianceOnly': clean_value(row['Suspension Count Defiance-Only']),
                'suspensionsOther': clean_value(row['Suspension Count Other Reasons']),
                'schoolType': row['School Type'],
                'sourceFile': path.name
            }

            cleaned_data.append(cleaned_row)

    if missing_sources:
        print("⚠️  Missing source files:", ', '.join(missing_sources))

    # Write cleaned data to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=2)

    print(f"✓ Cleaned {len(cleaned_data)} records")
    print(f"✓ Output written to {output_file}")

    # Print summary statistics
    years = set(row['academicYear'] for row in cleaned_data)
    categories = set(row['reportingCategoryDescription'] for row in cleaned_data if row['reportingCategoryDescription'])
    sources = set(row['sourceFile'] for row in cleaned_data)

    print(f"\nData Summary:")
    print(f"  Academic Years: {sorted(years)}")
    print(f"  Student Groups: {len(categories)}")
    print(f"  Categories: {sorted(categories)}")
    print(f"  Sources merged: {sorted(sources)}")

if __name__ == '__main__':
    main()

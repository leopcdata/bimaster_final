import os
import datetime


def select_input_file(input_folder):
    files = [
        f for f in os.listdir(input_folder)
        if os.path.isfile(os.path.join(input_folder, f)) and f.lower().endswith(".xlsx")
    ]

    if not files:
        raise FileNotFoundError("No input files found in the folder.")

    print("Available input files:")
    for i, file in enumerate(files, start=1):
        print(f"{i}: {file}")

    selection = input("Enter the number corresponding to the input file you want to use: ")

    try:
        selection = int(selection)
    except ValueError as exc:
        raise ValueError("Invalid input. Please enter a number.") from exc

    if not (1 <= selection <= len(files)):
        raise ValueError("Selection out of range.")

    return os.path.join(input_folder, files[selection - 1])


def get_country_code():
    country_code = input("Please enter a 3-digit country code for cca.ctrynum: ").strip()
    if not (country_code.isdigit() and len(country_code) == 3):
        raise ValueError("Invalid country code. Please enter a 3-digit numeric code.")
    return country_code


def build_output_path(results_folder, input_file):
    os.makedirs(results_folder, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    return os.path.join(results_folder, f"{base_name} ACL results - {timestamp_str}.xlsx")
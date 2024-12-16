import os
import requests

def check_email_with_api(email):
    api_url = "http://apilayer.net/api/check"
    api_key = "5982f99b442b768f67f3b6b95ed8a229"

    params = {
        "access_key": api_key,
        "email": email,
        "smtp": 1
    }

    try:
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get("format_valid", False) and data.get("smtp_check", False)
        else:
            print(f"API error for {email}: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return False

def print_colored(message, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "reset": "\033[0m"
    }
    return f"{colors.get(color, colors['reset'])}{message}{colors['reset']}"

def main():
    if not os.path.exists("email.txt"):
        print("The file 'email.txt' was not found. Make sure it is in the same folder as this script.")
        return

    with open("email.txt", "r") as file:
        emails = file.readlines()

    emails = [email.strip() for email in emails if email.strip()]

    if not emails:
        print("No emails found in 'email.txt'.")
        return

    print("\n--- Starting email validation ---\n")

    for email in emails:
        is_valid = check_email_with_api(email)
        if is_valid:
            print(print_colored(f"[VALID] The email is valid: {email}", "green"))
        else:
            print(print_colored(f"[INVALID] The email is invalid: {email}", "red"))

    print("\n--- Email validation completed ---")

if __name__ == "__main__":
    main()

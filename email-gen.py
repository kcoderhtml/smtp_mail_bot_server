import requests
import random
import string
import time

def load_dictionary(file_path):
    with open(file_path, 'r') as file:
        words = file.read().splitlines()
    return words

# Function to generate a random email address
def generate_random_email(dictionary):
    domain = "mail.kieranklukas.com"
    
    # Randomly select two words from the dictionary
    random_words = random.sample(dictionary, 2)
    
    # Combine the selected words with a dot separator
    local_part = ".".join(random_words)
    
    email = f"{local_part}@{domain}"
    return email

# URL and headers
url = 'https://kingsumo.com/giveaways/l1bih1/enter'
headers = {
    'cookie': 'XSRF-TOKEN=eyJpdiI6IjltMG12YjFIMmcrQjlEWkNIZXZ0eGc9PSIsInZhbHVlIjoidU9MWVFMbmpVbVwvWEpvRFA4eVJhcTJsQk1idUZ3dk9cL0Jud0Mwc0hCWGJUREFnKzlvUGRPUHdMYkFWTjZIbHloIiwibWFjIjoiYzA0NzEzN2FiYjhjMzM1ZTE4NmM0ZDdkZWM4YzBhMzhjMjc0NTRhY2JlOGQwODkwOGNlNGE1ZWNhZGE1ZDY4ZCJ9; kingsumo_session__=eyJpdiI6Ink1U1pEYUswSFRPRG1LV3VtcEswdmc9PSIsInZhbHVlIjoib1pLSkZRRGgyT3Z2NUJCYTFZbTQxM1J1VHE1R0wzd0hNaHlQcXVOT2hMWHA1MktaS3pPaFI4cUhzTWJ0Yk5vcyIsIm1hYyI6IjFiNDUwNzY5NzQ4ZDZjNmIxMGEwYmFmNjllYTQ2M2I2MDQxZjE5ZjVlNGRiZGZkY2E3YjQyMDU2NjAyNzc1ZmQifQ%3D%3D',  # Your cookie here
}

# POST data template
data = {
    '_token': 'V8gOoZAMSHxE7evq6LNnu7u03FMkdatFodTuiSWQ',
    'gdpr_consent': '1',
    'referrer': 'pe662eq',
    'g-recaptcha-response': 'HFYzIycEsUIjRwRDoHTRgWTFNRIE4zQzExMlJlF2dzO2MyZEMiGBN5HE0fWnY7dSRpYVZtEFZBYVZEACsfJCFzc2khJ0YQMG4SPmsdMQglYBBRdQxpCmQQMGdBSB9CQBobFkZxfHY4Pyo7X34RdSE9YWFwBzU9cTlJGHUGJFtkNSNwYXpBEAtCGxwMSiJeSWVWZSYZEg8qaxBlIyBdW3VuHFpydg',  # Your g-recaptcha-response here
}

failed = 0
success = 0

def get_email(dictionary):
    email = generate_random_email(dictionary)
    data['email'] = email

    response = requests.post(url, headers=headers, data=data, allow_redirects=True)
    print(f"Email: {email}")
    print("Response Status:", response.status_code)
    return response.status_code

if __name__ == "__main__":
    dictionary_path = "/usr/share/dict/words"  # Adjust the path as needed
    dictionary = load_dictionary(dictionary_path)
    
    try:
        while True:
            if failed >= 3:
                print("Failed 3 times, sleeping for 5 minutes...")
                time.sleep(300)
                failed = 0
                success = 0
            if success >= 5:
                print("Success 5 times, sleeping for 5 minutes...")
                time.sleep(300)
                failed = 0
                success = 0
            else:
                if get_email(dictionary) == 200:
                    print("Success!")
                    time.sleep(90)
                    failed = 0
                    success+=1
                else:
                    failed+=1
                    print("Failed!")
                    time.sleep(180+failed*20)
    except KeyboardInterrupt:
        print("Exiting...")
        exit()
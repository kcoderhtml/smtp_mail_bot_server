import time
import requests
import random
import string

def generate_random_email():
    domain = "mail.kieranklukas.com"
    random_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))
    email = f"{random_string}@{domain}"
    return email

# Replace these with the actual API endpoint and headers
url = 'https://kingsumo.com/giveaways/l1bih1/enter'

headers = {
    'cookie': 'XSRF-TOKEN=eyJpdiI6IjNEckNzdHhYZ0JYKzgzT0x0RUE3V0E9PSIsInZhbHVlIjoiMmxpOEMybENKUlwvVkhaWittQ1pPXC9vSUw4d0QwTlJnMXJ1M0lDZjBHQVFqMzVpRVFFXC9IdUJ6YUszNmRKTHk0bCIsIm1hYyI6ImNkMTIxZWQzZDRjYjc5MDUwZThhYjljZmM1YWQ4NDY4NTA5YzIwNGYzZjdkZjkzMjQ3M2U3ZWNlYWQ3YWYyOTAifQ%3D%3D; kingsumo_session__=eyJpdiI6IkM5MGFXeHAzMVlER0ZKbSttMW9wTFE9PSIsInZhbHVlIjoiZDBNYWRoNjJWNDdVVG5RblNBcXZZVjBJNFVjXC9vUWhVbzdMSkRVcUVoWEU1UDQ0RFpvZEJUczVOa0FGZHlEck4iLCJtYWMiOiIzODQ3Y2UyNGVhODYwYzM4ZWJiMTYzOWYxZjVkOWIzOGI0MDY5MWVhNTJhYmE0NjFmMGVkYTYyYjFkNzI1YzBiIn0%3D',  # Your cookie here
}

# POST data template
data = {
    '_token': 'BTNgzL77FhS4fWl3f2GUX9WlIfhug1q280sayxgb',
    'gdpr_consent': '1',
    'referrer': 'pe662eq',
    'g-recaptcha-response': '03ADUVZwA1zmwTO7yy0efKSeSKiDHDZFMowfU8JHGBrEU9Cn-g6tpkzTNbLIfqbQlHcJz0ScOxOcfBhAeVHQG2u1v3eHACVLABG7G3IrNZKjzJ4SyGvdCs3n1V3zVegs_h2hFtp1o1QhTZLqlZc1VJMmRuOTZoFkkGLbVQlFbDZ-aZ9p4cgIc-psg-OGNCex47DEk2CCw9PgF3NiAIwfxCKydT7C-gbV0BLREqFtUYMFV9SvTxhPM1vtqN-jAXxknH5lY9W8xCq42Qk-2ffCA1rw3LPH_FpHPwnaPiE0sPha70sSEh5U_2KzSwwSeUYASBWyAMcQUYEH18gY1aE2oSv2ejU3-JGsGOoN3rSmfIzQ6zfXw8l1dkdb86wv_Y9fV1vlkQWeyAcFYS5jQFGBwI1bsUb6HVpf8Z51GLM0CaD_E4S0kvwrpHQ5GJ5VwTj5FXgO92THRURVXlAFxKKPMEhpHjbc6-kbugF8A8RtLeui1sAwdnaouaM4_O6e9vU0SWUPoCq52cEeBuWmE3H3abE4DHa_h86xLm_v90yDKEs3Z9x0OLlXyH57SZKuZue_u8OIMuRCX3NUF5q4VOwt8aVI',  # Your g-recaptcha-response here
}

def test_request(interval):
    email = generate_random_email()
    data['email'] = email

    response = requests.get(url, headers=headers, data=data, allow_redirects=True)
    return response

def probe_rate_limit():
    base_interval = 5  # Starting interval in seconds
    max_successful_requests = 3  # Number of successful requests before testing rate limit
    rate_limit_reached = False

    for _ in range(max_successful_requests):
        response = test_request(base_interval)
        print(f"Status Code: {response.status_code}")
        time.sleep(base_interval)

    for i in range(base_interval - 1, 0, -1):
        print(f"Waiting for {i} seconds...")
        time.sleep(1)

    while not rate_limit_reached:
        response = test_request(base_interval)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 429:
            print("Rate limit reached!")
            rate_limit_reached = True
        time.sleep(base_interval)

probe_rate_limit()

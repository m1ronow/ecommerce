import hashlib
import hmac
import json
import requests
import re
import environ
env = environ.Env()
env.read_env()


def create_assessment(token, action):
    assessment_result = requests.post(
        f'https://recaptchaenterprise.googleapis.com/'
        f'v1/projects/{env("GCP_PROJECT_ID")}/assessments?key={env("GCP_PROJECT_API_KEY")}',
        headers={
            'Content-Type': 'application/json',
            'charset': 'utf-8',
        },
        data=json.dumps({
            "event": {
                "token": token,
                "siteKey": env("GCP_RECAPTCHA_SITE_KEY"),
                "expectedAction": action
            }
        }))

    return assessment_result.json()


def check_email_syntax(email):
    email_regex = r'^(?=.{1,254}$)(?=.{1,64}@)[a-zA-Z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&\'*+/=?^_`{' \
                  r'|}~-]+)*@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,' \
                  r'61}[a-zA-Z0-9])?)*$'
    return bool(re.match(email_regex, email))


def validate_webhook_signature(payload, webhook_signature):
    secret_key = env('COINBASE_COMMERCE_SHARED_SECRET').encode('utf-8')

    # Create a new HMAC object with the secret key and SHA256 digest algorithm
    hmac_obj = hmac.new(secret_key, payload, hashlib.sha256)

    # Calculate the computed signature
    computed_signature = hmac_obj.hexdigest()

    # Compare the computed signature with the provided signature
    if computed_signature == webhook_signature:
        return True
    else:
        return False


def create_coinbase_payment(amount, order_uuid):
    url = 'https://api.commerce.coinbase.com/charges/'
    headers = {
        'Content-Type': 'application/json',
        'X-CC-Api-Key': env('COINBASE_COMMERCE_API_KEY'),
        'X-CC-Version': env('COINBASE_COMMERCE_VERSION'),
    }
    data = json.dumps({
        'name': f'Payment {order_uuid}',
        'description': 'Payment',
        'pricing_type': 'fixed_price',
        'local_price': {
            'amount': amount,
            'currency': env('CURRENCY_CODE'),
        },
        'metadata': {
            'order_id': order_uuid,
        },
        'redirect_url': f'http://localhost:8100/profile/orders/{order_uuid}',
        'cancel_url': f'http://localhost:8100/profile/orders/{order_uuid}',
    })
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 201:
        return response.json()
    else:
        raise Exception('Failed to create Coinbase payment')

import os
import requests

for check in os.listdir('checks'):
    if not check.endswith('.py'):
        continue

    check_module = __import__(f"checks.{check[:-3]}", fromlist=[''])

    messages = check_module.main()

    if messages:
        requests.post('http://localhost:8080/api/v1/send_email', json={'message_text': '\n\n'.join(messages)})
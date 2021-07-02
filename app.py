from chalice import Chalice

app = Chalice(app_name='email-authentication')


@app.route('/generate/{email}', cors=True)
def generate(email):
    import boto3, uuid
    from botocore.exceptions import ClientError
    SENDER = "Cloudmatica Auth <noreply@cloudmatica.com>"
    RECIPIENT = email
    SUBJECT = "Your One-Time Password (OTP)"
    AWS_REGION = "us-east-1"
    otp = str(uuid.uuid4())
    BODY_TEXT = f"Your one-time password (OTP) is {otp}"
    CHARSET = "UTF-8"
    client = boto3.client('ses',region_name=AWS_REGION)
    s3 = boto3.client('s3', region_name=AWS_REGION)
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [ RECIPIENT ]
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT
                    }
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT
                }
            },
            Source=SENDER,
        )
        s3.put_object(Body=bytes(otp, 'utf-8'), Bucket='cloudmatica', Key=f'email-authentication/{email}')
    except ClientError as e:
        print(e.response['Error']['Message'])
        return False
    else:
        print("Email sent! Message ID: ", response['MessageId'])
        return True

@app.route('/verify/{email}/{otp}', cors=True)
def verify(email, otp):
    import boto3
    s3 = boto3.client('s3')
    return s3.get_object(Bucket='cloudmatica', Key=f'email-authentication/{email}')['Body'].read().decode('utf-8') == otp


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#

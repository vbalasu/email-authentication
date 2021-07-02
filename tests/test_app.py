import app
from chalice.test import Client

def test_generate():
  with Client(app.app) as client:
    response = client.http.get('/generate/vbalasu@gmail.com')
    assert response.status_code == 200
    assert response.json_body == True

# Compare the OTP value to `aws s3 cp s3://cloudmatica/email-authentication/vbalasu@gmail.com -`
def test_verify():
  with Client(app.app) as client:
    response = client.http.get('/verify/vbalasu@gmail.com/6e600f3d-d487-4505-88c5-9b1b6dee8f90')
    assert response.status_code == 200
    assert response.json_body == True
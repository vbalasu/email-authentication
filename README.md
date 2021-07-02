# email-authentication

`email-authentication` is a web service that generates one-time passwords (OTP) and sends them to a specified email address.

This is live at [https://email-authentication.cloudmatica.com](https://email-authentication.cloudmatica.com)

Input
- email address [required], callback url [optional]

Output
- Email sent to address from noreply@cloudmatica.com, with OTP in the body. Sent as a link if callback URL is provided

Process
- System generates a uuid to serve as the OTP. The generated OTP is stored for later verification
- Client calls /verify endpoint with email and OTP. The service responds with true/false indicating successful authentication

Interface
- /generate/{email} - returns true if email is sent
- /verify/{email}/{OTP} - returns true if OTP is correct
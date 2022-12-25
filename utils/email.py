from fastapi import Request, HTTPException
from typing import List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from jinja2 import Environment, select_autoescape, PackageLoader
from settings import settings

# env = Environment(
#     loader=PackageLoader('app', 'templates'),
#     autoescape=select_autoescape(['html', 'xml'])
# )



# class Email:
#     def __init__(self, user: dict, url: str, email: List[EmailStr]):
#         self.name = user['name']
#         self.sender = 'Codevo <admin@admin.com>'
#         self.email = email
#         self.url = url
#         pass

#     def sendMail(self, subject, template):
#         # Define the config
#         conf = ConnectionConfig(
#             MAIL_USERNAME=settings.EMAIL_USERNAME,
#             MAIL_PASSWORD=settings.EMAIL_PASSWORD,
#             MAIL_FROM=settings.EMAIL_FROM,
#             MAIL_PORT=settings.EMAIL_PORT,
#             MAIL_SERVER=settings.EMAIL_HOST,
#             MAIL_STARTTLS=False,
#             MAIL_SSL_TLS=False,
#             USE_CREDENTIALS=True,
#             VALIDATE_CERTS=True
#         )
#         # Generate the HTML template base on the template name
#         template = env.get_template(f'{template}.html')

#         html = template.render(
#             url=self.url,
#             first_name=self.name,
#             subject=subject
#         )

#         # Define the message options
#         message = MessageSchema(
#             subject=subject,
#             recipients=self.email,
#             body=html,
#             subtype="html"
#         )

#         # Send the email
#         fm = FastMail(conf)
#         fm.send_message(message)


def verification_mail(request, user, token):
    url = f"{request.url.scheme}://{request.client.host}:{request.url.port}/api/auth/verifyemail/{token}"
    message = f'''
    Hi {user.first_name}, 
    We are very happy to have you at consult, click on the url to verify your email {url}
    '''
    return message

def password_reset_mail(request, user, token):
    url = f"{request.url.scheme}://{request.client.host}:{request.url.port}/api/auth/verifyemail/{token}"
    message = f'''
    Hi {user.first_name}, 
    Your Password reset link is {url}
    '''
    return message
    # try:
    #     Email(user, url, [EmailStr(user.email)]).sendMail('Password Reset', 'password-reset')
    # except Exception as e:
    #     raise HTTPException(status_code=401, detail='There was an error sending Email')
    # return {'status': 'success', 'message': 'Verification token successfully sent to your email'}
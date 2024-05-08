import random
from django.core.mail import EmailMessage
def generate_otp_code():
    number_list = [x for x in range(10)] 
    code_items_for_otp = []
    for i in range(4):
        num = random.choice(number_list)
        code_items_for_otp.append(num)
    code_string = "".join(str(item)for item in code_items_for_otp)
    return code_string

def send_email(user_email,user_otp):
    email_message = EmailMessage('MaskneApp', f'Your OTP is {user_otp}, if you got any problem please connect with the support team',to=[user_email])
    email_message.send()
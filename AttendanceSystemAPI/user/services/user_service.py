from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from .Verification import Verification
from django.core.mail import EmailMessage
from decouple import config
from .mailling import Mailing

User = get_user_model()

class UserService():
    @classmethod
    def change_password(cls, email, current_password, new_password):
        try:
            user = User.objects.filter(email=email).first()
            if not user:
                raise ValueError("User not found.")
            
            if not check_password(current_password, user.password):
                raise ValueError("Current password is incorrect.")
            
            user.set_password(new_password)
            user.save()
        except ValueError as ve:
            raise ValueError(ve)
        except Exception as e:
            print(e)
            raise ValueError("An error occurred.")
        
    @classmethod
    def forgot_password(cls, email):
        try:
            user = User.objects.filter(email=email).first()
            if not user:
                raise ValueError("User not found.")
            
            data = {"email": email}
            token = Verification.create_token(data)

            fe_host = config('FE_HOST')
            admin_scheme = (
                "http"
                if fe_host.startswith("localhost") or fe_host.startswith("127.0.0.1")
                else "https"
            )

            link = f"{admin_scheme}://{fe_host}/reset_password?token={token}"

            data = {
                "template": "email_forgot_password_template.html",
                "subject": "Password Reset Request",
                "context": {
                    "email": email,
                    "link": link,
                },
                "to": [email],
            }
            
            message = Mailing.create_html_message(data=data)
            Mailing.asyn_send_message(message=message)

        except ValueError as ve:
            print(ve)
            raise ValueError(ve)

        except Exception as e:
            print(e)
            raise ValueError("An error occurred.")
        
    @classmethod
    def reset_password(cls, token, new_password):
        try:
            data = Verification.verify_token(token)
            email = data.get('email')
            user = User.objects.filter(email=email).first()
            if not user:
                raise ValueError("User not found.")
            user.set_password(new_password)
            user.save()
        except Verification.TokenExpiredError:
            raise ValueError("Token has expired.")
        except Verification.TokenInvalidError:
            raise ValueError("Invalid token.")
        except Exception as e:
            print(e)
            raise ValueError("An error occurred.")


            
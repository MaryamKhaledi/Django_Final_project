from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, password, email=None, phone_number=None, first_name=None, last_name=None,
                    birth_date=None,
                    gender=None, country=None, is_superuser=False):
        if not phone_number and not is_superuser:
            raise ValueError('accounts must have phone number')

        if not username:
            raise ValueError('accounts must have email')
        username = f'{username}@eml.com'
        user = self.model(username=username, email=email, phone_number=phone_number, first_name=first_name,
                          last_name=last_name, birth_date=birth_date, gender=gender, country=country)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):
        accounts = self.create_user(username, password, is_superuser=True)
        accounts.is_superuser = True
        accounts.is_staff = True
        accounts.is_active = True

        accounts.save(using=self._db)
        return

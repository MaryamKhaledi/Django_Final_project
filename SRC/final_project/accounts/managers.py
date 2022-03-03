from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, phone_number, first_name, last_name, birth_date, gender, country, password):
        if not phone_number:
            raise ValueError('accounts must have phone number')

        if not username:
            raise ValueError('accounts must have email')
        # username = username+"@eml"
        user = self.model(username=username, phone_number=phone_number, first_name=first_name, last_name=last_name,
                          birth_date=birth_date, gender=gender, country=country)
        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, phone_number, email, password):
        accounts = self.create_user(phone_number, email, password)
        accounts.is_superuser = True
        accounts.save(using=self._db)
        return

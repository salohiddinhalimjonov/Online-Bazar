from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator


from .managers import UserManager



class User(AbstractBaseUser, PermissionsMixin):
    
    phone_number = models.CharField(unique=True, max_length=12,validators=[RegexValidator(regex=r'^(\+?998)?([. \-])?((\d){2})([. \-])?(\d){3}([. \-])?(\d){2}([. \-])?(\d){2}$',
                                                        message="Given phone number is not valid")])
    full_name = models.CharField(_('Ismi:'), max_length=150)
    
    # set AbstractUser defaults
    date_joined = models.DateTimeField(
        _('Ro‘yxatdan o‘tgan sanasi'), default=timezone.now)
    is_superuser = models.BooleanField(
        _('Administratormi?'),
        default=False,
        help_text=_('Administrator huquqini beradi'),
    )
    is_staff = models.BooleanField(
        _('Moderatormi?'),
        default=False,
        help_text=_('Admin qismiga kirish huquqini beradi.'),
    )
    is_active = models.BooleanField(
        _('Aktivmi?'),
        default=True,
        help_text=_('Saytga kirish huquqini beradi.'),
    )
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'

    class Meta:
        verbose_name = _('Foydalanuvchi')
        verbose_name_plural = _('Foydalanuvchilar')

    def __str__(self):
        return self.full_name
    
# def _generate_verification_code():
#     range_start = 10 ** (6 - 1)
#     range_end = (10 ** 6) - 1
#     return randint(range_start, range_end)

# def _expire_at_default():
#     return timezone.now() + timezone.timedelta(minutes=settings.CODE_VERIFICATION_EXPIRE_TIME)    


# class VerificationCode(models.Model):
#     code_regex = RegexValidator(
#         regex=r'^\d{6}$', message="123456 holatda kiriting")
#     code = models.CharField(_('Maxfiy kod'), max_length=6, validators=[
#                             code_regex], default=_generate_verification_code)
#     phone_number = models.CharField(
#         _('Aloqa raqami'), max_length=12, 
#         validators=[RegexValidator(regex=r'^(\+?998)?([. \-])?((\d){2})([. \-])?(\d){3}([. \-])?(\d){2}([. \-])?(\d){2}$',
#                                                        message="Given phone number is not valid")]
# )
#     expire_at = models.DateTimeField(
#         _('Yaroqlilik muddati'), default=_expire_at_default)

#     def __str__(self):
#         return str(self.contact)

#     class Meta:
#         verbose_name = "Tasdiqlash kod"
#         verbose_name_plural = "Tasdiqlash kodlari"


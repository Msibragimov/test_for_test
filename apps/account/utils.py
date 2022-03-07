from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

from apps.account.models import Account

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: Account, timestamp: int):
        return (six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_email_verified))

generate_token = TokenGenerator()
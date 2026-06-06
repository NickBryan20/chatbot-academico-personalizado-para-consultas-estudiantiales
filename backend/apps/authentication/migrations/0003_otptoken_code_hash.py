from django.contrib.auth.hashers import make_password
from django.db import migrations, models


def hash_existing_otp_codes(apps, schema_editor):
    OTPToken = apps.get_model('authentication', 'OTPToken')
    for otp in OTPToken.objects.filter(code_hash='').exclude(code=''):
        if set(otp.code) == {'*'}:
            continue
        otp.code_hash = make_password(otp.code)
        otp.code = '*' * len(otp.code)
        otp.save(update_fields=['code_hash', 'code'])


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='otptoken',
            name='code_hash',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
        migrations.RunPython(hash_existing_otp_codes, migrations.RunPython.noop),
    ]

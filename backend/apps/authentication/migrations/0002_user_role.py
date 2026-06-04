from django.db import migrations, models


def set_existing_roles(apps, schema_editor):
    User = apps.get_model('authentication', 'User')
    User.objects.filter(is_staff=True).update(role='admin')
    User.objects.filter(is_superuser=True).update(role='admin')


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(
                choices=[
                    ('student', 'Estudiante'),
                    ('teacher', 'Docente'),
                    ('admin', 'Administrador'),
                ],
                default='student',
                max_length=20,
            ),
        ),
        migrations.RunPython(set_existing_roles, migrations.RunPython.noop),
    ]

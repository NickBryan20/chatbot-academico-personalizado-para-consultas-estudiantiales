from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('students', '0004_alter_student_carrera_alter_subject_carrera_activity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='professor',
            name='user',
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='professor_profile',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

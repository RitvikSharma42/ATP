# Generated by Django 3.2.5 on 2023-09-03 10:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('audio_app', '0002_audiorecording_script_output'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiorecording',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='audiorecording',
            name='audio_file',
            field=models.FileField(upload_to='audio/'),
        ),
        migrations.AlterField(
            model_name='audiorecording',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]

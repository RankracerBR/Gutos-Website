# Generated by Django 5.0 on 2024-01-04 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_userprofilehistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofilehistory',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
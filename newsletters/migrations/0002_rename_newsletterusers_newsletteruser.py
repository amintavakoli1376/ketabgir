# Generated by Django 3.2.9 on 2022-03-02 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletters', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NewsletterUsers',
            new_name='NewsletterUser',
        ),
    ]

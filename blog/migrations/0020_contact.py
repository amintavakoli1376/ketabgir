# Generated by Django 3.2.9 on 2022-03-22 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_delete_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_name', models.CharField(max_length=200)),
                ('message', models.EmailField(max_length=254)),
                ('message_email', models.TextField()),
            ],
        ),
    ]

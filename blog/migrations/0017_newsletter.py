# Generated by Django 3.2.9 on 2022-03-11 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_newsletteruser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=250)),
                ('body', models.TextField()),
                ('status', models.CharField(choices=[('draft', 'پیش نویس'), ('published', 'منتشرشده')], max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('email', models.ManyToManyField(to='blog.NewsletterUser')),
            ],
        ),
    ]

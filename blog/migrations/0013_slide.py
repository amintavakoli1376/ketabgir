# Generated by Django 3.2.9 on 2022-02-04 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_article_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
    ]
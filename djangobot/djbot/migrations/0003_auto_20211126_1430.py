# Generated by Django 3.2.9 on 2021-11-26 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djbot', '0002_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(unique=True, upload_to='media/tb'),
        ),
        migrations.AlterField(
            model_name='file',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
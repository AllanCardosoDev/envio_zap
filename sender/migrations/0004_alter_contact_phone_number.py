# Generated by Django 5.0.6 on 2024-06-11 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sender', '0003_alter_contact_name_alter_contact_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='phone_number',
            field=models.CharField(max_length=20),
        ),
    ]
# Generated by Django 5.0.6 on 2024-06-12 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sender', '0010_alter_group_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(to='sender.contact'),
        ),
    ]

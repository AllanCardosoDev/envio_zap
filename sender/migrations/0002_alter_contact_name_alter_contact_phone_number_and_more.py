# Generated by Django 5.0.6 on 2024-06-11 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sender', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone_number',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='group',
            name='group_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(related_name='groups', to='sender.contact'),
        ),
    ]

# Generated by Django 5.0.6 on 2024-06-11 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sender', '0005_rename_group_name_group_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='name',
        ),
        migrations.AddField(
            model_name='group',
            name='group_name',
            field=models.CharField(default='default_group_name', max_length=255),
        ),
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
        migrations.RemoveField(
            model_name='group',
            name='members',
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]

# Generated by Django 5.0.6 on 2024-06-22 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_uploadfile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadfile',
            name='file',
        ),
        migrations.RemoveField(
            model_name='uploadfile',
            name='id',
        ),
        migrations.AddField(
            model_name='uploadfile',
            name='type',
            field=models.CharField(default='pdf', max_length=30),
        ),
        migrations.AlterField(
            model_name='uploadfile',
            name='filename',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]

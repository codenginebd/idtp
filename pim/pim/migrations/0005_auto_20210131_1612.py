# Generated by Django 3.1.5 on 2021-01-31 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pim', '0004_auto_20210131_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auditlog',
            name='status',
            field=models.CharField(blank=True, default='SUCCESS', max_length=50, null=True),
        ),
    ]
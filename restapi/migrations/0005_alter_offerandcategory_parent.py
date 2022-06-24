# Generated by Django 4.0.5 on 2022-06-22 09:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0004_alter_offerandcategory_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offerandcategory',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='restapi.offerandcategory', to_field='uuid'),
        ),
    ]

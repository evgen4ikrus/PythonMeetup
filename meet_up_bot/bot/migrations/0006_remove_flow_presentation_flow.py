# Generated by Django 4.0.5 on 2022-08-04 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_flow_presentation_flow_flow_group_presentation_group_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flow',
            name='presentation_flow',
        ),
    ]
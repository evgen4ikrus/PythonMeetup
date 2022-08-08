# Generated by Django 4.0.5 on 2022-08-04 12:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_alter_block_flow_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='flow',
            name='presentation_flow',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='flow_group',
            name='presentation_group',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='block',
            name='Flow_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocks', to='bot.flow_group', verbose_name='Группа потока'),
        ),
    ]

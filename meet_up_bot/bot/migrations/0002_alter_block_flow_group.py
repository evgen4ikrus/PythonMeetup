# Generated by Django 4.0.5 on 2022-08-04 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='Flow_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocks', to='bot.flow_group', verbose_name='Группа потока'),
        ),
    ]
# Generated by Django 3.2.16 on 2022-11-07 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0006_alter_entry_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='tags',
            field=models.ManyToManyField(null=True, to='budgets.Tag', verbose_name='tags'),
        ),
    ]
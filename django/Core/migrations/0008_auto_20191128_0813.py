# Generated by Django 2.1.5 on 2019-11-28 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0007_auto_20191128_0724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='link',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Core.Page'),
        ),
    ]
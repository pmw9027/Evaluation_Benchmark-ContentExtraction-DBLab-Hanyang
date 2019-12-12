# Generated by Django 2.1.5 on 2019-12-11 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='node',
            name='node_name',
        ),
        migrations.AddField(
            model_name='node',
            name='name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Core.NodeName'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nodename',
            name='node_name',
            field=models.CharField(default=1, max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='testset',
            name='pages',
            field=models.ManyToManyField(blank=True, to='Core.Page'),
        ),
    ]

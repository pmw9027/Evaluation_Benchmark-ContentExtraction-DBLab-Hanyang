# Generated by Django 2.1.5 on 2019-12-16 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Extractor', '0003_auto_20191216_0724'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerformanceEvaluationResult',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('precision', models.FloatField(default=None, null=True)),
                ('recall', models.FloatField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PerformanceMetric',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='performanceevaluationresult',
            name='performance_metric',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Evaluation.PerformanceMetric'),
        ),
        migrations.AddField(
            model_name='performanceevaluationresult',
            name='predict',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Extractor.Predict'),
        ),
        migrations.AlterUniqueTogether(
            name='performanceevaluationresult',
            unique_together={('predict', 'performance_metric')},
        ),
    ]

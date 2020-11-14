# Generated by Django 2.0 on 2020-11-14 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare_workers', '0002_historicalmedicaldata_recentmedicaldata'),
        ('patient', '0006_auto_20201114_0425'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreviousPatient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=50)),
                ('admissionDate', models.DateField()),
                ('releaseData', models.DateField()),
                ('bed', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='healthcare_workers.Bed')),
            ],
        ),
    ]

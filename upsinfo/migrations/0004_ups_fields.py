# Generated by Django 3.1.1 on 2022-01-03 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('upsinfo', '0003_event_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ups',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='event',
            name='ups',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='upsinfo.ups'),
        ),
        migrations.AlterField(
            model_name='status',
            name='ups',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='status', to='upsinfo.ups'),
        ),
        migrations.AlterField(
            model_name='ups',
            name='ip',
            field=models.GenericIPAddressField(unique=True),
        ),
        migrations.AlterField(
            model_name='ups',
            name='vendor',
            field=models.CharField(choices=[['Generic', 'RFC 1628'], ['APC', 'APC'], ['Eaton', 'Eaton'], ['APCSmartConnect', 'APC Smart Connect']], default='Generic', max_length=20),
        ),
    ]

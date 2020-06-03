# Generated by Django 3.0.6 on 2020-06-03 02:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fr_sys', '0003_auto_20200603_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='fediverseuser',
            name='following',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='emoji',
            name='remote',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='emojis', to='fr_sys.FediverseServer'),
        ),
    ]
# Generated by Django 3.0.4 on 2020-03-25 02:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bevdir', '0006_auto_20200325_0230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portion',
            name='misc_ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portions', to='bevdir.MiscIngredient'),
        ),
    ]

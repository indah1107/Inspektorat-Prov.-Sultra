# Generated by Django 5.1.6 on 2025-02-12 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dokumen', '0002_alter_laporan_tanggal_masuk_surat'),
    ]

    operations = [
        migrations.AddField(
            model_name='dokumen',
            name='laporan_diunggah',
            field=models.BooleanField(default=False),
        ),
    ]

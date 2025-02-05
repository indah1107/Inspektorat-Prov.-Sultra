from django.db import models
from django.utils.timezone import now


class Dokumen(models.Model):
    IRBAN_CHOICES = [
        ("IRBAN 1", "IRBAN 1"),
        ("IRBAN 2", "IRBAN 2"),
        ("IRBAN 3", "IRBAN 3"),
        ("IRBAN 4", "IRBAN 4"),
        ("IRBAN INVESTIGASI", "IRBAN INVESTIGASI"),
    ]

    nomor_surat = models.CharField(max_length=100, unique=True)
    tanggal_surat = models.DateField()
    irban = models.CharField(max_length=20, choices=IRBAN_CHOICES)
    tim_audit = models.JSONField(default=list)
    uraian = models.CharField(max_length=255)
    file = models.FileField(upload_to="dokumen/")

    def __str__(self):
        return f"{self.nomor_surat} - {self.irban}"


class Laporan(models.Model):
    dokumen = models.OneToOneField(Dokumen, on_delete=models.CASCADE, related_name="laporan")
    judul_laporan = models.CharField(max_length=255)
    tanggal_laporan = models.DateField(default=now)
    nomor_laporan = models.CharField(max_length=100)
    keterangan = models.CharField(max_length=100)
    file = models.FileField(upload_to="laporan/")

    def __str__(self):
        return self.judul_laporan

from django.db import models

class Dokumen(models.Model):
    nomor_surat = models.CharField(max_length=50)
    judul = models.CharField(max_length=255)
    jenis = models.CharField(max_length=50)
    file = models.FileField(upload_to='dokumen/')  # Folder tempat menyimpan file

    def __str__(self):
        return self.judul

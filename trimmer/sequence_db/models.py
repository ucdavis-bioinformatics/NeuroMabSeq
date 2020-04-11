from django.db import models

# Create your models here.

class VLSeq(models.Model):
    id = models.AutoField(primary_key=True)
    seq = models.CharField(max_length=1500, default='')


class VHSeq(models.Model):
    id = models.AutoField(primary_key=True)
    seq = models.CharField(max_length=1500, default='')

class Metadata(models.Model):
    id = models.AutoField(primary_key=True)
    target_type = models.CharField(max_length=25, default='', blank=True)
    target = models.CharField(max_length=50, default='', blank=True)
    accession = models.CharField(max_length=20, default='', blank=True)
    gene_name = models.CharField(max_length=20, default='', blank=True)
    file_name = models.CharField(max_length=25, default='', blank=True)
    iso_type = models.CharField(max_length=15, default='', blank=True)
    validation_t = models.CharField(choices=(('Pass','Pass'), ('ND','ND'), ('Fail', 'Fail')), blank=True, max_length=10)
    validation_brib = models.CharField(choices=(('Pass','Pass'), ('ND','ND'), ('Fail', 'Fail')), blank=True, max_length=10)
    validation_brihc = models.CharField(choices=(('Pass','Pass'), ('ND','ND'), ('Fail', 'Fail')), blank=True, max_length=10)
    validation_ko = models.CharField(choices=(('Pass','Pass'), ('ND','ND'), ('Fail', 'Fail')), blank=True, max_length=10)
    tcsupe = models.CharField(max_length=25, default='', blank=True)
    pure = models.CharField(max_length=25, default='', blank=True)

class Entry(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='')
    vlseq = models.OneToOneField(VLSeq, on_delete=models.CASCADE, null=True)
    vhseq = models.OneToOneField(VHSeq, on_delete=models.CASCADE, null=True)
    metadata = models.OneToOneField(Metadata, on_delete=models.CASCADE, null=True)



class TrimmerEntry(models.Model):
    id = models.AutoField(primary_key=True)
    mabid = models.CharField(max_length=50, default='')


class TrimmerHeavy(models.Model):
    id = models.AutoField(primary_key=True)

    SMARTindex = models.CharField(max_length=20)
    pct_support = models.DecimalField(max_digits=10, decimal_places=5)
    asv_support = models.DecimalField(max_digits=10, decimal_places=5)
    total_reads = models.IntegerField()
    seq_platform = models.CharField(choices=(('Illumina','Illumina'),('Sanger','Sanger')), max_length=10)
    plate = models.CharField(max_length=30)
    seq = models.CharField(max_length=1500, default='')
    e_value = models.CharField(max_length=10, blank=True, null=True)
    score = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    seq_start_index = models.IntegerField(blank=True, null=True)
    seq_stop_index = models.IntegerField(blank=True, null=True)
    scheme = models.CharField(max_length=30, blank=True, null=True)
    frame = models.IntegerField(blank=True, null=True)
    aa = models.CharField(max_length=1000, blank=True, null=True)
    numbering = models.CharField(max_length=3000, blank=True, null=True)
    domain = models.CharField(max_length=1000, blank=True, null=True)

    entry = models.ForeignKey(TrimmerEntry, on_delete=models.CASCADE)


    @property
    def strip_domain(self):
        try:
            return TrimmerHeavy.objects.get(id=self.id).domain.replace(',', '')
        except:
            return ''

class TrimmerLight(models.Model):
    id = models.AutoField(primary_key=True)

    SMARTindex = models.CharField(max_length=20)
    pct_support = models.DecimalField(max_digits=10, decimal_places=5)
    asv_support = models.DecimalField(max_digits=10, decimal_places=5)
    total_reads = models.IntegerField()
    seq_platform = models.CharField(choices=(('Illumina','Illumina'),('Sanger','Sanger')), max_length=10)
    plate = models.CharField(max_length=30)
    seq = models.CharField(max_length=1500, default='')
    e_value = models.CharField(max_length=10, blank=True, null=True)
    score = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    seq_start_index = models.IntegerField(blank=True, null=True)
    seq_stop_index = models.IntegerField(blank=True, null=True)
    scheme = models.CharField(max_length=30, blank=True, null=True)
    frame = models.IntegerField(blank=True, null=True)
    aa = models.CharField(max_length=1000, blank=True, null=True)
    numbering = models.CharField(max_length=3000, blank=True, null=True)
    domain = models.CharField(max_length=1000, blank=True, null=True)

    entry = models.ForeignKey(TrimmerEntry, on_delete=models.CASCADE)

    @property
    def strip_domain(self):
        try:
            return TrimmerLight.objects.get(id=self.id).domain.replace(',', '')
        except:
            return ''


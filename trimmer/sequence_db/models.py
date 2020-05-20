from django.db import models

# Create your models here.

color_dict = {
    "R": "#E60606",
    "K": "#C64200",
    "Q": "#FF6600",
    "N": "#FF9900",
    "E": "#FFCC00",
    "D": "#FFCC99",
    "H": "#FFFF99",
    "P": "#FFFF00",
    "Y": "#CCFFCC",
    "W": "#CC99FF",
    "S": "#CCFF99",
    "T": "#00FF99",
    "G": "#00FF00",
    "A": "#CCFFFF",
    "M": "#99CCFF",
    "C": "#00FFFF",
    "F": "#00CCFF",
    "L": "#3366FF",
    "V": "#0000FF",
    "I": "#000080",
    "-": "#FFFFFF"

}

region_dict = {'HF': '#00FFFF', 'CDR': '#CCFF99'}


categories = {
    1: "NeuroMab IM subclones",
    2: "Non-NeuroMab High Priority Subclones",
    3: "NeuroMab Alternative Subclones",
    4: "High Priority Parents",
    5: "Other Parents",
              }

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
    show_on_web = models.BooleanField(default=True)
    category = models.IntegerField(blank=True, null=True)
    protein_target = models.CharField(max_length=100, blank=True, null=True)

    @property
    def get_category(self):
        return categories[self.category] if self.category != 'nan' and self.category else ''

    @property
    def get_protein_target(self):
        return self.protein_target if self.protein_target != 'nan' and self.protein_target else ''


    @property
    def heavy_duplicates(self):
        return TrimmerHeavy.objects.filter(entry__pk=self.pk, duplicate=True)

    @property
    def light_duplicates(self):
        return TrimmerLight.objects.filter(entry__pk=self.pk, duplicate=True)

    @property
    def heavy_count(self):
        return len(TrimmerHeavy.objects.filter(entry__pk=self.pk,  duplicate=False))

    @property
    def light_count(self):
        return len(TrimmerLight.objects.filter(entry__pk=self.pk,  duplicate=False))


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
    duplicate = models.BooleanField(default=False)
    entry = models.ForeignKey(TrimmerEntry, on_delete=models.CASCADE)

    @property
    def strip_domain(self):
        try:
            return TrimmerHeavy.objects.get(id=self.id).domain.replace(',', '')
        except:
            return ''

    @property
    def strip_aa(self):
        try:
            return TrimmerHeavy.objects.get(id=self.id).aa.replace('`', '')
        except:
            return ''

    @property
    def get_layout(self):
        try:
            return [{'numbering': x, 'domain': y, 'color': color_dict[y]} for x, y in zip(TrimmerHeavy.objects.get(id=self.id).numbering.split(','),
                                                                  TrimmerHeavy.objects.get(id=self.id).domain.replace(
                                                                      ',', ''))]
        except:
            return ''

    @property
    def get_region(self):
        try:
            return [{'range': 26, 'label': 'HFR1', 'color': region_dict['HF'],},
                    {'range': 12, 'label': 'CDR-H1', 'color': region_dict['CDR'],},
                    {'range': 17, 'label': 'HFR2', 'color': region_dict['HF'],},
                    {'range': 10, 'label': 'CDR-H2', 'color': region_dict['CDR'],},
                    {'range': 39, 'label': 'HFR3', 'color': region_dict['HF'],},
                    {'range': 13, 'label': 'CDR-H3', 'color': region_dict['CDR'],},
                    {'range': 11, 'label': 'HFR4', 'color': region_dict['HF'],}]
        except:
            return ''

    @property
    def get_table(self):
        try:
            return [{'range': '1-26', 'label': 'HFR1', 'splice': self.strip_domain[:26].replace('-', ''),  'color': region_dict['HF'],
                     'len_splice': len(self.strip_domain[:26].replace('-', ''))},
                    {'range': '27-38', 'label': 'CDR-H1', 'splice': self.strip_domain[26:38].replace('-', ''), 'color': region_dict['CDR'],
                     'len_splice': len(self.strip_domain[26:38].replace('-', ''))},
                    {'range': '39-55', 'label': 'HFR2', 'splice': self.strip_domain[38:55].replace('-', ''), 'color': region_dict['HF'],
                     'len_splice': len(self.strip_domain[38:55].replace('-', ''))},
                    {'range': '56-65', 'label': 'CDR-H2', 'splice': self.strip_domain[55:65].replace('-', ''), 'color': region_dict['CDR'],
                     'len_splice': len(self.strip_domain[55:65].replace('-', ''))},
                    {'range': '66-104', 'label': 'HFR3', 'splice': self.strip_domain[65:104].replace('-', ''), 'color': region_dict['HF'],
                     'len_splice': len(self.strip_domain[65:104].replace('-', ''))},
                    {'range': '105-117', 'label': 'CDR-H3', 'splice': self.strip_domain[104:117].replace('-', ''), 'color': region_dict['CDR'],
                     'len_splice': len(self.strip_domain[104:117].replace('-', ''))},
                    {'range': '118-128', 'label': 'HFR4', 'splice': self.strip_domain[117:128].replace('-', ''), 'color': region_dict['HF'],
                     'len_splice': len(self.strip_domain[117:128].replace('-', ''))}]
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
    duplicate = models.BooleanField(default=False)
    entry = models.ForeignKey(TrimmerEntry, on_delete=models.CASCADE)

    @property
    def strip_domain(self):
        try:
            return TrimmerLight.objects.get(id=self.id).domain.replace(',', '')
        except:
            return ''

    @property
    def strip_aa(self):
        try:
            return TrimmerLight.objects.get(id=self.id).aa.replace('`', '')
        except:
            return ''

    @property
    def get_layout(self):
        try:
            return [{'numbering': x, 'domain': y, 'color': color_dict[y]} for x,y in zip(TrimmerLight.objects.get(id=self.id).numbering.split(','),
                                                                 TrimmerLight.objects.get(id=self.id).domain.replace(',', ''))]
        except:
            return ''

    @property
    def get_region(self):
        try:
            return [{'range': 26, 'label': 'HFR1'}, {'range': 12, 'label': 'CDR-H1'},
                    {'range': 17, 'label': 'HFR2'}, {'range': 10, 'label': 'CDR-H2'}, {'range': 39, 'label': 'HFR3'},
                    {'range': 13, 'label': 'CDR-H3'}, {'range': 11, 'label': 'HFR4'}]
        except:
            return ''

    @property
    def get_table(self):
        try:
            return [{'range': '1-26', 'label': 'HFR1', 'splice': self.strip_domain[:26].replace('-', ''), 'len_splice': len(self.strip_domain[:26].replace('-', ''))},
                    {'range': '27-38', 'label': 'CDR-H1', 'splice': self.strip_domain[26:38].replace('-', ''), 'len_splice': len(self.strip_domain[26:38].replace('-', ''))},
                    {'range': '39-55', 'label': 'HFR2', 'splice': self.strip_domain[38:55].replace('-', ''), 'len_splice': len(self.strip_domain[38:55].replace('-', ''))},
                    {'range': '56-65', 'label': 'CDR-H2', 'splice': self.strip_domain[55:65].replace('-', ''), 'len_splice': len(self.strip_domain[55:65].replace('-', ''))},
                    {'range': '66-104', 'label': 'HFR3', 'splice': self.strip_domain[65:104].replace('-', ''), 'len_splice': len(self.strip_domain[65:104].replace('-', ''))},
                    {'range': '105-117', 'label': 'CDR-H3', 'splice': self.strip_domain[104:117].replace('-', ''), 'len_splice': len(self.strip_domain[104:117].replace('-', ''))},
                    {'range': '118-128', 'label': 'HFR4', 'splice': self.strip_domain[117:128].replace('-', ''), 'len_splice': len(self.strip_domain[117:128].replace('-', ''))}]
        except:
            return ''


class TrimmerEntryStatus(models.Model):
    id = models.AutoField(primary_key=True)
    entry = models.ForeignKey(TrimmerEntry, on_delete=models.CASCADE)

    sample_name = models.CharField(max_length=20)
    plate_location = models.CharField(max_length=5)
    volume = models.IntegerField()
    concentration = models.IntegerField()
    comments = models.CharField(max_length=50)
    amplicon_concentration = models.DecimalField(max_digits=10, decimal_places=2)
    failure = models.CharField(max_length=30)
    inline_index_name = models.CharField(max_length=30)
    inline_index = models.CharField(max_length=30)
    LCs_reported = models.IntegerField()
    HCs_reported = models.IntegerField()

    @property
    def plate_name(self):
        try:
            return TrimmerEntryStatus.objects.get(id=self.id).sample_name.split('_')[0]
        except:
            return ''


class Messages(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.CharField(max_length=400)

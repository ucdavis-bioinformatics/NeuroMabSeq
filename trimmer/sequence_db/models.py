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
    1: "NeuroMab mAbs",
    2: "Non-NeuroMab mAbs",
    3: "NeuroMab Alternative Subclones",
    4: "Lead oligoclonal Abs",
    5: "Other oligoclonal Abs",
    6: "Recombinant mAbs",
    7: "NeuroMab mAbs: commercially sequenced"
              }

heavy_increment = [
    {'range': '1-26', 'label': 'HFR1', 'splice': [0,26]},
    {'range': '27-38', 'label': 'CDR-H1', 'splice': [26,38]},
    {'range': '39-55', 'label': 'HFR2', 'splice': [38,55]},
    {'range': '56-65', 'label': 'CDR-H2', 'splice': [55,65]},
    {'range': '66-104', 'label': 'HFR3', 'splice': [65,104]},
    {'range': '105-117', 'label': 'CDR-H3', 'splice': [104,117]},
    {'range': '118-128', 'label': 'HFR4', 'splice': [117,128]},
                   ]

light_increment = [
    {'range': '1-26', 'label': 'LFR1', 'splice': [0,26]},
    {'range': '27-38', 'label': 'CDR-L1', 'splice': [26,38]},
    {'range': '39-55', 'label': 'LFR2', 'splice': [38,55]},
    {'range': '56-65', 'label': 'CDR-L2', 'splice': [55,65]},
    {'range': '66-104', 'label': 'LFR3', 'splice': [65,104]},
    {'range': '105-117', 'label': 'CDR-L3', 'splice': [104,117]},
    {'range': '118-128', 'label': 'LFR4', 'splice': [117,128]},
                   ]

def general_regions_function(object, type):
    if type == 'Heavy':
        increment = heavy_increment
    else:
        increment = light_increment
    regions_info = []
    for region in increment:
        new_dict = {}
        length = 0
        for number in object.numbering.split(','):

            if int(number) in [i for i in range(region['splice'][0] + 1, region['splice'][1] + 1)]:
                length += 1
        new_dict['length'] = length
        if 'CDR' in region['label']:
            new_dict['color'] = region_dict['CDR']
        else:
            new_dict['color'] = region_dict['HF']
        new_dict['label'] = region['label']
        regions_info.append(new_dict)
    return regions_info

def general_table(object, type):
    if type == 'Heavy':
        increment = heavy_increment
    else:
        increment = light_increment
    table_dict = []
    for region in increment:
        new_dict = {}
        length = 0
        new_splice = ''
        for number, aa in zip(object.numbering.split(','), object.domain.split(',')):
            if int(number) in [i for i in range(region['splice'][0] + 1, region['splice'][1] + 1)]:
                new_splice += aa
                length += 1
        if 'CDR' in region['label']:
            new_dict['color'] = region_dict['CDR']
        else:
            new_dict['color'] = region_dict['HF']
        new_dict['splice'] = new_splice.replace('-','')
        new_dict['len_splice'] = length
        new_dict['range'] = region['range']
        new_dict['label'] = region['label']


        table_dict.append(new_dict)

    return table_dict


# TODO delete
class VLSeq(models.Model):
    id = models.AutoField(primary_key=True)
    seq = models.CharField(max_length=1500, default='')

# TODO delete
class VHSeq(models.Model):
    id = models.AutoField(primary_key=True)
    seq = models.CharField(max_length=1500, default='')

# TODO delete
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

# TODO delete
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
    light_count = models.IntegerField(blank=True, null=True)
    heavy_count = models.IntegerField(blank=True, null=True)

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
    def get_url(self):
        return 'new_entry/' + str(self.pk)


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
    sample_name = models.CharField(max_length=20, default='')


    @property
    def strip_domain(self):
        try:
            return self.domain.replace(',', '')
        except:
            return ''

    @property
    def strip_aa(self):
        try:
            return self.aa.replace('`', '')
        except:
            return ''

    @property
    def get_layout(self):
        try:
            this = [{'numbering': x, 'domain': y, } for x, y in zip(self.numbering.split(','),
                                                                    self.domain.replace(',', ''))]
            return this
        except:
            return ''

    @property
    def get_region(self):
        try:
            return general_regions_function(self, 'Heavy')
        except:
            return ['error']

    @property
    def get_table(self):
        try:
            return general_table(self, 'Heavy')
        except:
            return ['error']

    @property
    def is_sanger(self):
        return self.seq_platform == 'Sanger'


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
    sample_name = models.CharField(max_length=20, default='')


    @property
    def strip_domain(self):
        try:
            return self.domain.replace(',', '')
        except:
            return ''

    @property
    def strip_aa(self):
        try:
            return self.aa.replace('`', '')
        except:
            return ''

    @property
    def get_layout(self):
        try:
            this = [{'numbering': x, 'domain': y, } for x,y in zip(self.numbering.split(','),
                                                                   self.domain.replace(',', ''))]
            return this
        except:
            return ''

    @property
    def get_region(self):
        try:
            return general_regions_function(self, 'Light')
        except:
            return ['error']

    @property
    def get_table(self):
        try:
            return general_table(self, 'Light')
        except:
            return ['error']

    @property
    def is_sanger(self):
        return self.seq_platform == 'Sanger'


class TrimmerEntryStatus(models.Model):
    id = models.AutoField(primary_key=True)
    entry = models.ForeignKey(TrimmerEntry, on_delete=models.CASCADE)

    sample_name = models.CharField(max_length=20)
    plate_location = models.CharField(max_length=5)
    volume = models.IntegerField(default=0)
    concentration = models.IntegerField(default=0)
    comments = models.CharField(max_length=50)
    amplicon_concentration = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    failure = models.CharField(max_length=30)
    inline_index_name = models.CharField(max_length=30)
    inline_index = models.CharField(max_length=30)
    LCs_reported = models.IntegerField(default=0)
    HCs_reported = models.IntegerField(default=0)

    @property
    def plate_name(self):
        try:
            return TrimmerEntryStatus.objects.get(id=self.id).sample_name.split('_')[0]
        except:
            return ''


class Messages(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.CharField(max_length=400)

class FilesProcessed(models.Model):
    id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=400)


class FAQ(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=4000)
    message = models.CharField(max_length=4000)
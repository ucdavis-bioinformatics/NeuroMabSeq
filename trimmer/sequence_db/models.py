from django.db import models
from django.contrib.auth.models import User

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

n_to_aa = {
        'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
        'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
        'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
        'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
        'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
        'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
        'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
        'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
        'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
        'TAC':'Y', 'TAT':'Y', 'TAA':'Stop', 'TAG':'Stop',
        'TGC':'C', 'TGT':'C', 'TGA':'Stop', 'TGG':'W',
    }

region_dict = {'HF': '#00FFFF', 'CDR': '#CCFF99'}

# if the key is < 10 need to add a 0 to the start though
well_dictionary = {str(key)+"-SMARTindex": value for key, value in zip([i for i in range(1,97)],
                                                    ["A1","B1","C1","D1","E1","F1","G1","H1",
                                                     "A2","B2","C2","D2","E2","F2","G2","H2",
                                                     "A3","B3","C3","D3","E3","F3","G3","H3",
                                                     "A4","B4","C4","D4","E4","F4","G4","H4",
                                                     "A5","B5","C5","D5","E5","F5","G5","H5",
                                                     "A6","B6","C6","D6","E6","F6","G6","H6",
                                                     "A7","B7","C7","D7","E7","F7","G7","H7",
                                                     "A8","B8","C8","D8","E8","F8","G8","H8",
                                                     "A9","B9","C9","D9","E9","F9","G9","H9",
                                                     "A10","B10","C10","D10","E10","F10","G10","H10",
                                                     "A11","B11","C11","D11","E11","F11","G11","H11",
                                                     "A12","B12","C12","D12","E12","F12","G12","H12",])}

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
        for number, domain in zip(object.numbering.split(','), object.domain.split(",")):
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
    # expected length and actual length
    if type == 'Heavy':
        increment = heavy_increment
    else:
        increment = light_increment
    table_dict = []
    for region in increment:
        new_dict = {}
        length = 0
        max_len = 0
        new_splice = ''
        for number, aa in zip(object.numbering.split(','), object.domain.split(',')):
            if int(number) in [i for i in range(region['splice'][0] + 1, region['splice'][1] + 1)]:
                new_splice += aa
                if aa != "-":
                    length += 1
                max_len += 1
        if 'CDR' in region['label']:
            new_dict['color'] = region_dict['CDR']
        else:
            new_dict['color'] = region_dict['HF']
        new_dict['splice'] = new_splice.replace('-','')
        new_dict['len_splice'] = length
        new_dict['region_max_len'] = max_len
        new_dict['range'] = region['range']
        new_dict['label'] = region['label']


        table_dict.append(new_dict)

    return table_dict


class TrimmerEntry(models.Model):
    sample_name = models.CharField(max_length=20)
    id = models.AutoField(primary_key=True)
    mabid = models.CharField(max_length=50, default='')
    show_on_web = models.BooleanField(default=False)
    category = models.IntegerField(blank=True, null=True)
    protein_target = models.CharField(max_length=100, blank=True, null=True)
    light_count = models.IntegerField(blank=True, null=True)
    heavy_count = models.IntegerField(blank=True, null=True)
    clonality = models.CharField(choices=(('Monoclonal','Monoclonal'),
                                          ('Oligoclonal','Oligoclonal')), max_length=12, default="")
    max_lcstars = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    max_hcstars = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    maxavgstars = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    contains_verified = models.BooleanField(default=False)
    contains_failed = models.BooleanField(default=False)

    @property
    def get_count(self):
        return TrimmerEntry.objects.filter(mabid=self.mabid).count()

    @property
    def get_category(self):
        return categories[self.category] if self.category != 'nan' and self.category else ''

    @property
    def get_protein_target(self):
        return self.protein_target if self.protein_target != 'nan' and self.protein_target else ''


    @property
    def heavy_duplicates(self):
        return TrimmerSequence.objects.filter(entry__pk=self.pk,
                                              anarci_bad=False,
                                              anarci_duplicate=True,
                                              bad_support=False,
                                              chain="Heavy").order_by('asv_support')

    @property
    def light_duplicates(self):
        return TrimmerSequence.objects.filter(entry__pk=self.pk,
                                              anarci_bad=False,
                                              anarci_duplicate=True,
                                              bad_support=False,
                                              chain="Heavy").order_by('asv_support')

    @property
    def new_heavy_count(self):
        return len(TrimmerSequence.objects.filter(entry__pk=self.pk,
                                                  anarci_bad=False,
                                                  anarci_duplicate=False,
                                                  bad_support=False,
                                                  chain="Heavy"))

    @property
    def new_light_count(self):
        return len(TrimmerSequence.objects.filter(entry__pk=self.pk,
                                                  anarci_bad=False,
                                                  anarci_duplicate=False,
                                                  bad_support=False,
                                                  chain="Light"))

    @property
    def get_url(self):
        return 'new_entry/' + str(self.pk)

    # @property
    # def clonality(self):
    #     if self.entry.category in [4,5]:
    #         return "Oligoclonal"
    #     else:
    #         return "Monoclonal"

    def __str__(self):
        return '%s' % (self.mabid)


def translate_seq(
        seq: str,
        aa: str,
):
    aa_comp = []
    for i in range(0,len(aa)):
        if n_to_aa[seq[i*3:i*3+3]] == "Stop":
            break
        else:
            aa_comp.append(n_to_aa[seq[i*3:i*3+3]])
    return ''.join(aa_comp) == aa


class TrimmerSequence(models.Model):
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
    chain = models.CharField(choices=(("Light", "Light"),("Heavy", "Heavy")), max_length=10)
    asv_order = models.IntegerField(blank=True, null=True)
    chain_id = models.CharField(max_length=25, default='')
    anarci_bad = models.BooleanField(default=False)
    anarci_duplicate = models.BooleanField(default=False)
    bad_support = models.BooleanField(default=False)
    subseqs = models.IntegerField(blank=True, null=True)
    stars = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    asv_stars = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    duplicate_stars = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    verified = models.BooleanField(default=False)
    failed = models.BooleanField(default=False)

    @property
    def well_from_smartindex(self):
        # remove the leading 0 if it exist:
        try:
            if self.SMARTindex[0] == '0':
                return well_dictionary[self.SMARTindex[1:]]
            else:
                return well_dictionary[self.SMARTindex]
        except KeyError:
            return ''
    
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
            return general_regions_function(self, self.chain)
        except:
            return ['error']

    @property
    def get_table(self):
        try:
            return general_table(self, self.chain)
        except:
            return ['error']

    @property
    def is_sanger(self):
        return self.seq_platform == 'Sanger'

    @property
    def run_anarci(self):
        import subprocess
        """Run ANARCI program and parse results into a dictionary. Return FIRST hit."""
        result = None
        aa = self.strip_aa
        # Parse the aa into each sub-piece that doesn't have a stop codon:
        # TODO
        subAAs = str(aa).strip('X').split('*')
        for i in range(len(subAAs)):
            s = subAAs[i]
            if (len(s) > 0):
                cmd = "anarci" + " --scheme imgt -i " + s
                test = subprocess.run(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                      universal_newlines=True)
                output = test.stdout.splitlines()
                if len(output) > 2:
                    result = {}
                    mcols = output[4].split('|')
                    mdata = output[5].split('|')
                    result['chain_type'] = mdata[mcols.index('chain_type')]
                    result['e-value'] = mdata[mcols.index('e-value')]
                    result['score'] = mdata[mcols.index('score')]
                    result['seqstart_index'] = mdata[mcols.index('seqstart_index')]
                    result['seqend_index'] = mdata[mcols.index('seqend_index')]
                    result['scheme'] = output[6].split('=')[1].strip()
                    splitAA = s[0:int(result['seqstart_index'])]
                    splitAA += '`' + s[int(result['seqstart_index']):int(result['seqend_index'])] + '`'
                    splitAA += s[int(result['seqend_index']):]
                    subAAs[i] = splitAA
                    #result['frame'] = frame
                    result['AA'] = '*'.join(subAAs)
                    result['numbering'] = []
                    result['domain'] = []
                    for l in output[7:]:
                        if l != '//':
                            result['numbering'] += [l.strip().split()[1]]
                            result['domain'] += [l.strip().split()[-1]]
                    result['numbering'] = ','.join(result['numbering'])
                    result['domain'] = ','.join(result['domain'])
                    break
        #print(result)
        return result

    @property
    def vector_sequence(self):
        try:
            find_dom_in_aa = self.strip_aa.find(self.strip_domain.replace("-",""))
            end_spot = len(self.strip_domain.replace("-","")) + find_dom_in_aa
            # make sure always aaa at the end and 6 nts being stripped at the end
            # check each of the ORF spots
            # TODO make this just an iteration of whole thing
            for i in range(-3,6):
                if translate_seq(seq=self.seq[find_dom_in_aa*3+i:end_spot*3+i], aa=self.strip_domain.replace("-","")):
                    # print(self.seq[find_dom_in_aa*3+i:end_spot*3+i],
                    #       self.strip_domain.replace("-", "")
                    #       )
                    # print(len(self.seq[find_dom_in_aa*3+i:end_spot*3+i]),
                    #       len(self.strip_domain.replace("-", ""))
                    #       )
                    return self.seq[find_dom_in_aa*3+i:end_spot*3+i]

        except:
            return "Failed"

#

# class TrimmerHeavy(models.Model):
#     id = models.AutoField(primary_key=True)
#     SMARTindex = models.CharField(max_length=20)
#     pct_support = models.DecimalField(max_digits=10, decimal_places=5)
#     asv_support = models.DecimalField(max_digits=10, decimal_places=5)
#     total_reads = models.IntegerField()
#     seq_platform = models.CharField(choices=(('Illumina','Illumina'),('Sanger','Sanger')), max_length=10)
#     plate = models.CharField(max_length=30)
#     seq = models.CharField(max_length=1500, default='')
#     e_value = models.CharField(max_length=10, blank=True, null=True)
#     score = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     seq_start_index = models.IntegerField(blank=True, null=True)
#     seq_stop_index = models.IntegerField(blank=True, null=True)
#     scheme = models.CharField(max_length=30, blank=True, null=True)
#     frame = models.IntegerField(blank=True, null=True)
#     aa = models.CharField(max_length=1000, blank=True, null=True)
#     numbering = models.CharField(max_length=3000, blank=True, null=True)
#     domain = models.CharField(max_length=1000, blank=True, null=True)
#     duplicate = models.BooleanField(default=False)
#     entry = models.ForeignKey(TrimmerEntry, on_delete=models.CASCADE)
#     sample_name = models.CharField(max_length=20, default='')
#
#
#     @property
#     def strip_domain(self):
#         try:
#             return self.domain.replace(',', '')
#         except:
#             return ''
#
#     @property
#     def strip_aa(self):
#         try:
#             return self.aa.replace('`', '')
#         except:
#             return ''
#
#     @property
#     def get_layout(self):
#         try:
#             this = [{'numbering': x, 'domain': y, } for x, y in zip(self.numbering.split(','),
#                                                                     self.domain.replace(',', ''))]
#             return this
#         except:
#             return ''
#
#     @property
#     def get_region(self):
#         try:
#             return general_regions_function(self, 'Heavy')
#         except:
#             return ['error']
#
#     @property
#     def get_table(self):
#         try:
#             return general_table(self, 'Heavy')
#         except:
#             return ['error']
#
#     @property
#     def is_sanger(self):
#         return self.seq_platform == 'Sanger'
#
#
# class TrimmerLight(models.Model):
#     id = models.AutoField(primary_key=True)
#     SMARTindex = models.CharField(max_length=20)
#     pct_support = models.DecimalField(max_digits=10, decimal_places=5)
#     asv_support = models.DecimalField(max_digits=10, decimal_places=5)
#     total_reads = models.IntegerField()
#     seq_platform = models.CharField(choices=(('Illumina','Illumina'),('Sanger','Sanger')), max_length=10)
#     plate = models.CharField(max_length=30)
#     seq = models.CharField(max_length=1500, default='')
#     e_value = models.CharField(max_length=10, blank=True, null=True)
#     score = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     seq_start_index = models.IntegerField(blank=True, null=True)
#     seq_stop_index = models.IntegerField(blank=True, null=True)
#     scheme = models.CharField(max_length=30, blank=True, null=True)
#     frame = models.IntegerField(blank=True, null=True)
#     aa = models.CharField(max_length=1000, blank=True, null=True)
#     numbering = models.CharField(max_length=3000, blank=True, null=True)
#     domain = models.CharField(max_length=1000, blank=True, null=True)
#     duplicate = models.BooleanField(default=False)
#     entry = models.ForeignKey(TrimmerEntry, on_delete=models.CASCADE)
#     sample_name = models.CharField(max_length=20, default='')
#
#
#     @property
#     def strip_domain(self):
#         try:
#             return self.domain.replace(',', '')
#         except:
#             return ''
#
#     @property
#     def strip_aa(self):
#         try:
#             return self.aa.replace('`', '')
#         except:
#             return ''
#
#     @property
#     def get_layout(self):
#         try:
#             this = [{'numbering': x, 'domain': y, } for x,y in zip(self.numbering.split(','),
#                                                                    self.domain.replace(',', ''))]
#             return this
#         except:
#             return ''
#
#     @property
#     def get_region(self):
#         try:
#             return general_regions_function(self, 'Light')
#         except:
#             return ['error']
#
#     @property
#     def get_table(self):
#         try:
#             return general_table(self, 'Light')
#         except:
#             return ['error']
#
#     @property
#     def is_sanger(self):
#         return self.seq_platform == 'Sanger'


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
    is_definition = models.BooleanField(default=False)
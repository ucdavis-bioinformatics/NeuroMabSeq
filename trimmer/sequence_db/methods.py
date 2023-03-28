from .models import *
import pandas as pd
import os
import math
## To run
# python manage.py shell
# from sequence_db.methods import *
from multiprocessing.dummy import Pool as ThreadPool


# todo just run this all on entry
def group_objects(entry):
    for chain_type in ["Light", "Heavy"]:
        seqs = TrimmerSequence.objects.filter(entry__show_on_web=True,
                                              entry__pk=entry.pk,
                                              chain=chain_type,
                                              # sketchy to have this?
                                              anarci_duplicate=False).order_by('asv_order')
        if not entry.pk % 100:
            print(f"{chain_type}-{entry.pk}")

        #imgt_aa_acid_seqs = [i.strip_domain for i in light_seqs]
        #if len(imgt_aa_acid_seqs) != len(set(imgt_aa_acid_seqs)):
        seq_dict = {}
        seq_count = {}
        pk_dict = {}
        final = []
        # here we get the ones that match and group them
        # todo make this pandas eventually
        for item in seqs:
            # this should update strip domain
            item.domain = item.run_anarci["domain"]
            item.numbering = item.run_anarci["numbering"]
            if item.strip_domain in seq_dict.keys():
                seq_dict[item.strip_domain] += item.asv_support
                seq_count[item.strip_domain] += 1
                item.anarci_duplicate = True
            else:
                seq_dict[item.strip_domain] = item.asv_support
                seq_count[item.strip_domain] = 1
                #pk_dict [item.strip_domain]
                final.append(item)
            item.save()
        update_final = []
        # todo add substrings or subsequences/results for some
        # seen mabs with identical mab id
        # subclones should be same category, everything before / in theory all targets same protein

        # next we get the ones that have bad characteristics and get rid of those
        for item in final:
            keep = True
            item.asv_support = seq_dict[item.strip_domain]
            item.subseqs = seq_count[item.strip_domain]
            table = general_table(item, chain_type)
            # not have a region (FR or CDR) with 0 length, dont keep if missing
            for region in table:
                if region["len_splice"] == 0:
                    keep = False
                    item.anarci_bad = True
            # stop or start missing 10 elements from FR 1 or 4 then bad sign too
            if item.strip_domain[-10:] == "----------" or item.strip_domain[:10] == "----------":
                keep = False
                item.anarci_bad = True

            # lets go with a 10% cutoff for now
            if item.asv_support/item.total_reads < 0.1:
                # keep = False
                # update_final.append(item)
                # TODO make this a seperate flag
                item.bad_support = True
            item.save()
        if chain_type == "Light":
            entry.light_count = entry.new_light_count
        if chain_type == "Heavy":
            entry.heavy_count = entry.new_heavy_count
        entry.save()


def run_all_entry_group():
    all_entries = TrimmerEntry.objects.filter(show_on_web=True)
    print("Fixing Anarci Sequences")
    pool = ThreadPool(20)
    results = pool.map(group_objects, all_entries)


# this is called in the wipe_db.py script
def clear_new_data_upload():
    TrimmerEntry.objects.all().delete()
    TrimmerSequence.objects.all().delete()

# this is called in the wipe_status_data.py script
def clear_status_data():
    TrimmerEntryStatus.objects.all().delete()


def check_file_entries(filename):
    try:
        file_processed = FilesProcessed.objects.get(message=filename)
        if file_processed:
            return True
        else:
            return False
    except:
        return False


def get_data_base_dir():
    homedir = os.environ['HOME']
    if 'ubuntu' in homedir:
        return True
    else:
        return False

########################################################################################################################
# BLAT  (see generate_blat.py and reset_db.sh and update_db.sh)
########################################################################################################################
def get_header(chain, type):
    try:
        result = '>' + '_'.join([str(chain.id),
                               chain.entry.mabid.replace(' ',':'),
                               str(chain.entry.id),
                               chain.entry.protein_target.replace(' ',':'),
                               categories[chain.entry.category].replace(' ',':'),
                               type,
                               str(chain.chain_id),
                               str(chain.entry.clonality)]) + '\n'
        return result
    except Exception as error:
        cwd = os.getcwd()
        prefix = '/'.join(cwd.split('/')[:-1])
        if "ubuntu" in prefix:
            pass
        else:
            print(error)
            print(chain.__dict__)
        return None


#TODO update this now that they are the same
def get_list(heavy_chains, light_chains, type):
    seq_list = []
    for item in heavy_chains:
        if getattr(item, type):
            if get_header(item, 'Heavy'):
                seq_list.append(get_header(item, 'Heavy'))
                seq_list.append(getattr(item, type) + '\n')
    for item in light_chains:
        if getattr(item, type):
            if get_header(item, 'Light'):
                seq_list.append(get_header(item, 'Light'))
                seq_list.append(getattr(item, type) + '\n')
    return seq_list

def generate_seq_fa():
    all_heavy_chains = TrimmerSequence.objects.filter(entry__show_on_web=True,
                                                      chain="Heavy",
                                                      anarci_bad=False,
                                                      anarci_duplicate=False,
                                                      bad_support=False).exclude(aa='-')
    all_light_chains = TrimmerSequence.objects.filter(entry__show_on_web=True,
                                                      chain="Light",
                                                      anarci_bad=False,
                                                      anarci_duplicate=False,
                                                      bad_support=False).exclude(aa='-')
    seq_list = get_list(all_heavy_chains, all_light_chains, 'seq')
    with open('../static_data/dna.fa','w') as dna_fa_out:
        for item in seq_list:
            dna_fa_out.write(item)

def generate_aa_fa():
    all_heavy_chains = TrimmerSequence.objects.filter(entry__show_on_web=True,
                                                      chain="Heavy",
                                                      anarci_bad=False,
                                                      anarci_duplicate=False,
                                                      bad_support=False).exclude(aa='-')
    all_light_chains = TrimmerSequence.objects.filter(entry__show_on_web=True,
                                                      chain="Light",
                                                      anarci_bad=False,
                                                      anarci_duplicate=False,
                                                      bad_support=False).exclude(aa='-')

    aa_list = get_list(all_heavy_chains, all_light_chains, 'strip_aa')
    with open('../static_data/protein.fa','w') as dna_fa_out:
        for item in aa_list:
            dna_fa_out.write(item)

########################################################################################################################
# FAQ
########################################################################################################################
def generate_faq():
    with open("/Users/keithmitchell/Desktop/Repositories/NeuroMabSeq/static_data/faq/faq.tsv") as faq_file:
        for line in faq_file:
            line = line.replace('\n', '')
            line = line.split('\t')
            if line[2] == "Definition":
                is_def = True
            else:
                is_def = False
            new_faq = FAQ.objects.create(message=line[1], question=line[0], is_definition=is_def)
            new_faq.save()


########################################################################################################################
# NEW NEW ENTRY STUFF
########################################################################################################################
def new_create_entries(entry_list, row, duplicate, sanger):
    for value in entry_list:
        if sanger:
            row['SMARTindex'] = "None"
            row['ASVcount'] = 1
        if row['Chain'] == 'LC':
            chain_type = 'Light'
        else:
            chain_type = 'Heavy'
        if row['e.value'] != '-':
            create =TrimmerSequence.objects.create(entry=value,
                                                   SMARTindex=row['SMARTindex'],
                                                   pct_support=row['PctSupport'],
                                                   asv_support=row['ASVcount'],
                                                   total_reads=row['TotalReads'],
                                                   seq_platform=row['Sequencing'],
                                                   plate=row['plate'],
                                                   seq=row['ASV'],
                                                   e_value=row['e.value'],
                                                   score=row['score'],
                                                   seq_start_index=row['seqstart_index'],
                                                   seq_stop_index=row['seqend_index'],
                                                   scheme=row['scheme'],
                                                   frame=row['frame'],
                                                   aa=row['AA'],
                                                   numbering=row['numbering'],
                                                   domain=row['domain'],
                                                   duplicate=duplicate,
                                                   sample_name = row['Sample_Name'],
                                                   chain = chain_type,
                                                   chain_id = row['ChainID']
                                                )
        else:
            create = TrimmerSequence.objects.create(entry=value,
                                                           SMARTindex=row['SMARTindex'],
                                                           pct_support=row['PctSupport'],
                                                           asv_support=row['ASVcount'],
                                                           total_reads=row['TotalReads'],
                                                           seq_platform=row['Sequencing'],
                                                           plate=row['plate'],
                                                           seq=row['ASV'],
                                                           duplicate=duplicate,
                                                           sample_name=row['Sample_Name'],
                                                           chain = chain_type,
                                                           chain_id = row['ChainID']

            )
        create.save()



# def get_entries_light_and_heavy(light, heavy):
#     entry_list = []
#     for i in light:
#         entry_list.append(i.entry)
#     for x in heavy:
#         if x not in entry_list:
#             entry_list.append(x.entry)
#     return entry_list


# this is called in the run_update.py script and the run_entry_reset.py
def data_upload(update, dir):
    # update is false when reseting otherwise it is True
    # TODO function that get directory based on if AWS server or local or just pass diretory.
    dir += "/"
    files = os.listdir(dir)
    files = [i for i in files if ".tsv" in i]
    #files = [i for i in files if " " not in i]

    for file in files:

        file = dir+file
        result = pd.read_csv(file, delimiter='\t', index_col=False)
        result = result.to_dict(orient='records')
        print(file)
        if "Sanger" in file:
            sanger = True
        else:
            sanger = False

        for row, num in zip(result, range(1,len(result)+1)):
            try:
                entry = TrimmerEntry.objects.get(sample_name=row['Sample_Name'])

                # if we are updating we wont iterate through the whole file where we already have sample_names
                # only exception is if sanger is True then we dont want to break because AddGene are added here

            except:
                entry = None

            if update and entry:
                print ("Next file")
                break

            if not entry:
                entry_create = TrimmerEntry.objects.create(sample_name=row['Sample_Name'])
                entry_create.save()
                entry = entry_create
            entry_list = []
            entry_list.append(entry)
            new_create_entries(entry_list, row, False, sanger)

        # # TODO fix this as this as it is based on plate_well for duplicated on now... also do we use this at all??
        # for row, num in zip(result, range(1,len(result)+1)):
        #
        #
        #     if update and entry and not sanger:
        #         break
        #
        #     entry_list = []
        #     if isinstance(row['DuplicatedIn'], str):
        #         for x in row['DuplicatedIn'].split(','):
        #             # try:
        #             #     entry_list.append(TrimmerEntry.objects.get(mabid=x.replace(' ', '')))
        #             # except:
        #             #     print("The Duplicate mabID does not exist: %s" % x.replace(' ', ''))
        #             light_entry = TrimmerLight.objects.filter(sample_name=x.replace(' ', ''))
        #             heavy_entry = TrimmerHeavy.objects.filter(sample_name=x.replace(' ', ''))
        #
        #             if not light_entry and not heavy_entry:
        #                 print("The Duplicate plate_name does not exist: %s" % x.replace(' ', ''))
        #             entry_list = get_entries_light_and_heavy(light_entry, heavy_entry)
        #     # fake_smart_index = new_get_fake_smart(num, sanger)
        #     new_create_entries(entry_list, row, True, sanger)


def seq_count(entry, chain_type):
    return len(TrimmerSequence.objects.filter(entry__pk=entry.pk,
                                              duplicate=False,
                                              chain=chain_type,
                                              anarci_bad=False,
                                              anarci_duplicate=False,
                                              ))


def assign_order(seqs, chain_type):
    for i in seqs:
        i.asv_order = int(i.chain_id.split(chain_type)[1])
        i.save()


def update_order(entry):
    light_seqs = TrimmerSequence.objects.filter(entry__pk=entry.pk,
                                                duplicate=False,
                                                chain="Light",
                                                anarci_bad=False,
                                                anarci_duplicate=False).exclude(aa='-')
    heavy_seqs = TrimmerSequence.objects.filter(entry__pk=entry.pk,
                                                duplicate=False,
                                                chain="Heavy",
                                                anarci_bad=False,
                                                anarci_duplicate=False).exclude(aa='-')
    assign_order(light_seqs, "LC")
    assign_order(heavy_seqs, "HC")


def get_light_and_heavy_per_entry():
    for item in TrimmerEntry.objects.all():
        item.light_count = seq_count(item, "Light")
        item.heavy_count = seq_count(item, "Heavy")
        update_order(item)
        item.save()


########################################################################################################################
# STATUS STUFF
########################################################################################################################


# TODO this and function below are a bit reducnd
def new_create_status(row, entry):

    if entry:
        status_create = TrimmerEntryStatus.objects.create(entry=entry,
                                                            sample_name = row['sample_name'],
                                                            plate_location = row['plate_location'],
                                                            volume = row['volume'],
                                                            concentration = row['concentration'],
                                                            comments = row['comments'],
                                                            amplicon_concentration = 0 if math.isnan(row['LCs.Reported']) else row['LCs.Reported'],
                                                            failure = row['failure'],
                                                            inline_index_name = row['inline_index_name'],
                                                            inline_index = row['inline_index'],
                                                            LCs_reported = 0 if math.isnan(row['LCs.Reported']) else row['LCs.Reported'],
                                                            HCs_reported = 0 if math.isnan(row['HCs.Reported']) else row['HCs.Reported']
                                                            )

        status_create.save()



# status upload. Works the same whether updating or not.
def status_upload(update, dir):
    dir += "/StatusReports/"
    files = os.listdir(dir)
    files = [i for i in files if ".tsv" in i]
    files = [i for i in files if " " not in i]

    not_found_list = []

    for file in files:
        file = dir+file
        if "Sanger" in file:
            sanger = True
        else:
            sanger = False
        result = pd.read_csv(file, delimiter='\t', index_col=False)
        result = result.to_dict(orient='records')
        # check if a light file and do same processing for Trimmer Light entry
        for row in result:
            try:
                entry = TrimmerEntry.objects.get(sample_name=row['sample_name'])
            except:
                not_found_list.append(row['sample_name'])
                entry = None

            if update and entry and not sanger:
                print ("Next file")
                break

            new_create_status(row, entry)
    return not_found_list

########################################################################################################################
# METADATA STUFF
########################################################################################################################

def new_update_entry(entry, row):
    if entry.mabid != row['trimmer_id']:
        string = "The mabID %s has been updated to %s." %(entry.mabid, row['trimmer_id'])
        message = Messages.objects.create(message=string)
        message.save()
    entry.category = row['Category'] if str(row['Category']) != 'nan' else None
    if entry.category in [4, 5]:
        entry.clonality = "Oligoclonal"
    else:
        entry.clonality = "Monoclonal"
    entry.protein_target = row['ProteinTarget']
    entry.show_on_web = False if row['ShowOnWeb'] == 'F' else True
    entry.mabid = row['trimmer_id']
    try:
        entry.save()
    except:
        print(entry.__dict__)

# TODO delete all message by default each time this is ran
# TODO make this a try and except
def new_metadata_upload(filename=None):
    # print(mapping)
    if filename == None:
        dir = "../static_data/"
        files = sorted(os.listdir(dir))
        files = [dir + i for i in files if ".tsv" in i]

    else:
        files = [filename,]

    for file in files:
        result = pd.read_csv(file, delimiter='\t', index_col=False)
        result = result.to_dict(orient='records')
        for row in result:
            light_entries = []
            heavy_entries = []
            if row['sample_name'] != 'None' and row['sample_name'] != 0 and '_' in row['sample_name']:
                # well = row['sample_name'].split('_')[1]
                # plate = 'plate' + row['sample_name'].split('_')[0][1:]
                light_entries = TrimmerSequence.objects.filter(sample_name=row['sample_name'],
                                                               chain="Light",
                                                               anarci_bad=False,
                                                               bad_support=False,
                                                               anarci_duplicate=False,
                                                               )
                heavy_entries = TrimmerSequence.objects.filter(sample_name=row['sample_name'],
                                                               chain="Heavy",
                                                               anarci_bad=False,
                                                               bad_support=False,
                                                               anarci_duplicate=False,
                                                               )

            if len(light_entries):
                entry = light_entries[0].entry
                new_update_entry(entry, row)
            elif len(heavy_entries):
                entry = heavy_entries[0].entry
                new_update_entry(entry, row)
            else:
                string = "Unable to update the metadata for this sample name: %s" % row['sample_name']
                message = Messages.objects.create(message=string)
                message.save()


def metadata_file_process(context, filename):
    new_metadata_upload(filename=filename)
    generate_aa_fa()
    generate_seq_fa()

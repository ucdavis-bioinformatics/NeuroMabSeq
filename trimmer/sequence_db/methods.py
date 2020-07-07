from .models import *
import pandas as pd
import os
import math
## To run
# python manage.py shell
# from sequence_db.methods import *

# this is called in the wipe_db.py script
def clear_new_data_upload():
    TrimmerEntry.objects.all().delete()
    TrimmerLight.objects.all().delete()
    TrimmerHeavy.objects.all().delete()

# this is called in the wipe_status_data.py script
def clear_status_data():
    TrimmerEntryStatus.objects.all().delete()


########################################################################################################################
# NEW NEW ENTRY STUFF
########################################################################################################################
def new_create_entries(entry_list, row, duplicate, sanger, fake_smart_index):
    for value in entry_list:
        if sanger:
            row['SMARTindex'] = fake_smart_index
            row['ASVcount'] = 1
        if row['Chain'] == 'LC':
            chain_type = 'Light'
        else:
            chain_type = 'Heavy'
        if row['e-value'] != '-':
            create = eval("Trimmer" + chain_type).objects.create(entry=value,
                                                               SMARTindex=row['SMARTindex'],
                                                               pct_support=row['PctSupport'],
                                                               asv_support=row['ASVcount'],
                                                               total_reads=row['TotalReads'],
                                                               seq_platform=row['Sequencing'],
                                                               plate=row['plate'],
                                                               seq=row['ASV'],
                                                               e_value=row['e-value'],
                                                               score=row['score'],
                                                               seq_start_index=row['seqstart_index'],
                                                               seq_stop_index=row['seqend_index'],
                                                               scheme=row['scheme'],
                                                               frame=row['frame'],
                                                               aa=row['AA'],
                                                               numbering=row['numbering'],
                                                               domain=row['domain'],
                                                               duplicate=duplicate,
                                                               sample_name = row['Sample_Name']
                                                            )
        else:
            create = eval("Trimmer" + chain_type).objects.create(entry=value,
                                                           SMARTindex=row['SMARTindex'],
                                                           pct_support=row['PctSupport'],
                                                           asv_support=row['ASVcount'],
                                                           total_reads=row['TotalReads'],
                                                           seq_platform=row['Sequencing'],
                                                           plate=row['plate'],
                                                           seq=row['ASV'],
                                                           duplicate=duplicate,
                                                           sample_name=row['Sample_Name']
                                                           )
        create.save()



def new_get_fake_smart(num, sanger):
    if sanger:
        fake_smart_index = str(num) + '-SMARTindex'
    else:
        fake_smart_index = ''
    return fake_smart_index

def get_entries_light_and_heavy(light, heavy):
    entry_list = []
    for i in light:
        entry_list.append(i.entry)
    for x in heavy:
        if x not in entry_list:
            entry_list.append(x.entry)
    return entry_list

# this is called in the run_update.py script
def new_new_data_upload():
    dir = "/Users/keithmitchell/Desktop/Repositories/NeuroMabSeq/data2/AnnotatedResults/"
    files = os.listdir(dir)
    files = [i for i in files if ".tsv" in i]
    files = [i for i in files if " " not in i]

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
                entry = TrimmerEntry.objects.get(mabid=row['MabID'])
            except:
                entry = None
            if not entry:
                entry_create = TrimmerEntry.objects.create(mabid=row['MabID'])
                entry_create.save()
                entry = entry_create
            fake_smart_index = new_get_fake_smart(num, sanger)
            entry_list = []
            entry_list.append(entry)
            new_create_entries(entry_list, row, False, sanger, fake_smart_index)

        # todo fix this as this as it is based on plate_well for duplicated on now.
        for row, num in zip(result, range(1,len(result)+1)):
            entry_list = []
            if isinstance(row['DuplicatedIn'], str):
                for x in row['DuplicatedIn'].split(','):
                    # try:
                    #     entry_list.append(TrimmerEntry.objects.get(mabid=x.replace(' ', '')))
                    # except:
                    #     print("The Duplicate mabID does not exist: %s" % x.replace(' ', ''))
                    light_entry = TrimmerLight.objects.filter(sample_name=x.replace(' ', ''))
                    heavy_entry = TrimmerHeavy.objects.filter(sample_name=x.replace(' ', ''))

                    if not light_entry and not heavy_entry:
                        print("The Duplicate plate_name does not exist: %s" % x.replace(' ', ''))
                    entry_list = get_entries_light_and_heavy(light_entry, heavy_entry)
            fake_smart_index = new_get_fake_smart(num, sanger)
            new_create_entries(entry_list, row, True, sanger, fake_smart_index)


def heavy_count(entry):
    return len(TrimmerHeavy.objects.filter(entry__pk=entry.pk,  duplicate=False))


def light_count(entry):
    return len(TrimmerLight.objects.filter(entry__pk=entry.pk,  duplicate=False))


def get_light_and_heavy_per_entry():
    for item in TrimmerEntry.objects.all():
        item.light_count = light_count(item)
        item.heavy_count = heavy_count(item)
        item.save()


########################################################################################################################
# NEW NEW STATUS STUFF
########################################################################################################################

def status_not_present():
    dir = "../data2/StatusReports/"
    files = os.listdir(dir)
    files = [i for i in files if ".tsv" in i]
    files = [i for i in files if " " not in i]
    not_found_list = []
    for file in files:
        file = dir + file
        result = pd.read_csv(file, delimiter='\t', index_col=False)
        result = result.to_dict(orient='records')
        # check if a light file and do same processing for Trimmer Light entry
        for row in result:
            if str(row['trimmer_id']) != 'nan':
                try:
                    entry = TrimmerEntry.objects.get(mabid=row['trimmer_id'])
                except:
                    not_found_list.append([row['trimmer_id'], row['sample_name']])
                    entry = None

    return not_found_list


# TODO this and function below are a bit reducnd
def new_create_status(row, partial):
    not_found_list = []
    light_entry = TrimmerLight.objects.filter(sample_name=row['sample_name'])
    heavy_entry = TrimmerHeavy.objects.filter(sample_name=row['sample_name'])

    if not len(light_entry) and not len(heavy_entry):
        pass
    else:
        if not len(light_entry):
            entry = heavy_entry[0].entry
        else:
            entry = light_entry[0].entry
        if not partial:
            status_create = TrimmerEntryStatus.objects.create(entry=entry,
                                                                sample_name = row['sample_name'],
                                                                plate_location = row['plate_location'],
                                                                volume = row['volume'],
                                                                # concentration = row['concentration'],
                                                                comments = row['comments'],
                                                                # amplicon_concentration = row['amplicon_concentration'],
                                                                failure = row['failure'],
                                                                inline_index_name = row['inline_index_name'],
                                                                inline_index = row['inline_index'],
                                                                # LCs_reported = 0 if math.isnan(row['LCs.Reported']) else row['LCs.Reported'],
                                                                # HCs_reported = 0 if math.isnan(row['HCs.Reported']) else row['HCs.Reported']
                                                                )

        else:
            status_create = TrimmerEntryStatus.objects.create(entry=entry,
                                                        sample_name = '' if math.isnan(row['sample_name']) else row['sample_name'],
                                                        plate_location = '' if math.isnan(row['plate_location']) else row['plate_location'],
                                                        volume = 0 if math.isnan(row['volume']) else row['volume'],
                                                        # concentration = 0 if math.isnan(row['concentration']) else row['concentration'],
                                                        comments = '' if math.isnan(row['comments']) else row['comments'],
                                                        # amplicon_concentration = 0 if math.isnan(row['amplicon_concentration']) else row['amplicon_concentration'],
                                                        failure = '' if math.isnan(row['failure']) else row['failure'],
                                                        inline_index_name = '' if type(row['inline_index_name']) != str else row['inline_index_name'],
                                                        inline_index = '' if math.isnan(row['inline_index']) else row['inline_index'],
                                                        # LCs_reported = 0 if math.isnan(row['LCs.Reported']) else row['LCs.Reported'],
                                                        # HCs_reported = 0 if math.isnan(row['HCs.Reported']) else row['HCs.Reported']
                                                        )

        status_create.save()
    return not_found_list


# TODO these next two functions can be the same function
def new_status_upload():
    dir = "../data2/StatusReports/"
    files = os.listdir(dir)
    files = [i for i in files if ".tsv" in i]
    files = [i for i in files if " " not in i]

    not_found_list = []
    for file in files:
        file = dir+file
        result = pd.read_csv(file, delimiter='\t', index_col=False)
        result = result.to_dict(orient='records')
        # check if a light file and do same processing for Trimmer Light entry
        for row in result:
            if type(row['sample_name']) is str:
                if type(row['sample_name']) is str:
                    partial = False
                else:
                    partial = True
                not_found_list += new_create_status(row, partial)


def new_status_not_present():
    dir = "../data2/StatusReports/"
    files = os.listdir(dir)
    files = [i for i in files if ".tsv" in i]
    files = [i for i in files if " " not in i]

    not_found_list = []
    for file in files:
        file = dir + file
        result = pd.read_csv(file, delimiter='\t', index_col=False)
        result = result.to_dict(orient='records')
        # check if a light file and do same processing for Trimmer Light entry
        for row in result:
            if str(row['sample_name']) != 'nan':
                light_entry = TrimmerLight.objects.filter(sample_name=row['sample_name'])
                heavy_entry = TrimmerHeavy.objects.filter(sample_name=row['sample_name'])
                if not light_entry and not heavy_entry:
                    not_found_list.append(row['sample_name'])
    return not_found_list



########################################################################################################################
# NEW METADATA STUFF
########################################################################################################################
def new_get_map_dict():
    file = '../static_data/plate_map.txt'
    f = open(file)
    mapping = {}
    for line in f:
        values = line.split('\t')
        mapping[values[0].replace('"', '')] = values[1].replace('"', '').replace('\n', '')
    return mapping

def new_update_entry(entry, row):
    if entry.mabid != row['trimmer_id']:
        string = "The mabID %s has been updated to %s." %(entry.mabid, row['trimmer_id'])
        message = Messages.objects.create(message=string)
        message.save()
    entry.category = row['Category'] if str(row['Category']) != 'nan' else None
    entry.protein_target = row['ProteinTarget']
    entry.show_on_web = False if row['ShowOnWeb'] == 'F' else True
    entry.mabid = row['trimmer_id']
    try:
        entry.save()
    except:
        print(entry.__dict__)


# TODO fix the ranD samples
def new_metadata_upload():
    mapping = new_get_map_dict()
    # print(mapping)
    dir = "../static_data/"
    files = os.listdir(dir)
    files = [i for i in files if ".tsv" in i]

    for file in files:
        file = dir+file
        result = pd.read_csv(file, delimiter='\t', index_col=False)
        result = result.to_dict(orient='records')
        for row in result:
            light_entries = []
            heavy_entries = []
            if row['sample_name'] != 'None' and row['sample_name'] != 0 and '_' in row['sample_name']:
                # well = row['sample_name'].split('_')[1]
                # plate = 'plate' + row['sample_name'].split('_')[0][1:]
                light_entries = TrimmerLight.objects.filter(sample_name=row['sample_name'])
                heavy_entries = TrimmerHeavy.objects.filter(sample_name=row['sample_name'])

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

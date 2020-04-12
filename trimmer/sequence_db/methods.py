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
# ENTRY STUFF
########################################################################################################################
def create_entries(chain_type, entry_list, row):
    for value in entry_list:
        if row['e-value'] != '-':
            create = eval("Trimmer" + chain_type).objects.create(entry=value,
                                                           SMARTindex=row['SMARTindex'],
                                                           pct_support=row['PctSupport'],
                                                           asv_support=row['ASVcount'],
                                                           total_reads=row['TotalReads'],
                                                           seq_platform=row['Sequencing'],
                                                           plate=row['plate'],
                                                           seq=row[chain_type + 'Chain'],
                                                           e_value=row['e-value'],
                                                           score=row['score'],
                                                           seq_start_index=row['seqstart_index'],
                                                           seq_stop_index=row['seqend_index'],
                                                           scheme=row['scheme'],
                                                           frame=row['frame'],
                                                           aa=row['AA'],
                                                           numbering=row['numbering'],
                                                           domain=row['domain'],
                                                           )
        else:
            create = eval("Trimmer" + chain_type).objects.create(entry=value,
                                                           SMARTindex=row['SMARTindex'],
                                                           pct_support=row['PctSupport'],
                                                           asv_support=row['ASVcount'],
                                                           total_reads=row['TotalReads'],
                                                           seq_platform=row['Sequencing'],
                                                           plate=row['plate'],
                                                           seq=row[chain_type + 'Chain'],
                                                           )
        create.save()

# this is called in the run_update.py script
def new_data_upload():
    dir = "/Users/keithmitchell/Desktop/Repositories/NeuroMabSeq/data/AnnotatedResults/"
    files = os.listdir(dir)
    files = [i for i in files if ".tsv" in i]
    print(files)
    for file in files:
        file = dir+file
        result = pd.read_csv(file, delimiter='\t', index_col=False)
        result = result.to_dict(orient='records')
        print(file)
        if "Heavy" in file:
            chain_type = "Heavy"
        else:
            chain_type = "Light"

        for row in result:
            try:
                entry = TrimmerEntry.objects.get(mabid=row['MabID'])
            except:
                entry = None
            if not entry:
                entry_create = TrimmerEntry.objects.create(mabid=row['MabID'])
                entry_create.save()
                entry = entry_create

            entry_list = []
            entry_list.append(entry)
            create_entries(chain_type, entry_list, row)

        for row in result:
            entry_list = []
            if isinstance(row['DuplicatedIn'], str):
                for x in row['DuplicatedIn'].split(','):
                    try:
                        entry_list.append(TrimmerEntry.objects.get(mabid=x.replace(' ', '')))
                    except:
                        print("The Duplicate mabID does not exist: %s" % x.replace(' ', ''))
            create_entries(chain_type, entry_list, row)


########################################################################################################################
# STATUS STUFF
########################################################################################################################
def create_status(row):
    not_found_list = []
    try:
        entry = TrimmerEntry.objects.get(mabid=row['trimmer_id'])
    except:
        not_found_list.append(row['trimmer_id'])
        entry = None

    if not entry:
        pass
    else:
        status_create = TrimmerEntryStatus.objects.create(entry=entry,
                                                            sample_name = row['sample_name'],
                                                            plate_location = row['plate_location'],
                                                            volume = row['volume'],
                                                            concentration = row['concentration'],
                                                            comments = row['comments'],
                                                            amplicon_concentration = row['amplicon_concentration'],
                                                            failure = row['failure'],
                                                            inline_index_name = row['inline_index_name'],
                                                            inline_index = row['inline_index'],
                                                            LCs_reported = 0 if math.isnan(row['LCs.Reported']) else row['LCs.Reported'],
                                                            HCs_reported = 0 if math.isnan(row['HCs.Reported']) else row['HCs.Reported']
                                                            )

        status_create.save()
    return not_found_list

# TODO these next two functions can be the same function
def status_upload():
    dir = "../data/StatusReports/"
    files = os.listdir(dir)
    files = [i for i in files if ".tsv" in i]
    not_found_list = []
    for file in files:
        file = dir+file
        result = pd.read_csv(file, delimiter='\t', index_col=False)
        result = result.to_dict(orient='records')
        # check if a light file and do same processing for Trimmer Light entry
        for row in result:
            not_found_list += create_status(row)

def status_not_present():
    dir = "../data/StatusReports/"
    files = os.listdir(dir)
    files = [i for i in files if ".tsv" in i]
    not_found_list = []
    for file in files:
        file = dir + file
        result = pd.read_csv(file, delimiter='\t', index_col=False)
        result = result.to_dict(orient='records')
        # check if a light file and do same processing for Trimmer Light entry
        for row in result:
            try:
                entry = TrimmerEntry.objects.get(mabid=row['trimmer_id'])
            except:
                not_found_list.append(row['trimmer_id'])
                entry = None

    return not_found_list


########################################################################################################################
# OLD DATA STUFF
########################################################################################################################
def old_data_upload():
    result = pd.read_csv('/old_data_methods/output.csv', index_col=False)
    result = result.to_dict(orient='records')
    for row in result:
        vl_seq_obj = VLSeq.objects.create(seq=row['VL sequence'])
        vh_seq_obj = VHSeq.objects.create(seq=row['VH sequence'])
        meta = Metadata.objects.create(
                                      target_type=row['TargetType'],
                                      target=row['Target'],
                                      accession=row['AccessionNum'],
                                      gene_name=row['HumanGeneName'],
                                      file_name=row['DataSheetFileName'],
                                      iso_type=row['IsoType'],
                                      validation_t=row['ValidationT'],
                                      validation_brib=row['ValidationBrIB'],
                                      validation_brihc=row['ValidationBrIHC'],
                                      validation_ko=row['ValidationKO'],
                                      tcsupe=row['TCSupe RRID:AB_'],
                                      pure=row['Pure RRID:AB_'],
                                      )


        entry = Entry.objects.create(
                                     name=row['Clone'],
                                     vlseq=vl_seq_obj,
                                     vhseq=vh_seq_obj,
                                     metadata=meta,
                                    )
        vl_seq_obj.save()
        vh_seq_obj.save()
        meta.save()
        entry.save()

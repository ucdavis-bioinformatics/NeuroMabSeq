from .models import *
import pandas as pd
import os
## To run
# python manage.py shell
# from sequence_db.methods import *


def clear_new_data_upload():
    TrimmerEntry.objects.all().delete()
    TrimmerLight.objects.all().delete()
    TrimmerHeavy.objects.all().delete()


def duplicated(row):
    return 0

def new_data_upload():
    dir = "/Users/keithmitchell/Desktop/Repositories/NeuroMabSeq/data/AnnotatedResults/"
    files = os.listdir('/Users/keithmitchell/Desktop/Repositories/NeuroMabSeq/data/AnnotatedResults/')
    files = [i for i in files if ".tsv" in i]
    print(files)
    for file in files:
        file = dir+file
        result = pd.read_csv(file, delimiter='\t', index_col=False)
        result = result.to_dict(orient='records')
        print(file)
        # check if a light file and do same processing for Trimmer Light entry
        if "Light" in file:
            for row in result:
                try:
                    entry = TrimmerEntry.objects.get(mabid=row['MabID'])
                except:
                    entry = None
                if not entry:
                    entry_create = TrimmerEntry.objects.create(mabid=row['MabID'])
                    entry_create.save()
                    entry = entry_create

                print(row['DuplicatedIn'])
                if row['e-value'] != '-':
                    light_create = TrimmerLight.objects.create(entry=entry,
                                                               SMARTindex=row['SMARTindex'],
                                                               pct_support=row['PctSupport'],
                                                               asv_support=row['ASVcount'],
                                                               total_reads=row['TotalReads'],
                                                               seq_platform=row['Sequencing'],
                                                               plate=row['plate'],
                                                               seq=row['LightChain'],
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
                    light_create = TrimmerLight.objects.create(entry=entry,
                                                               SMARTindex=row['SMARTindex'],
                                                               pct_support=row['PctSupport'],
                                                               asv_support=row['ASVcount'],
                                                               total_reads=row['TotalReads'],
                                                               seq_platform=row['Sequencing'],
                                                               plate=row['plate'],
                                                               seq=row['LightChain'],
                                                               )
                light_create.save()

        # check if a heavy file and do same processing for Trimmer Heavy entry
        if "Heavy" in file:
            for row in result:
                try:
                    entry = TrimmerEntry.objects.get(mabid=row['MabID'])
                except:
                    entry = None
                if not entry:
                    entry_create = TrimmerEntry.objects.create(mabid=row['MabID'])
                    entry_create.save()
                    entry = entry_create
                if row['e-value'] != '-':

                    heavy_create = TrimmerHeavy.objects.create(entry=entry,
                                                               SMARTindex=row['SMARTindex'],
                                                               pct_support=row['PctSupport'],
                                                               asv_support=row['ASVcount'],
                                                               total_reads=row['TotalReads'],
                                                               seq_platform=row['Sequencing'],
                                                               plate=row['plate'],
                                                               seq=row['HeavyChain'],
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
                    heavy_create = TrimmerHeavy.objects.create(entry=entry,
                                                               SMARTindex=row['SMARTindex'],
                                                               pct_support=row['PctSupport'],
                                                               asv_support=row['ASVcount'],
                                                               total_reads=row['TotalReads'],
                                                               seq_platform=row['Sequencing'],
                                                               plate=row['plate'],
                                                               seq=row['HeavyChain'],
                                                               )

                heavy_create.save()


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

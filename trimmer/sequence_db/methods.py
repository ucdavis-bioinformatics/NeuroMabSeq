from .models import *
import pandas as pd

## To run
# python manage.py shell
# from sequence_db.methods import *


def clear_new_data_upload():
    TrimmerEntry.objects.all().delete()
    TrimmerLight.objects.all().delete()
    TrimmerHeavy.objects.all().delete()

def new_data_upload():
    light_result = pd.read_csv('/Users/keithmitchell/Desktop/Repositories/NeuroMabSeq/LightChain.tsv', delimiter='\t', index_col=False)
    heavy_result = pd.read_csv('/Users/keithmitchell/Desktop/Repositories/NeuroMabSeq/HeavyChain.tsv', delimiter='\t', index_col=False)
    light_result = light_result.to_dict(orient='records')
    heavy_result = heavy_result.to_dict(orient='records')
    for row in light_result:
        try:
            entry = TrimmerEntry.objects.get(trimmerid=row['TrimmerID'])
        except:
            entry = None
        if not entry:
            entry_create = TrimmerEntry.objects.create(trimmerid=row['TrimmerID'])
            entry_create.save()
            entry = entry_create


        light_create = TrimmerLight.objects.create(entry=entry,
                                                   pctsupport=row['PctSupport'],
                                                   asvcount=row['ASVcount'],
                                                   plate=row['plate'],
                                                   SMARTindex=row['SMARTindex'],
                                                   seq=row['LightChain'])
        light_create.save()

    for row in heavy_result:
        try:
            entry = TrimmerEntry.objects.get(trimmerid=row['TrimmerID'])
        except:
            entry = None
        if not entry:
            entry_create = TrimmerEntry.objects.create(trimmerid=row['TrimmerID'])
            entry_create.save()
            entry = entry_create

        heavy_create = TrimmerHeavy.objects.create(entry=entry,
                                                   pctsupport=row['PctSupport'],
                                                   asvcount=row['ASVcount'],
                                                   plate=row['plate'],
                                                   SMARTindex=row['SMARTindex'],
                                                   seq=row['HeavyChain'])
        heavy_create.save()


def data_upload():
    result = pd.read_csv('/Users/keithmitchell/Desktop/Repositories/NeuroMabSeq/output.csv', index_col=False)
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


def data_backup():
    return 0
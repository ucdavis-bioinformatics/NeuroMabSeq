from .models import *
import pandas as pd

## To run
# python manage.py shell
# from sequence_db.methods import *


def data_upload():
    result = pd.read_csv('/Users/keithmitchell/Desktop/Repositories/trimmer_lab/output.csv', index_col=False)
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
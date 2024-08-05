from sequence_db.methods import *
import sys

#if sys.argv[2] == 'True':
#    is_update = True
#else:
#    is_update = False
#directory = sys.argv[1]

is_update = False
directory = "/Users/keithmitchell/Desktop/Repositories/NeuroMabSeq/data3"


status_upload(is_update, directory) # True for update
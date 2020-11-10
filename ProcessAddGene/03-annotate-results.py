
#!/usr/bin/env python3
'''
Update:
This program expects there to be on plate_Sequences.tsv file.

            This program expects there to be two csv files:
            ./02-Results/*_HeavyChain.tsv
            ./02-Results/*_LightChain.tsv

It will load each of these files, calculate the three
frames of translations, then push the sequences through
ANARCI to look for a predicted domain and numbering. 
ANARCI output will then be parsed and included in a new 
output file for the web page.
'''

from Bio.Seq import Seq
import csv
import subprocess
from glob import glob
import os

## Globals
anarciexe = 'ANARCI'
outpath = './03-AnnotatedResults/'

os.system('mkdir -p ' + outpath)

def process_file(chain):
    """Process ASV records through ANARCI software tool and write new table to outpath."""
    tsvs = glob('./02-Results/*_' + chain + '.tsv')
    assert (len(tsvs) > 0), "NO TSV file found, check that R scripts ran."
    assert (len(tsvs) == 1), "More than one TSV file was found for " + './02-Results/*_' + chain + '.tsv'
    inf = tsvs[0]
    infDR = csv.DictReader(open(inf, 'r'), delimiter='\t')
    outf = open(os.path.join(outpath,os.path.basename(inf)), 'w')
    outfDW = csv.DictWriter(outf, delimiter='\t', restval='-', fieldnames = infDR.fieldnames + 
                                ['chain_type', 'e-value', 'score', 'seqstart_index', 'seqend_index', 'scheme', 'frame', 'AA', 'numbering', 'domain'])
    outfDW.writeheader()

    for record in infDR:
        seq = Seq(record['ASV'].strip())
        # Build translations of each frame until one has a predicted domain:
        for i in range(3):
            aa = (seq[i:] + ("N" * (3 - len(seq[i:]) %3))).translate()
            anarci = run_anarci(aa, i)
            if anarci is not None:
                record.update(anarci)
                break
        outfDW.writerow(record)
    outf.close()


def run_anarci(aa, frame):
    """Run ANARCI program and parse results into a dictionary. Return FIRST hit."""
    result = None
    # Parse the aa into each sub-piece that doesn't have a stop codon:
    subAAs = str(aa).strip('X').split('*')
    for i in range(len(subAAs)):
        s = subAAs[i]
        if(len(s) > 0):
            cmd = anarciexe + " --scheme imgt -i " + s
            test = subprocess.run(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
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
                result['frame'] = frame
                result['AA'] = '*'.join(subAAs)
                result['numbering'] = []
                result['domain'] = []
                for l in output[7:]:
                    if l != '//':
                        result['numbering'] += [l.strip().split()[1]]
                        result['domain'] += [l.strip().split()[2]]
                result['numbering'] = ','.join(result['numbering'])
                result['domain'] = ','.join(result['domain'])
                break
    return(result)


#for chain in ['HeavyChain', 'LightChain']:
#    process_file(chain)
for chain in ['Sequences']:
    process_file(chain)



"""
Example call:
./anarci-1.3/bin/ANARCI --scheme imgt -i TDQSPQAVSSGCLLKMKLPVRLLVLMFWIPASSSDVVMTQTPLSLPVSLGDQASISCRSSQSLVHSNGNTYLHWYLQNPGQSPKLLIYKVSKRFSGVPDRFSGSGSGTDFTLKISRVEAEDLGVYFCSQSTHVPYTFGGGTKLEIKRA

NL*SVSSPQSLKTLTLTMEWSWVFLFLLSVTSGVHSQVQLQQSGAELVKPGASVKLSCKTSGYTFTSYWIQWVKRRPGQGLGWIGEIFPGTGTTYYNENFKGKATLTIDTSSSTAYMQLSSLTSEDSAVYFCARVDGSSYFDYWGQGTTLTVSS
"""
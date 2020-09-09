import sys
import os
from glob import glob

r1 = sys.argv[1]
r2 = sys.argv[2]
primerf = sys.argv[3]
cmdf = sys.argv[4]

#r1 = glob('./00-RawData/*_R1_*.fastq.gz')[0]
#r2 = r1.replace('_R1_', '_R2_')
#primerf = '1_Short_primers.csv'
#cmdf = '01-trim-1_Short_CSP.sh'

# r1f = './00-RawData/2_Long_CSP_Pool_S2_L001_R1_001.fastq.gz'
# r1r = './00-RawData/2_Long_CSP_Pool_S2_L001_R2_001.fastq.gz'
# primerf = '2_Long_primers.csv'
# cmdf = '01-trim-2_Long_CSP.sh'

# python 01-build_hts.py ./00-RawData/Trimmer6_S22_L001_R1_001.fastq.gz \
#     ./00-RawData/Trimmer6_S22_L001_R2_001.fastq.gz \
#     1_Short_primers.csv 01-trim-1_Short_CSP.sh

os.system('mkdir -p 01-PrimerTrim')

outf = open(cmdf, 'w')

htspath = "../../HTStream/build/bin/"

i=0
for l in open(primerf, 'r'):
    if i == 0:
        header=l.strip().split()
        i += 1
        continue
    l2 = l.strip().split()
    if len(l2) == 6:
        #sample = primerf.replace(".csv", '') + "_" + l2[header.index('SampleID')] + "_" + l2[header.index('Primer1ID')] + "_" + l2[header.index('Primer2ID')]
        sample = l2[header.index('SampleID')]
        logf = './01-PrimerTrim/' + sample + '.log'
        prefix = './01-PrimerTrim/' + sample
        cmd = "nice -n1 " + htspath + "hts_Primers -d 0 -l 0 -e 0 -r 2 -x -P " + l2[header.index('Primer1Seq')] + "TGGGG"
        cmd += " -Q " + l2[header.index('Primer2Seq')] + " -1 " + r1 + " -2 " + r2 + " -L " + logf + " | "
        cmd += htspath + "hts_NTrimmer -e -AL " + logf + " | "
        cmd += htspath + "hts_SeqScreener -C -r -x .01 -k 21 -s aberrant_LC.fasta -AL " + logf + " | "
        cmd += htspath + "hts_QWindowTrim -l -n -q 10 -m 260 -AL " + logf + " | "
        cmd += htspath + "hts_Overlapper -AL " + logf + " -m 385 -f " + prefix + '\n'
        outf.write(cmd)
outf.close()

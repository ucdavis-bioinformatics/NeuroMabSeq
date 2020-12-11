import sys
import os
from glob import glob

r1 = sys.argv[1]
r2 = sys.argv[2]
primerf = sys.argv[3]
cmdf = sys.argv[4]

#r1 = glob('./00-RawData/*_R1_*.fastq.gz')[0]
#r2 = r1.replace('_R1_', '_R2_')
#primerf = 'TSO_demux_primers.csv'
#cmdf = '01-trim-1_Short_CSP.sh'


# python3 01-build_hts.py ./00-RawData/R1_250k.fastq.gz \
#     ./00-RawData/R2_250k.fastq.gz \
#     TSO_demux_primers.csv 01-trim-1_Short_CSP.sh

os.system('mkdir -p 01-PrimerTrim')

outf = open(cmdf, 'w')

htspath = "../../TrimmerConda/bin/"

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
        cmd =  f"nice -n1 {htspath}hts_Primers -d 0 -l 0 -e 0 -r 2 -x -P {l2[header.index('TSOBarcode')]}"
        cmd += f" -Q {l2[header.index('TargetSpecificPrimers')]} -1 {r1} -2  {r2} -L {logf} | "
        cmd += f"{htspath}hts_NTrimmer -e -A {logf} | "
        cmd += f"{htspath}hts_SeqScreener -C -r -x .01 -k 21 -s aberrant_LC.fasta -A {logf} | "
        cmd += f"{htspath}hts_QWindowTrim -l -q 10 -A {logf} | "
        cmd += f"{htspath}hts_Overlapper -A {logf} | " 
        cmd += f"{htspath}hts_LengthFilter -m 385 -A {logf} -F -f {prefix}\n"
        outf.write(cmd)
outf.close()

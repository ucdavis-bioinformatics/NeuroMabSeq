import sys
import os

r1f = sys.argv[1]
r1r = sys.argv[2]
primerf = sys.argv[3]
cmdf = sys.argv[4]

# r1f = './00-RawData/2_Long_CSP_Pool_S2_L001_R1_001.fastq.gz'
# r1r = './00-RawData/2_Long_CSP_Pool_S2_L001_R2_001.fastq.gz'
# primerf = '2_Long_primers.csv'
# cmdf = '01-trim-2_Long_CSP.sh'

os.system('mkdir -p 01-PrimerTrim')

outf = open(cmdf, 'w')

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
        cmd = "../HTStream/build/bin/hts_Primers -d 0 -l 0 -e 0 -r 2 -x -P " + l2[header.index('Primer1Seq')] + "TGGGG"
        cmd += " -Q " + l2[header.index('Primer2Seq')] + " -1 " + r1f + " -2 " + r1r + " -L " + logf + " | "
        cmd += "../HTStream/build/bin/hts_NTrimmer -e -AL " + logf + " | "
        cmd += "../HTStream/build/bin/hts_SeqScreener -C -r -x .01 -k 21 -s aberrant_LC.fasta -AL " + logf + " | "
        cmd += "../HTStream/build/bin/hts_QWindowTrim -l -n -q 10 -m 260 -AL " + logf + " | "
        cmd += "../HTStream/build/bin/hts_Overlapper -AL " + logf + " -m 385 -f " + prefix + '\n'
        outf.write(cmd)
outf.close()

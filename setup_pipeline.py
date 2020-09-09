#!/usr/bin/env python3

import os
import csv
from glob import glob

# Constants:
ncpu = 10


# Read in SampleSheet:
ss = csv.DictReader(open("SampleSheet.txt", 'r'), delimiter='\t')

# Setup plates:
for plate in ss:
    r1 = glob(f"./00-RawData/{plate['filePrefix']}*_R1_*")
    assert len(r1) == 1, f"ERROR: plate['filePrefix'] matches more than one file."
    r1 = r1[0]
    r2 = r1.replace("_R1_", "_R2_")
    s = os.path.join('01-Processing', plate['plate'])
    os.system('mkdir -p ./' + s + '/00-RawData/')
    os.system('mkdir -p ./' + s + '/01-PrimerTrimReport/')
    os.system('mkdir -p ./' + s + '/02-Results/')
    os.system('ln -s ' + os.path.abspath(r1) + ' ./' + s + '/00-RawData/')
    os.system('ln -s ' + os.path.abspath(r2) + ' ./' + s + '/00-RawData/')
    os.system('ln -s ./NeuroMabSeq/01-build_hts.py ./' + s + '/')
    os.system('ln -s ./NeuroMabSeq/aberrant_LC.fasta ./' + s + '/')
    os.system('cp ./NeuroMabSeq/01-PrimerTrimReport/report.RMD ./' + s + '/01-PrimerTrimReport/')
    os.system('ln -s ./NeuroMabSeq/SMARTindex_well.tsv ./' + s + '/02-Results/')
    os.system('cp ./NeuroMabSeq/02-Results/02-Hybridoma-DADA2-analysis.RMD ./' + s + '/02-Results/')
    os.system('ln -s ./NeuroMabSeq/03-annotate-results.py ./' + s + '/')
    os.system(f'ln -s ./NeuroMabSeq/{plate["Primers"]} ./' + s + '/')
    os.system('ln -s ./NeuroMabSeq/samlogin.pem ./' + s + '/')

    #Create run_pipeline.sh with proper settings:
    outf = open(f"./{s}/run_pipeline.sh", 'w')
    cmd = "aklog\n"
    outf.write(cmd)
    cmd = "module load R/3.6.1\n"
    outf.write(cmd)
    cmd = "source /share/biocore/projects/Trimmer_James_UCD/2019.11.18-Trimmer-Hybridoma-Seq/ANARCI-venv/bin/activate\n"
    outf.write(cmd)
    cmd = f"python 01-build_hts.py {r1} {r2} {plate['Primers']} 01-runHTS.sh\n"
    outf.write(cmd)
    cmd = f"parallel -j {ncpu} < 01-runTS.sh\n"
    outf.write(cmd)
    # Build a report of cleaning:
    cmd = f"module load R/3.6.1;"
    cmd += f"Rscript -e \"plate='{plate['plate']}';submission='{plate['submissionID']}';"
    cmd += f"rmarkdown::render('./01-PrimerTrimReport/report.RMD')\"\n"
    outf.write(cmd)
    # Build ASVs:
    cmd = "module load R/3.6.1;"
    cmd += f"Rscript -e \"plate='{plate['plate']}';submission='{plate['submissionID']}';"
    cmd += f"rmarkdown::render('./02-Results/02-Hybridoma-DADA2-analysis.RMD')\"\n"
    outf.write(cmd)
    # Use ANARCI to annotate results:
    cmd = "source /share/biocore/projects/Trimmer_James_UCD/2019.11.18-Trimmer-Hybridoma-Seq/ANARCI-venv/bin/activate;"
    cmd += "python3 03-annotate-results.py"
    # Finally, upload results:
    dest = 'shunter@ec2-54-177-200-140.us-west-1.compute.amazonaws.com:/home/shunter/data/'
    cmd = f"rsync -avz -e 'ssh -i samlogin.pem' ./03-AnnotatedResults/*.tsv {dest}AnnotatedResults"
    outf.write(cmd)
    cmd = f"rsync -avz -e 'ssh -i samlogin.pem' ./02-Results/*_SampleStatus.tsv {dest}StatusReports"
    outf.write(cmd)
    cmd = f"rsync -avz -e 'ssh -i samlogin.pem' ./01-PrimerTrimReport/report.html {dest}HTML_Reports/{plate['plate']}_PrimerTrimReport.html"
    outf.write(cmd)
    cmd = f"rsync -avz -e 'ssh -i samlogin.pem' ./02-Results/02-Hybridoma-DADA2-analysis.html {dest}HTML_Reports/{plate['plate']}_report.html"
    outf.write(cmd)
        

    #rsync -vrt --no-p --no-g --chmod=ugo=rwX ./03-AnnotatedResults/*.tsv bioshare@bioshare.bioinformatics.ucdavis.edu:/3ksenvfdffie3aj/AnnotatedResults/
    #rsync -vrt --no-p --no-g --chmod=ugo=rwX ./02-Results/*_SampleStatus.tsv bioshare@bioshare.bioinformatics.ucdavis.edu:/3ksenvfdffie3aj/StatusReports/
    #rsync -vrt --no-p --no-g --chmod=ugo=rwX ./02-Results/02-Hybridoma-DADA2-analysis.html  bioshare@bioshare.bioinformatics.ucdavis.edu:'/3ksenvfdffie3aj/HTML_Reports/'$plate'_report.html'
    #ssh -i ~/.ssh/samlogin.pem shunter@ec2-54-177-200-140.us-west-1.compute.amazonaws.com



rsync -avz -e 'ssh -i samlogin.pem' SMARTindex_6-REV-LC_dist.tsv  shunter@ec2-54-177-200-140.us-west-1.compute.amazonaws.com:/home/shunter/data/

- create an 01-Processing/TRIMMER00NN folder
- link reads, copy in all of the important pieces
- setup the scripts based on the primers used
    -run_pipeline.sh
    -01-build_hts.py
    
#!/usr/bin/env python3

import os
import csv
from glob import glob

# Constants:
ncpu = 10

# Read in SampleSheet:
ss = csv.DictReader(open("./NeuroMabSeq/SampleSheet.txt", 'r'), delimiter='\t')

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
    os.system('ln -s ' + os.path.abspath('./NeuroMabSeq/01-build_hts.py') + ' ./' + s + '/')
    os.system('ln -s ' + os.path.abspath('./NeuroMabSeq/aberrant_LC.fasta') + ' ./' + s + '/')
    os.system('cp ./NeuroMabSeq/01-PrimerTrimReport/report.RMD ./' + s + '/01-PrimerTrimReport/')
    os.system('ln -s ' + os.path.abspath('./NeuroMabSeq/SMARTindex_well.tsv') + ' ./' + s + '/02-Results/')
    os.system('cp ./NeuroMabSeq/02-Results/02-Hybridoma-DADA2-analysis.RMD ./' + s + '/02-Results/')
    os.system('ln -s ' + os.path.abspath('./NeuroMabSeq/03-annotate-results.py') + ' ./' + s + '/')
    os.system('ln -s ' + os.path.abspath(f'./NeuroMabSeq/{plate["Primers"]} ')  + s + '/')
    os.system('ln -s ' + os.path.abspath('samlogin.pem') + ' ./' + s + '/')

    #Create run_pipeline.sh with proper settings:
    with open(f"./{s}/run_pipeline.sh", 'w') as outf:
        outf.write("#Setup\n")
        cmd = "aklog\n"
        outf.write(cmd)
        cmd = "module load R/3.6.1\n"
        outf.write(cmd)
        cmd = "source /share/biocore/projects/Trimmer_James_UCD/2019.11.18-Trimmer-Hybridoma-Seq/ANARCI-venv/bin/activate\n"
        outf.write(cmd)
        outf.write("\n#Build HTStream script\n")
        cmd = f"python 01-build_hts.py {r1} {r2} {plate['Primers']} 01-runHTS.sh\n"
        outf.write(cmd)
        outf.write("\n#Run HTStream script\n")
        cmd = f"parallel -j {ncpu} < 01-runTS.sh\n"
        outf.write(cmd)
        # Build a report of cleaning:
        outf.write("\n# Build a report of cleaning:\n")
        cmd = f"module load R/3.6.1;"
        cmd += f"Rscript -e \"plate='{plate['plate']}';submission='{plate['submissionID']}';"
        cmd += f"rmarkdown::render('./01-PrimerTrimReport/report.RMD')\"\n"
        outf.write(cmd)
        # Build ASVs:
        outf.write("\n# Build ASVs:\n")
        cmd = "module load R/3.6.1;"
        cmd += f"Rscript -e \"plate='{plate['plate']}';submission='{plate['submissionID']}';"
        cmd += f"rmarkdown::render('./02-Results/02-Hybridoma-DADA2-analysis.RMD')\"\n"
        outf.write(cmd)
        # Use ANARCI to annotate results:
        outf.write("\n# Use ANARCI to annotate results:\n")
        cmd = "source /share/biocore/projects/Trimmer_James_UCD/2019.11.18-Trimmer-Hybridoma-Seq/ANARCI-venv/bin/activate;"
        cmd += "python3 03-annotate-results.py"
        # Finally, upload results:
        outf.write("\n# Upload results:\n")
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

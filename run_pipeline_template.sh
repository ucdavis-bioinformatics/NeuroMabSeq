submissionID=038b80bc1099
plate=plate28

python 01-build_hts.py 

# ./00-RawData/Trimmer6_S22_L001_R1_001.fastq.gz \
#    ./00-RawData/Trimmer6_S22_L001_R2_001.fastq.gz \
#    1_Short_primers.csv 01-trim-1_Short_CSP.sh

parallel < 01-trim-1_Short_CSP.sh

module load R/3.6.1
Rscript -e "plate='$plate';submission='$submissionID';rmarkdown::render('./01-PrimerTrimReport/report.RMD')"

Rscript -e "plate='$plate';submission='$submissionID';rmarkdown::render('./02-Results/02-Hybridoma-DADA2-analysis.RMD')"

#Rscript -e "rmarkdown::render('02-Hybridoma-DADA2-analysis.RMD')"

# Use python to add AA translations to the putative LCS:
source /share/biocore/projects/Trimmer_James_UCD/2019.11.18-Trimmer-Hybridoma-Seq/ANARCI-venv/bin/activate

python3 03-annotate-results.py 

rsync -vrt --no-p --no-g --chmod=ugo=rwX ./03-AnnotatedResults/*.tsv bioshare@bioshare.bioinformatics.ucdavis.edu:/3ksenvfdffie3aj/AnnotatedResults/
rsync -vrt --no-p --no-g --chmod=ugo=rwX ./02-Results/*_SampleStatus.tsv bioshare@bioshare.bioinformatics.ucdavis.edu:/3ksenvfdffie3aj/StatusReports/
rsync -vrt --no-p --no-g --chmod=ugo=rwX ./02-Results/02-Hybridoma-DADA2-analysis.html  bioshare@bioshare.bioinformatics.ucdavis.edu:'/3ksenvfdffie3aj/HTML_Reports/'$plate'_report.html'

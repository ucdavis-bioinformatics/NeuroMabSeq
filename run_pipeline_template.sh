# NOTE, for now, run the following before running this script:
# module load R/3.6.1
# source /share/biocore/projects/Trimmer_James_UCD/2019.11.18-Trimmer-Hybridoma-Seq/ANARCI-venv/bin/activate

## SET Submission and Plate:
submissionID=038b80bc1099
plate=plate28

# Build cleaning script
python 01-build_hts.py 

# Run cleaning for all samples:
parallel < 01-trim-1_Short_CSP.sh

# Build a report of cleaning:
Rscript -e "plate='$plate';submission='$submissionID';rmarkdown::render('./01-PrimerTrimReport/report.RMD')"

# Build ASVs:
Rscript -e "plate='$plate';submission='$submissionID';rmarkdown::render('./02-Results/02-Hybridoma-DADA2-analysis.RMD')"

# Use python to add AA translations to the putative LCS:
# source /share/biocore/projects/Trimmer_James_UCD/2019.11.18-Trimmer-Hybridoma-Seq/ANARCI-venv/bin/activate
python3 03-annotate-results.py 

# Upload:
rsync -vrt --no-p --no-g --chmod=ugo=rwX ./03-AnnotatedResults/*.tsv bioshare@bioshare.bioinformatics.ucdavis.edu:/3ksenvfdffie3aj/AnnotatedResults/
rsync -vrt --no-p --no-g --chmod=ugo=rwX ./02-Results/*_SampleStatus.tsv bioshare@bioshare.bioinformatics.ucdavis.edu:/3ksenvfdffie3aj/StatusReports/
rsync -vrt --no-p --no-g --chmod=ugo=rwX ./02-Results/02-Hybridoma-DADA2-analysis.html  bioshare@bioshare.bioinformatics.ucdavis.edu:'/3ksenvfdffie3aj/HTML_Reports/'$plate'_report.html'

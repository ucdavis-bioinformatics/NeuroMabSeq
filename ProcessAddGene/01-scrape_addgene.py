#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import csv
import sys

### functions ####
def parse_mab(url, num, mabid):
    # extract data from a single mab
    page = requests.get(url)
    if page.status_code != 200: 
        print(f"Error, {url} didn't work, exiting.")
        sys.exit()
    soup = BeautifulSoup(page.content, 'html.parser')
    # get all text areas and look for "Light Chain Variable Domain"
    agd = lc = hc = None
    for ta in soup.find_all('textarea'):
        txt = ta.get_text()
        if txt[0] == '>':
            txt2 = txt.split('\n')
            if 'light chain variable domain' in txt2[0].lower():
                lc = ''.join(txt2[1:]).strip().replace('_', '')
            if 'heavy chain variable domain' in txt2[0].lower():
                hc = ''.join(txt2[1:]).strip().replace('_', '')
    if lc is not None and hc is not None:
        agd = []
        agd.append( {'Sample_Name':"Psanger_" + num,
                    'plate':'Psanger',
                    'SMARTindex':'None',
                    'MabID':mabid,
                    'Chain':'HC',
                    'ChainID':'Psanger_' + num + ".HC1",
                    'ASVcount':1,
                    'PctSupport':100,
                    'TotalReads':1,
                    'Sequencing':'Sanger',
                    'ASV':hc,
                    'DuplicatedIn':''})
        agd.append( {'Sample_Name':"Psanger_" + num,
                    'plate':'Psanger',
                    'SMARTindex':'None',
                    'MabID':mabid,
                    'Chain':'LC',
                    'ChainID':'Psanger_' + num + ".LC1",
                    'ASVcount':1,
                    'PctSupport':100,
                    'TotalReads':1,
                    'Sequencing':'Sanger',
                    'ASV':lc,
                    'DuplicatedIn':''})
    return(agd)
 
### Create output files ###
sequencesF = open('./02-Results/Sanger_samples_Sequences.tsv', 'w')
sequencesFieldnames = ['Sample_Name','plate','SMARTindex','MabID','Chain','ChainID','ASVcount','PctSupport','TotalReads','Sequencing','ASV','DuplicatedIn']
seqWriter = csv.DictWriter(sequencesF, fieldnames=sequencesFieldnames, delimiter='\t')
seqWriter.writeheader()

mdataF = open('Sanger_metadata.tsv', 'w')
mdataFieldnames = ['sample_name','trimmer_id','PlateName','Category','ShowOnWeb','ProteinTarget']
mdataWriter = csv.DictWriter(mdataF, fieldnames=mdataFieldnames, delimiter='\t')
mdataWriter.writeheader()


# Start parsing all samples:
#url = 'http://' + line2[3].replace('(', '').replace(')', '') + '/sequences/'
url = "https://www.addgene.org/antibodies/trimmer-neuromab/"
page = requests.get(url)
if page.status_code != 200:
    print(f"Error, {url} didn't work, exiting.")
soup = BeautifulSoup(page.content, 'html.parser')

# Extract the table listing all samples:
tbl = soup.find('table')

# Parse the table, extract data elements, get the sequences, write to files:
print("Starting web scraping...")
i = 0
for rec in tbl.find_all('tr'):
    if i == 0:
        header = rec.text.strip().split('\n')
    else:
        values = rec.text.strip().split('\n')
        num = values[header.index('Addgene ID')]
        mabid = values[header.index('Plasmid')]
        ProteinTarget = values[header.index('Target')]
        url = "https://www.addgene.org/" + num + '/sequences/'
        agd = parse_mab(url, num, mabid)
        if agd is not None:
            mdata = {'sample_name':'Psanger_' + num,
                     'trimmer_id':mabid,
                     'PlateName':'Sanger_samples',
                     'Category':'6',
                     'ShowOnWeb':'T',
                     'ProteinTarget':ProteinTarget}
            mdataWriter.writerow(mdata)
            for chain in agd:
                seqWriter.writerow(chain)       
    i += 1

print(F"Web scraping complete, pulled {i} records.")
print("Adding GS sequences...")
# Finally, read in the GS sequences (these were sequenced via Sanger, but are not in AddGene):
for rec in csv.DictReader(open("Sanger_GS_sequences.tsv", 'r'), delimiter='\t'):
    #print(rec)
    seqWriter.writerow(rec)
sequencesF.close()

# Metadata supplied by the master metadata spreadsheet for now?
mdataF.close()


print("Processing complete.")


16S_Amplicon_Pipeline
=====================

Scripts for 16S amplicon analysis

######The 16S analysis was completed following the [MOTHUR 454 SOP ](http://www.mothur.org/wiki/Schloss_SOP) and [Costello stool analysis protocol] (http://www.mothur.org/wiki/Costello_stool_analysis) with a few modifications.

#####1. Parse Amplicons

Split ITS, LSU and 16S reads using Matt's dbcAmplicon python script: https://github.com/msettles/dbcAmplicons.
```bash
dbcAmplicons preprocess -b barcodeLookupTable.txt -p 16S_ITS_LSU_PrimerTable.txt -s ZanneAmplicons_MattPipeline.txt -u -U -v -1 Undetermined_S0_L001_R1_001.fastq -2 MariyaAmy002_S1_L001_R1_001.fastq -3 MariyaAmy002_S1_L001_R2_001.fastq -4 Undetermined_S0_L001_R2_001.fastq &
```
The -s flag gives the name of a sample sheet file. The sample sheet used for the Tyson year 3 harvest is included in this repository (Tyson_samplesheet.txt).

#####2. Split by Sample
Split sequences into individual files by sample and generate a file mapping file name to sample name for mothur analysis.

```bash
python  parsefastq.py -s ZanneAmplicons_MattPipeline.txt -r1 R1.fastq -r2 R2.fastq -o output/directory -p PrimerName
```
This script will generate a file called "stability.files" this file contains a mapping of file names to their corresponding samples. The stability file will be the input file to mothur. Navigate to the specified ouput directory and start mothur ...

######The following commands can be run in batch mode from the 16S_mothur_script.sh rather than interactivly in the mothur shell as described below.
     
#####3. Assemble Paried End Reads
```
mothur > make.contigs(file=stability.files, processors=10)

Output File Names: 
stability.trim.contigs.fasta
stability.contigs.report
stability.scrap.contigs.fasta
stability.contigs.groups
```
#####4. Sequence Processing and Cleanup

Look at the quality of LSU sequences.
      
```
mothur > summary.seqs(fasta=stability.trim.contigs.fasta)

Using 10 processors.

                Start   End     NBases  Ambigs  Polymer NumSeqs
Minimum:        1       277     277     0       3       1
2.5%-tile:      1       431     431     0       4       152765
25%-tile:       1       433     433     0       4       1527650
Median:         1       447     447     0       5       3055299
75%-tile:       1       472     472     1       5       4582948
97.5%-tile:     1       498     498     16      7       5957833
Maximum:        1       563     562     73      280     6110597
Mean:   1       453.881 453.881 1.42854 4.85083
# of Seqs:      6110597

Output File Names: 
stability.trim.contigs.summary
```      

Clean up sequences by removing all sequences with more than 1 ambiguity or homopolymers longer than 8 bp.

*Note: mothur has many parameters for quality screening sequence using the [trim.seqs()](http://www.mothur.org/wiki/Trim.seqs) command. Quality screening should be based on the results of the summary.seqs() command for each particular set of sequences.* 

```
mothur > screen.seqs(fasta=stability.trim.contigs.fasta, group=stability.contigs.groups, maxambig=1, minlength=300, maxhomop=8)

Output File Names: 
stability.trim.contigs.good.fasta
stability.trim.contigs.bad.accnos
stability.contigs.good.groups

mothur > summary.seqs(fasta=stability.trim.contigs.good.fasta)

Using 10 processors.
[WARNING]: This command can take a namefile and you did not provide one. The current namefile is stability.trim.contigs.good.names which seems to match stability.trim.contigs.good.fasta.

                Start   End     NBases  Ambigs  Polymer NumSeqs
Minimum:        1       300     300     0       3       1
2.5%-tile:      1       431     431     0       4       128916
25%-tile:       1       433     433     0       4       1289160
Median:         1       446     446     0       5       2578319
75%-tile:       1       468     468     0       5       3867478
97.5%-tile:     1       495     495     1       6       5027721
Maximum:        1       561     560     1       8       5156636
Mean:   1       452.306 452.306 0.119068        4.78745
# of Seqs:      5156636

Output File Names: 
stability.trim.contigs.good.summary
```
Collapse all identical sequences.
     
```
mothur > unique.seqs(fasta=stability.trim.contigs.good.fasta)

  Output File Names: 
  stability.trim.contigs.good.names
  stability.trim.contigs.good.unique.fasta
  
mothur > summary.seqs(fasta=stability.trim.contigs.good.unique.fasta)

Using 10 processors.
[WARNING]: This command can take a namefile and you did not provide one. The current namefile is stability.trim.contigs.good.names which seems to match stability.trim.contigs.good.unique.fasta.

                Start   End     NBases  Ambigs  Polymer NumSeqs
Minimum:        1       300     300     0       3       1
2.5%-tile:      1       431     431     0       4       95710
25%-tile:       1       433     433     0       4       957099
Median:         1       447     447     0       5       1914198
75%-tile:       1       472     472     0       5       2871297
97.5%-tile:     1       498     498     1       6       3732686
Maximum:        1       561     560     1       8       3828395
Mean:   1       453.966 453.966 0.155886        4.83139
# of Seqs:      3828395

Output File Names: 
stability.trim.contigs.good.unique.summary
```
#####5. Alignment

Align 16S sequences to [referance 16S silva alignment](http://www.mothur.org/w/images/9/98/Silva.bacteria.zip).
  
```
mothur > align.seqs(fasta=stability.trim.contigs.good.unique.fasta, reference=../silva.bacteria/silva.bacteria.fasta, processors=10)

Some of you sequences generated alignments that eliminated too many bases, a list is provided in stability.trim.contigs.good.unique.flip.accnos. If you set the flip parameter to true mothur will try aligning the
 reverse compliment as well.
It took 10160 secs to align 3828395 sequences.


Output File Names: 
stability.trim.contigs.good.unique.align
stability.trim.contigs.good.unique.align.report
stability.trim.contigs.good.unique.flip.accnos

mothur > summary.seqs(fasta=stability.trim.contigs.good.unique.align)

Using 10 processors.
[WARNING]: This command can take a namefile and you did not provide one. The current namefile is stability.trim.contigs.good.names which seems to match stability.trim.contigs.good.unique.align.

                Start   End     NBases  Ambigs  Polymer NumSeqs
Minimum:        0       0       0       0       1       1
2.5%-tile:      1044    10303   431     0       4       95710
25%-tile:       1044    13125   433     0       4       957099
Median:         1044    13125   447     0       5       1914198
75%-tile:       1044    13125   470     0       5       2871297
97.5%-tile:     1044    13859   497     1       6       3732686
Maximum:        43116   43116   560     1       8       3828395
Mean:   1072.42 13061.1 452.867 0.15577 4.8272
# of Seqs:      3828395

Output File Names: 
stability.trim.contigs.good.unique.summary
```

#####6. Check for Chimeras

Use chimera slayer and the referance 16S alignment to check for chimeric 16S sequences.
    
```
mothur > chimera.slayer(fasta=Zanne_LSU_aligned.trim.unique.align, template=James_2006_FungiOnly_LSU_LR0R_LR3.fasta, processors=10, blastlocation=/usr/bin/)
```


##To Update ...
Remove chimeric sequences from analysis files. 
```
mothur > remove.seqs(accnos=Zanne_LSU_aligned.trim.unique.slayer.accnos, name=Zanne-LSU_aligned.trim.names)
    
      Output File Names:
      Zanne-LSU_aligned.trim.pick.names
      
mothur > remove.seqs(accnos=Zanne_LSU_aligned.trim.unique.slayer.accnos, group=LSU.groups)
      
      Output File Names: 
      LSU.pick.groups
      
mothur > remove.seqs(accnos=Zanne_LSU_aligned.trim.unique.slayer.accnos, fasta=Zanne_LSU_aligned.trim.unique.align)
      
      Output File Names: 
      Zanne_LSU_aligned.trim.unique.pick.align
```
     
#####7. Clean Alignment

Check quality of alignment with chimeras removed.   
```
mothur > summary.seqs(fasta=Zanne_LSU_aligned.trim.unique.pick.align, processors=15)
      
      Using 15 processors.
      
                      Start   End     NBases  Ambigs  Polymer NumSeqs
      Minimum:        0       0       0       0       1       1
      2.5%-tile:      1       264     195     0       4       129794
      25%-tile:       18      644     520     0       4       1297937
      Median:         18      686     543     0       5       2595874
      75%-tile:       18      954     565     1       5       3893810
      97.5%-tile:     53      954     569     1       7       5061953
      Maximum:        972     972     575     1       11      5191746
      Mean:   25.6089 756.843 517.662 0.420943        4.85864
      # of Seqs:      5191746
```
Remove sequences that align after base 53 or are less than 500 bp long.

*Note: mothur has many parameters for quality screening alignments using the [screen.seqs()](http://www.mothur.org/wiki/Screen.seqs) command. Quality screening should be based on the results of the summary.seqs() command for each particular alignment.* 

```
mothur > screen.seqs(fasta=Zanne_LSU_aligned.trim.unique.pick.align, start=53, minlength=500)

      Output File Names: 
      Zanne_LSU_aligned.trim.unique.pick.good.align
      Zanne_LSU_aligned.trim.unique.pick.bad.accnos
      
      It took 51 secs to screen 5191746 sequences.
      
mothur > summary.seqs(fasta=Zanne_LSU_aligned.trim.unique.pick.good.align)
      
      Using 15 processors
      
                      Start   End     NBases  Ambigs  Polymer NumSeqs
      Minimum:        1       609     500     0       3       1
      2.5%-tile:      18      632     507     0       4       106087
      25%-tile:       18      654     530     0       4       1060862
      Median:         18      721     555     1       5       2121723
      75%-tile:       18      954     566     1       5       3182584
      97.5%-tile:     44      954     569     1       7       4137359
      Maximum:        53      972     575     1       11      4243445
      Mean:   20.5771 806.123 547.62  0.508047        4.92197
      # of Seqs:      4243445
```
Remove regions with only gaps from the alignment
```
mothur > filter.seqs(fasta=Zanne_LSU_aligned.trim.unique.pick.good.align)
      
      Length of filtered alignment: 771
      Number of columns removed: 201
      Length of the original alignment: 972
      Number of sequences used to construct filter: 4243445
      
      Output File Names: 
      Zanne_LSU_aligned.filter
      Zanne_LSU_aligned.trim.unique.pick.good.filter.fasta
      
mothur > summary.seqs(fasta=Zanne_LSU_aligned.trim.unique.pick.good.filter.fasta)
      
      Using 15 processors
      
                      Start   End     NBases  Ambigs  Polymer NumSeqs
      Minimum:        1       605     500     0       3       1
      2.5%-tile:      18      628     507     0       4       106087
      25%-tile:       18      650     530     0       4       1060862
      Median:         18      717     555     1       5       2121723
      75%-tile:       18      754     566     1       5       3182584
      97.5%-tile:     44      754     569     1       7       4137359
      Maximum:        53      771     575     1       11      4243445
      Mean:   20.5771 706.101 547.62  0.508047        4.92197
      # of Seqs:      4243445
     
      Output File Names: 
      Zanne_LSU_aligned.trim.unique.pick.good.filter.summary
```
Extract sequence names maintained in filtered alignment and subset mothur files to only those names.
```
mothur > list.seqs(fasta=Zanne_LSU_aligned.trim.unique.pick.good.filter.fasta)
    
      Output File Names: 
      Zanne_LSU_aligned.trim.unique.pick.good.filter.accnos
      
mothur > get.seqs(accnos=Zanne_LSU_aligned.trim.unique.pick.good.filter.accnos, name=Zanne-LSU_aligned.trim.names) 
     
      Output File Names:
      Zanne-LSU_aligned.trim.pick.names
      
mothur > get.seqs(accnos=Zanne_LSU_aligned.trim.unique.pick.good.filter.accnos, name=LSU.groups) \n",
      
      Output File Names: 
      LSU.pick.groups
```
      
#####8. Phylogenetic Analysis
Reconstruct a neighbor joining tree from the LSU alignment. 

*Note: this command did not sucessfully run on a 30 gb ram server for a 5 million sequence alignment.*
```
mothur > clearcut(fasta=Zanne_LSU_aligned.trim.unique.pick.good.filter.fasta, DNA=t, verbose=t)
```

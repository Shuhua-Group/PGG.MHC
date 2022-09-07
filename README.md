# PGG.MHC
Database related code  
The code here is mainly used to set up the analysis part of the database to run  
# HLA Imputation  

***SNP2HLA_workflow.py*** use **SNP2HLA** to do the imputation of HLA alleles from genotyping data.
```
usage: SNP2HLA_workflow.py [-h] -f VCF -o OUT -p PREFIX [-x THREADS]
                           [-w WINDOWSIZE] -v {38,19,18} -r REFERENCE_PANEL

optional arguments:
  -h, --help            show this help message and exit
  -f VCF, --vcf VCF     vcf file input bgzip and tabix
  -o OUT, --out OUT     output dir
  -p PREFIX, --prefix PREFIX
                        output prefix
  -x THREADS, --threads THREADS
                        threads
  -w WINDOWSIZE, --windowsize WINDOWSIZE
                        SNP2HLA window_size
  -v {38,19,18}, --version {38,19,18}
                        SNP versions
  -r REFERENCE_PANEL, --reference_panel REFERENCE_PANEL
                        reference_panel

```
***dosage_result_to_hla_type.py*** was used to sort out the HLA alleles from the dosage result.
```
usage: dosage_result_to_hla_type.py [-h] -d DOSAGE -o OUT -f FAM

optional arguments:
  -h, --help            show this help message and exit
  -d DOSAGE, --dosage DOSAGE
                        dosage results
  -o OUT, --out OUT     output dir
  -f FAM, --fam FAM     fam file


```
For more information ,you can visit:
[HLA Imputation Instructions](https://pog.fudan.edu.cn/pggmhc/#/help/tool/imputation)  

# HLA Association
After install PyHLA,The following parameters were used to analyze the association between different controls:
```
PyHLA.py 
 -i INPUT, --input INPUT
 -o OUT, --out OUT
 -d {2,4,6}, --digit {2,4,6},default 4
 -a, --assoc association analysis
 -m {allelic,dom,rec,additive}, --model {allelic,dom,rec,additive} genetic model, default allelic
 -t {fisher,chisq,logistic,linear}, statistical test method,default fisher
 -f FREQ, --freq FREQ  minimal frequency, default 0
 -j {FDR,FDR_BY,Bonferroni,Holm}, --adjust ,p value correction, default FDR
--digit 4               [Default]
--test fisher           [Default]
--model allelic         [Default]
--freq 0                [Default]
--adjust FDR            [Default]
--out output.txt        [Default]
```
For more information ,you can visit:
[HLA Association Instructions](https://pog.fudan.edu.cn/pggmhc/#/help/tool/comparison)
# Reference
**SNP2HLA**: Xiaoming Jia*, Buhm Han*, Suna Onengut-Gumuscu, Wei-Min Chen, Patrick J. Concannon, Stephen S. Rich, Soumya Raychaudhuri, Paul I.W. de Bakker. "Imputing Amino Acid Polymorphisms in Human Leukocyte Antigenes." PLoS One. 8(6):e64683. 2013.  

**PyHLA**:Yanhui Fan, You-Qiang Song. (2016) PyHLA: tests for association between HLA alleles and diseases. BMC Bioinformatics. 2017. 18:90
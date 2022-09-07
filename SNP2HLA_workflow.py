#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@time        :2021/10/22 15:58:25
@Author      :masen
@Mail        :masen2019@sibs.ac.cn   
'''
import os 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f','--vcf', required=True, help='vcf file input bgzip and tabix')
parser.add_argument('-o','--out', required=True, help='output dir')
parser.add_argument('-p','--prefix', required=True, help='output prefix')
parser.add_argument('-x','--threads',default=32, help='threads')
parser.add_argument('-w','--windowsize',default=1000, help='SNP2HLA window_size')
parser.add_argument('-v','--version',choices=['38','19','18'],required=True ,help='SNP versions')
parser.add_argument('-r','--reference_panel',required=True, help='reference_panel')
args = parser.parse_args()

vcf_input=args.vcf
out_put_dir=args.out
window_size=args.windowsize
prefix=args.prefix
threads=args.threads
version=str(args.version)
ref_panel=args.reference_panel

###source 
#####hg38_liftover to hg18
if version=="38":
    os.system("CrossMap.py vcf /resources/liftover/chain/hg38ToHg19.over.chain.gz {vcf} /resources/hg19/hg19_ucsc_chr/hg19.fa {out_put_dir}/{prefix}_hg19_version.vcf;CrossMap.py vcf /resources/liftover/chain/hg19ToHg18.over.chain.gz {out_put_dir}/{prefix}_hg19_version.vcf /resources/hg18/hg18.fa {out_put_dir}/{prefix}_hg18_version.vcf;bgzip {out_put_dir}/{prefix}_hg18_version.vcf;tabix -p vcf {out_put_dir}/{prefix}_hg18_version.vcf.gz".format(out_put_dir=out_put_dir,prefix=prefix,vcf=vcf_input))
    os.system("bcftools norm --threads {threads} -d exact --check-ref wx -f /resources/hg18/hg18.fa {out_put_dir}/{prefix}_hg18_version.vcf.gz -Oz -o {out_put_dir}/{prefix}_hg18_version_norm.vcf.gz;tabix -p vcf {out_put_dir}/{prefix}_hg18_version_norm.vcf.gz".format(out_put_dir=out_put_dir,prefix=prefix,threads=threads))
    os.system("bcftools annotate --threads {threads} --set-id '%CHROM\_%POS\_%REF\_%FIRST_ALT' {out_put_dir}/{prefix}_hg18_version_norm.vcf.gz -Oz -o {out_put_dir}/{prefix}_hg18_version_setid.vcf.gz;tabix -p vcf {out_put_dir}/{prefix}_hg18_version_setid.vcf.gz".format(out_put_dir=out_put_dir,prefix=prefix,threads=threads))
    os.system("bcftools annotate --threads {threads} -a /HLA_reference_panel/dbsnp/dbSNP_151_hg18_chr6.vcf.gz -c ID  {out_put_dir}/{prefix}_hg18_version_setid.vcf.gz -Oz -o {out_put_dir}/{prefix}_hg18_version_rssnp.vcf.gz;tabix -p vcf {out_put_dir}/{prefix}_hg18_version_rssnp.vcf.gz".format(out_put_dir=out_put_dir,prefix=prefix,threads=threads))
    os.system("bcftools view --threads {threads} -m2 -M2 -v snps {out_put_dir}/{prefix}_hg18_version_rssnp.vcf.gz -Oz -o {out_put_dir}/{prefix}_hg18_version_filter.vcf.gz ;tabix -p vcf {out_put_dir}/{prefix}_hg18_version_filter.vcf.gz".format(out_put_dir=out_put_dir,prefix=prefix,threads=threads))

    os.system("rm {out_put_dir}/{prefix}_hg18_version.vcf* {out_put_dir}/{prefix}_hg19_version.vcf* {out_put_dir}/{prefix}_hg18_version_rssnp.vcf.gz* {out_put_dir}/{prefix}_hg18_version_setid.vcf.gz* {out_put_dir}/{prefix}_hg18_version_norm.vcf.gz*".format(out_put_dir=out_put_dir,prefix=prefix))

    os.system("plink --double-id --threads  {threads} --vcf {out_put_dir}/{prefix}_hg18_version_filter.vcf.gz --geno 0.1 --maf 0.001  --make-bed --vcf-half-call m --out {out_put_dir}/{prefix}_hg18".format(out_put_dir=out_put_dir,prefix=prefix,threads=threads))

    os.system("cd /bio/SNP2HLA/SNP2HLA_package_v1.0.3/SNP2HLA;./SNP2HLA.csh {out_put_dir}/{prefix}_hg18 {ref_panel} {out_put_dir}/{prefix}_snp2hla ./plink 80000 {windows}".format(ref_panel=ref_panel,out_put_dir=out_put_dir,prefix=prefix,windows=window_size))

elif version=="19":
    os.system("CrossMap.py vcf /resources/liftover/chain/hg19ToHg18.over.chain.gz {vcf} /resources/hg18/hg18.fa {out_put_dir}/{prefix}_hg18_version.vcf;bgzip {out_put_dir}/{prefix}_hg18_version.vcf;tabix -p vcf {out_put_dir}/{prefix}_hg18_version.vcf.gz".format(out_put_dir=out_put_dir,prefix=prefix,vcf=vcf_input))

    os.system("bcftools norm --threads {threads} -d exact --check-ref wx -f /resources/hg18/hg18.fa {out_put_dir}/{prefix}_hg18_version.vcf.gz -Oz -o {out_put_dir}/{prefix}_hg18_version_norm.vcf.gz;tabix -p vcf {out_put_dir}/{prefix}_hg18_version_norm.vcf.gz".format(out_put_dir=out_put_dir,prefix=prefix,threads=threads))
    os.system("bcftools annotate --threads {threads} --set-id '%CHROM\_%POS\_%REF\_%FIRST_ALT' {out_put_dir}/{prefix}_hg18_version_norm.vcf.gz -Oz -o {out_put_dir}/{prefix}_hg18_version_setid.vcf.gz;tabix -p vcf {out_put_dir}/{prefix}_hg18_version_setid.vcf.gz".format(out_put_dir=out_put_dir,prefix=prefix,threads=threads))
    os.system("bcftools annotate --threads {threads} -a /HLA_reference_panel/dbsnp/dbSNP_151_hg18_chr6.vcf.gz -c ID  {out_put_dir}/{prefix}_hg18_version_setid.vcf.gz -Oz -o {out_put_dir}/{prefix}_hg18_version_rssnp.vcf.gz;tabix -p vcf {out_put_dir}/{prefix}_hg18_version_rssnp.vcf.gz".format(out_put_dir=out_put_dir,prefix=prefix,threads=threads))
    os.system("bcftools view --threads {threads} -m2 -M2 -v snps {out_put_dir}/{prefix}_hg18_version_rssnp.vcf.gz -Oz -o {out_put_dir}/{prefix}_hg18_version_filter.vcf.gz ;tabix -p vcf {out_put_dir}/{prefix}_hg18_version_filter.vcf.gz".format(out_put_dir=out_put_dir,prefix=prefix,threads=threads))

    os.system("rm  {out_put_dir}/{prefix}_hg18_version.vcf* {out_put_dir}/{prefix}_hg18_version_setid.vcf.gz* {out_put_dir}/{prefix}_hg18_version_norm.vcf.gz* {out_put_dir}/{prefix}_hg18_version_rssnp.vcf.gz*".format(out_put_dir=out_put_dir,prefix=prefix))
    os.system("plink  --double-id --threads  {threads} --vcf {out_put_dir}/{prefix}_hg18_version_filter.vcf.gz --geno 0.1 --maf 0.001  --make-bed --vcf-half-call m --out {out_put_dir}/{prefix}_hg18".format(out_put_dir=out_put_dir,prefix=prefix,threads=threads))

    os.system("cd /bio/SNP2HLA/SNP2HLA_package_v1.0.3/SNP2HLA;./SNP2HLA.csh {out_put_dir}/{prefix}_hg18 {ref_panel} {out_put_dir}/{prefix}_snp2hla  ./plink 80000 {windows}".format(ref_panel=ref_panel,out_put_dir=out_put_dir,prefix=prefix,windows=window_size))

elif version=="18":
    os.system("plink  --double-id --threads  {threads} --vcf {vcf} --geno 0.1 --maf 0.001  --make-bed --vcf-half-call m --out {out_put_dir}/{prefix}_hg18".format(out_put_dir=out_put_dir,prefix=prefix,threads=threads,vcf=vcf_input))
    os.system("cd /bio/SNP2HLA/SNP2HLA_package_v1.0.3/SNP2HLA;./SNP2HLA.csh {out_put_dir}/{prefix}_hg18 {ref_panel} {out_put_dir}/{prefix}_snp2hla  ./plink 80000 {windows}".format(ref_panel=ref_panel,out_put_dir=out_put_dir,prefix=prefix,windows=window_size))

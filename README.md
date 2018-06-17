# Deepssv: detecting somatic small variants in paired tumor and normal sequencing data with convolutional neural network

Deepssv takes as input a mixed pileup file generated by samtools from tumor and normal BAM files. It first operates on each genomic site independently to identify candidate somatic sites based on the criteria we have defineds. Next it encodes the mapping information samples that are readily available in the pileup format file around the candidate somatic sites into an array. Each array is a spatial representation of mapping information adapted for convolutional architecture. Then the convolutional neural network (CNN) model trained on experimentally validated somatic events evaluates the information in these arrays to obtain additional support for true positives and filter false positive predictions. Finally, potential somatic small variants determined by the CNN model are generated in the variant call format (VCF). 


#### Deepssv was tested on ubuntu 16.04 LTS and requires Python 3.

## Prerequisites:

TensorFlow 1.8.0

Please see https://www.tensorflow.org/install/install_linux for how to install TensorFlow.


## Getting started

1. Run samtools (tested version: 1.8) to convert tumor and normal BAM files to a mixed pileup file required by Deepssv:

        samtools mpileup -B -d 100 -f /path/to/ref.fasta [-l] [-r] -q 10 -O -s -a /path/to/tumor.bam /path/to/normal.bam > /path/to/mixed_pileup_file

   Note: For the case of applying Deepssv on a part of the whole genome, specify the genomic region via the option -l or -r, and increase the BED entry by 110 base pairs in each direction.

2. Run identi_candi_sites.py to identify candidate somatic small variants from the mixed pileup file:

        identi_candi_sites.py
        --Tumor_Normal_mpileup /path/to/mixed_pileup_file
        --Candidate_somatic_sites /path/to/candidate_sites

3. Run mapping_infor_candi_sites.py to create a file with mapping information for candidate somatic small variant sites and their neighbours as input for trained CNN model:

        mapping_infor_candi_sites.py
        --Candidate_validated_somatic_sites /path/to/candidate_validated_sites
        --Tumor_Normal_mpileup /path/to/mixed_pileup_file
        --Mapping_information_file /path/to/mapping_infor_file

4. Run model_infer.py to predict somatic small variants:

        model_infer.py
        --checkpoint_file /path/to/trained_CNN_model
        --Mapping_information_file_inference /path/to/mapping_infor_file
        --vcf_file /path/to/vcf_file
        --Candidate_somatic_sites /path/to/candidate_sites
        
## Fine-tuning the CNN model
To fine-tune the CNN model, run the first step with the BED file of validated somatic small variant sites, 
  
   
Please help us improve Deepssv, by reporting bugs or any ideas on how to make things better. You can submit an issue or send me an email.

Jing Meng        

jing.mengrabbit@gmail.com

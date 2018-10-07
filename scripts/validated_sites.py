#!/usr/bin/env python

'''Create a file with indexes for validated somatic small variant sites.
'''

import argparse
import time
import itertools
import pandas as pd

parser = argparse.ArgumentParser()

parser.add_argument('--Tumor_Normal_mpileup', required=True, metavar='pileup', help='a mixed mpileup file from tumor and normal bam files generated by samtools')
parser.add_argument('--mpileup_index', required=True, metavar='file', help='a file with indexes for genomic sites in the mixed mpileup file')
parser.add_argument('--Validated_labels', required=True, metavar='file', help='a file for validated sites with labels')
parser.add_argument('--Validated_somatic_sites', required=True, metavar='file', help='a file with indexes for validated sites')

args = parser.parse_args()

def pairwise(iterable, n = 110):
    '''Return every pair of items that are separated by n items from iterable.
       s --> (s[0], s[n]), (s[1], s[n+1]), (s[2], s[n+2]), ...'''
    a, b = itertools.tee(iterable)
    next(itertools.islice(a, n, n), None)
    next(itertools.islice(b, 2*n, 2*n), None)
    return zip(a, b)

def main(args):
    with open(args.Tumor_Normal_mpileup, 'rt') as TN, open(args.mpileup_index, 'wt') as Cs:
        n = 110
        k = 10   # depth in tumor and normal
        combi = pairwise(enumerate(TN))
        
        for line, line_pair in combi:
            # look at a genomic site and its next 110 site
            line_content = line[1].rstrip('\n').split('\t')
            line_pair_content = line_pair[1].rstrip('\n').split('\t')

            if line_content[0] == line_pair_content[0] and (int(line_pair_content[1]) - int(line_content[1]) == n):
                if line_content[2] not in 'Nn' and int(line_content[3]) >= k and int(line_content[8]) >= k:
                    Cs.write(str(line[0]) + '\t' + str(line_content[0]) + '\t' + str(line_content[1]) + '\n')
                else:
                    pass         
            else:
                # ignore the genomic site if its next 110 site does not exist
                next(itertools.islice(combi, 2*n-1, 2*n-1), None)         
    
    df1 = pd.read_table(args.mpileup_index, sep = '\t', header = None)
    df2 = pd.read_table(args.Validated_labels, sep = '\t', header = None)
    df1.merge(df2, left_on=[1,2], right_on=[0,1]).loc[:, ['0_x', '1_x', '2_x', '2_y']].to_csv(args.Validated_somatic_sites, sep='\t', header=False, index=False)

if __name__ == '__main__':
    start_time = time.time()
    main(args)
    print('--- %s seconds ---' %(time.time() - start_time))

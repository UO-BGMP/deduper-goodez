#!/usr/bin/env python3

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", required=True)
parser.add_argument("-p", "--paired", action="store_true")
parser.add_argument("-u", "--umi")
args = parser.parse_args()

# If user specifies paired-end option, exit with error
if args.paired:
    raise NameError('Paired-end data is not yet supported')

# If user supplies a file of UMIs, add them to a list
if args.umi:
    umi_list = []
    with open(args.umi, 'r') as umi_file:
        for line in umi_file:
            umi_list.append(line.strip())
else:
    no_list = True

#*************
# FUNCTIONS  *********************************************************
#*************

def umi_check(UMI):
    '''Checks if the UMI exists in UMI list given by user'''
    try:
        if no_list:
            return True
        if UMI in umi_list:
            return True
    except NameError:
        pass
        
    if UMI in umi_list:
        return True
    else:
        return False # Indicates to throw out this read
    
######
    
def cig_check(cigar):
    '''Adjusts original position for potential soft clipping'''
    
    if cigar.endswith("S"): # Ignore soft clipping at the end
        cigar = cigar[:-1] # This will remove the terminal "S"
        
    '''Now without any terminal soft clipping, 
    simply test if "S" is present'''
    
    if "S" in cigar:
        adjust = int(cigar.split("S")[0]) # Take only the integer before 'S'
        adj_pos = pos - adjust
        return adj_pos
    else:
        return pos

######
    
def strand_check(FLAG):
    '''Takes bitwise flag and returns + or - indicating strand'''
    if ((FLAG & 16) != 16):
        return "+"
    else:
        return "-"
    
#*******************
# END OF FUNCTIONS ****************************************************
#*******************

#file prefix to name output
prefix = args.filename[:-4]

# Open output sam file without duplicates
deduped = open(prefix+"_deduped.sam",'w')

# Counter which will tell user number of removed dupes or 
# unrecognized UMIs
dupe_count = 0

with open(args.filename, 'r') as fh:
    line_count = 0
    for read in fh:
        # Write header info to file
        if read.startswith("@"):
            deduped.write(read)
        
        # Lines below the header info
        if read.startswith("@") == False:
            line_count += 1
            line = read.split('\t')
            
            ##########################################
            # Enter this loop after the first line is read
            if line_count > 1:
                
                # First assume line_b is not a duplicate
                dupe = False
                
                ### Same as outer loop below - save current read information ###
                umi_b = line[0].split(':')[7]
                strand_b = strand_check(int(line[1]))
                chrom_b = line[2]
                pos = int(line[3])
                pos_b = cig_check(line[5])
                ###
                
                # Decide if line_b is a duplicate
                if chrom_a == chrom_b:
                    if pos_a == pos_b:
                        if strand_a == strand_b:
                            if umi_a == umi_b:
                                dupe = True
                                dupe_count += 1
                
                # Check if user supplied a list of UMIs, or if UMI is not on the list
                if umi_check(umi_b) != True:
                    dupe = True
                    dupe_count +=1
                    
                if dupe == False:
                    deduped.write(read)
                
            #########################################
                
            # Save UMI for record_a
            umi_a = line[0].split(':')[7]
            
            # Check strandedness from bitwise flag
            strand_a = strand_check(int(line[1]))
                
            # Save chromosome record_a
            chrom_a = line[2]
            
            # Save raw position - not yet adjusted for soft clipping
            pos = int(line[3])
            # Use cigar string to adjust for potential soft clipping
            pos_a = cig_check(line[5])
            
            #########################################
            # Decide if the first line is a valid UMI
            if line_count == 1:
                if umi_check(umi_a) == True:
                    deduped.write(read)
            ##########################################

deduped.close()

print("Done...")
print("Removed " + str(dupe_count) + " duplicates or unrecognized UMIs (if UMIs were supplied)")

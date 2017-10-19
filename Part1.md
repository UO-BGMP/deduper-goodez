# DeDuper Assignment Part 1

#### Zach Goode

---

### Defining the problem

When PCR is used to amplify sequency libraries, it is important to consider how this introduces bias in the abundance of 
different sequences. One way to avoid this bias during library preparation is to label the molecules with unique molecular 
identifiers (UMIs) before performing PCR. This allows us to recognize which reads are amplicons so we can discard them. 
In addition to the UMIs, PCR duplicates can also be recognized within a SAM file after aligning the reads. There are a few clues 
in SAM files which suggest duplication:

* Duplicate reads should have **identical `POS` values** (left-most starting position), provided there is no sequencing error causing the 
position to shift slightly
     * This can be corrected with information from the `CIGAR` string
* Duplicate reads should be **located on the same chromosome** (3rd field of SAM file)
* As mentioned before, duplicate reads should be labeled with **identical UMIs**, provided there is no sequencing error within the UMI

---

### Pseudocode to dedupe a SAM file
##### *NOTE: For now the code is designed for reads which are single-end, uniquely mapped, soft clipped, and untrimmed.*

(Before running the code, sort the BAM file by chromosome and position using `samtools`.)

Utilize `argparse` to take in files and any other options the user might specify

Define UMIs in some form of `list/dictionary` from an input file or manually define them

Open the file and iterate through each line:
* Ignore the header section (lines beginning with `@`)
* Separate the fields of the current line delimited by `tab` characters
* Define relevant local variables
     * UMI = end of 1st field
     * CHROMOSOME = 3rd field
     * POSITION = 4th field
     * CIGAR = 5th field
     * etc.
* Check if the UMI at the end of the first field is a member of our defined UMIs
     * If it does **NOT** match, throw out this read and move to the next line
* Check in `CIGAR` if the read is soft clipped at the left-most end
     * If so, subtract the amount clipped from the `POSITION`
* Check if the current `UMI` and adjusted `POSITION` are novel
     * If they **ARE** new --> write to the updated SAM file
     * If **NOT** new --> throw out this read and move to the next line

#### Useful functions:

```
def UMI_check(UMI, UMI_list):
    if the UMI is in UMI_list:
        return True
    if UMI is not in the UMI_list:
        return False
```

```
def CIGAR_check(CIGAR, POSITION):
    if CIGAR string begins with soft clipping:
        subtract from POSITION
        
    return new POSITION
```

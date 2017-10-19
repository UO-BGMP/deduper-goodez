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


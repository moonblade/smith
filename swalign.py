#!/bin/python2
import swalign
sw = swalign.LocalAlignment(
    swalign.NucleotideScoringMatrix(match, mismatch),
    gap_penalty, gap_extension_penalty, gap_extension_decay)

aln = sw.align(r_seq, q_seq, ref_name, query_name)
aln.dump()
#!/usr/bin/env python3
"""Convert FASTA alignment to PHYLIP interleaved format for PAML.

Usage: python3 fasta2phylip.py <input.fasta> <output.phy>

PAML requires PHYLIP format with:
  - Header: num_species seq_length
  - Species name (10 chars) + sequence blocks
"""
import sys


def fasta_to_phylip(fasta_path, phy_path):
    names = []
    seqs = []

    with open(fasta_path) as f:
        name = None
        seq = []
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if name is not None:
                    names.append(name)
                    seqs.append(''.join(seq))
                name = line[1:].split()[0][:30]  # truncate long names
                seq = []
            elif line:
                seq.append(line.replace(' ', ''))
        if name is not None:
            names.append(name)
            seqs.append(''.join(seq))

    n = len(names)
    seqlen = len(seqs[0])

    # Validate all sequences same length
    for i, s in enumerate(seqs):
        if len(s) != seqlen:
            print(f"Error: sequence {names[i]} length {len(s)} != {seqlen}", file=sys.stderr)
            sys.exit(1)

    with open(phy_path, 'w') as f:
        f.write(f"  {n}  {seqlen}\n")
        # Write interleaved: first block of 60 chars for all species, then next block, etc.
        block_size = 60
        for block_start in range(0, seqlen, block_size):
            for i in range(n):
                name_field = names[i][:10].ljust(10)
                block = seqs[i][block_start:block_start + block_size]
                if block_start == 0:
                    f.write(f"{name_field}{block}\n")
                else:
                    f.write(f"{'':10}{block}\n")
            f.write("\n")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 fasta2phylip.py <input.fasta> <output.phy>", file=sys.stderr)
        sys.exit(1)
    fasta_to_phylip(sys.argv[1], sys.argv[2])

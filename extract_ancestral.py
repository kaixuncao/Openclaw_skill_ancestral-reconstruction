#!/usr/bin/env python3
"""Extract ancestral sequences from PAML rst file to FASTA format.

Usage: python3 extract_ancestral.py <rst_file> [> output.fasta]

PAML rst file contains ancestral sequences under:
  "Ancestral sequences by node (TREE #1)"
Each node has a header line with node number and average PP,
followed by the sequence in blocks of 10 residues.
"""
import sys
import re


def parse_rst(rst_path):
    sequences = {}
    current_node = None
    current_pp = None
    current_seq = []

    with open(rst_path) as f:
        in_ancestral = False
        for line in f:
            line = line.rstrip()

            # Detect start of ancestral section
            if "Ancestral sequences by node" in line:
                in_ancestral = True
                continue

            if not in_ancestral:
                continue

            # Node header: "node #N  PP = X.XXXX ..."
            m = re.match(r'\s*node\s+#(\d+)\s+PP\s*=\s*([\d.]+)', line)
            if m:
                # Save previous node
                if current_node is not None:
                    sequences[current_node] = {
                        'pp': current_pp,
                        'seq': ''.join(current_seq)
                    }
                current_node = int(m.group(1))
                current_pp = float(m.group(2))
                current_seq = []
                continue

            # Sequence line: just amino acid characters (with possible spaces)
            if current_node is not None and line.strip():
                # Skip lines that are clearly not sequence data
                if line.strip().startswith('(') or 'Prob' in line:
                    continue
                # Extract only amino acid letters
                residues = re.findall(r'[A-Z*\-]', line)
                if residues:
                    current_seq.extend(residues)

    # Save last node
    if current_node is not None:
        sequences[current_node] = {
            'pp': current_pp,
            'seq': ''.join(current_seq)
        }

    return sequences


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_ancestral.py <rst_file>", file=sys.stderr)
        sys.exit(1)

    rst_path = sys.argv[1]
    sequences = parse_rst(rst_path)

    for node_num in sorted(sequences.keys()):
        info = sequences[node_num]
        print(f">Node{node_num}_avgPP={info['pp']:.4f}")
        seq = info['seq']
        # Print in blocks of 60
        for i in range(0, len(seq), 60):
            print(''.join(seq[i:i+60]))


if __name__ == '__main__':
    main()

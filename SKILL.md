---
name: ancestral-reconstruction
description: |
  Ancestral Sequence Reconstruction (ASR) workflow from species tree to PAML-based ancestral sequences.
  Use when user wants to: (1) build a species tree from OrthoFinder or use a literature tree, (2) run PAML baseml/codeml for ancestral reconstruction, (3) extract and analyze ancestral protein sequences.
  Covers OrthoFinder, IQ-TREE2, trimAl, and PAML (baseml/codeml) integration.
---

# Ancestral Sequence Reconstruction (ASR)

Complete workflow from protein sequences to ancestral sequences using PAML.

## Prerequisites

- **PAML** (codeml/baseml): `/home/kiz-412/soft/paml4.9j/bin/`
- **IQ-TREE2**: `/home/kiz-412/soft/iqtree-2.2.2.7-Linux/bin/`
- **trimAl**: `trimAl` in PATH
- **MAFFT**: `mafft` in PATH
- **OrthoFinder**: `orthofinder` in PATH (if building species tree from proteomes)

## Workflow Overview

```
Protein FASTA → MAFFT alignment → trimAl trim → IQ-TREE gene tree
                                                      ↓
Proteomes → OrthoFinder → Species tree ──→ PAML codeml → Ancestral sequences
              (or literature tree)
```

## Step 1: Sequence Alignment & Trimming

```bash
# MAFFT alignment
mafft --auto input.fasta > aligned.fasta

# trimAl trimming (remove poorly aligned columns)
trimal -in aligned.fasta -out trimmed.fasta -automated1
```

## Step 2: Gene Tree (IQ-TREE2)

```bash
iqtree2 -s trimmed.fasta -m MFP -bb 1000 -nt AUTO
```

Output: `trimmed.fasta.treefile` (gene tree, NOT for species tree in publications)

## Step 3: Species Tree

### Option A: OrthoFinder (Recommended)

Requires whole-proteome FASTA files for all species.

```bash
orthofinder -f proteomes_dir/ -t 8
```

Output species tree: `OrthoFinder/Results_*/Species_Tree/SpeciesTree_rooted.txt`

**Critical**: The species tree must be derived independently from the gene of interest. Using a single-gene tree as species tree is a fatal flaw in peer review.

### Option B: Literature Tree

Construct from published phylogenies. Format as Newick with branch lengths.

### Species Tree Preparation

Ensure species names in the tree match those in the alignment FASTA headers exactly.

```bash
# Check name consistency
grep ">" trimmed.fasta | sed 's/>//' | sort > names_alignment.txt
# Compare with tree leaf names
```

## Step 4: PAML Ancestral Reconstruction

### Control File Template (`codeml.ctl`)

```
      seqfile = trimmed.phy   * protein alignment in PHYLIP format
     treefile = species.nwk   * species tree with branch lengths
      outfile = mlc_output    * main output file

        noisy = 0
      verbose = 0
      runmode = 0

      seqtype = 2   * 1:codon 2:AA 3:codon+AA
        ndata = 1
        clock = 0
       aaRatefile = dat/jones.dat  * or wag.dat, dayhoff.dat

        model = 0
        Mgene = 0

    fix_alpha = 1
        alpha = 0
       Malpha = 0
        ncatG = 5

        getSE = 0
 RateAncestor = 1   * 0:no 1:ANCEML 2:Bayes
  Small_Diff = 7e-6
    cleandata = 0
       method = 0
```

### Run PAML

```bash
# Convert FASTA to PHYLIP interleaved format
# (use scripts/fasta2phylip.py)

cd paml_workdir/
/home/kiz-412/soft/paml4.9j/bin/codeml codeml.ctl
```

### Key Parameters

- `seqtype = 2` for protein (amino acid) analysis
- `RateAncestor = 1` enables ancestral reconstruction (ANCEML)
- `model = 0` for empirical amino acid substitution model (Jones/WAG/etc.)

## Step 5: Extract Ancestral Sequences

From `rst` file, sequences are under "Ancestral sequences by node (TREE #1)".

Parse with:

```bash
# Extract from rst file (see scripts/extract_ancestral.py)
python3 scripts/extract_ancestral.py rst > ancestral.fasta
```

## Output Interpretation

| File | Content |
|------|---------|
| `mlc_*` | Full PAML output with lnL, tree, parameters |
| `rst` | Site-by-site ancestral probabilities |
| `ancestral_*.fasta` | Reconstructed ancestral sequences |

### Key Metrics

- **lnL** (log-likelihood): Higher = better tree fit. Compare trees: ΔlnL > 2 is significant.
- **avgPP**: Average posterior probability per node. >0.9 = high confidence.
- **Node numbering**: PAML starts internal nodes from N+1 (N = number of leaves).

## File Organization

```
project/
├── input.fasta                    * Raw protein sequences
├── aligned.fasta                  * MAFFT output
├── trimmed.fasta                  * trimAl output
├── species_tree.nwk               * Species tree (Newick)
├── paml_asr/
│   ├── codeml.ctl                 * PAML control file
│   ├── trimmed.phy                * PHYLIP format alignment
│   ├── mlc_*                      * PAML output
│   ├── rst                        * Detailed reconstruction
│   └── ancestral_*.fasta          * Extracted ancestral sequences
└── README.md                      * Analysis documentation
```

## Common Pitfalls

1. **Gene tree ≠ species tree**: Never use single-gene tree as species tree in publications
2. **Name mismatch**: Species names must be identical between tree and alignment
3. **Codon vs protein**: Use `seqtype=2` for protein; `seqtype=1` for codon
4. **Gap handling**: `cleandata=1` removes sites with gaps; `cleandata=0` keeps them
5. **Branch lengths**: Species tree should have branch lengths; use IQ-TREE or r8s if missing

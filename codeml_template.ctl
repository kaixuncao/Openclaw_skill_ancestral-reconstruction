* PAML codeml control file for Ancestral Sequence Reconstruction
* Modify paths and parameters as needed

      seqfile = trimmed.phy      * PHYLIP format alignment (protein)
     treefile = species.nwk      * Species tree (Newick format)
      outfile = mlc_output       * Main output file

        noisy = 0   * 0,1,2,3: how much rubbish on the screen
      verbose = 0   * 1: detailed output
      runmode = 0   * 0: user tree

      seqtype = 2   * 1:codon  2:amino acid  3:codon+AA
        ndata = 1   * number of data sets
        clock = 0   * 0:no clock  1:clock  2:local clock
       aaRatefile = dat/jones.dat  * substitution model
*       aaRatefile = dat/wag.dat   * alternative: WAG model
*       aaRatefile = dat/dayhoff.dat  * alternative: Dayhoff model

        model = 0   * model for amino acids
        Mgene = 0   * 0:rates, 1:separate, 2:diff pi, 3:diff kapa, 4:all diff

    fix_alpha = 1   * 0:estimate gamma  1:fix alpha
        alpha = 0   * 0:infinity (constant rate)
       Malpha = 0   * 1:diff alpha for each gene
        ncatG = 5   * number of categories in dG

        getSE = 0   * 0:don't want them  1:want S.E.s
 RateAncestor = 1   * 0:no  1:ANCEML  2:Bayes (recommended for protein)
  Small_Diff = 7e-6
    cleandata = 0   * 1:remove sites with ambiguity data
       method = 0   * 0:convergence  1:Newton

from scorer.Scorer import Scorer
from target.Target import Target

import math

# This is a 13 line python function to calculate the sgRNA on-target efficacy score from the article
# "Rational design of highly active sgRNAs for CRISPR-Cas9–mediated gene inactivation"
# by J Doench et al. 2014
# The authors' web tool is available at http://www.broadinstitute.org/rnai/public/analysis-tools/sgrna-design
# Thanks to Cameron Mac Pherson at Pasteur Paris for fixing my original version. Maximilian Haeussler 2014

#TODO in JSON datein schreiben und dann laden

params = [
    # pasted/typed table from PDF and converted to zero-based positions
    (1, 'G', -0.2753771), (2, 'A', -0.3238875), (2, 'C', 0.17212887), (3, 'C', -0.1006662),
    (4, 'C', -0.2018029), (4, 'G', 0.24595663), (5, 'A', 0.03644004), (5, 'C', 0.09837684),
    (6, 'C', -0.7411813), (6, 'G', -0.3932644), (11, 'A', -0.466099), (14, 'A', 0.08537695),
    (14, 'C', -0.013814), (15, 'A', 0.27262051), (15, 'C', -0.1190226), (15, 'T', -0.2859442),
    (16, 'A', 0.09745459), (16, 'G', -0.1755462), (17, 'C', -0.3457955), (17, 'G', -0.6780964),
    (18, 'A', 0.22508903), (18, 'C', -0.5077941), (19, 'G', -0.4173736), (19, 'T', -0.054307),
    (20, 'G', 0.37989937), (20, 'T', -0.0907126), (21, 'C', 0.05782332), (21, 'T', -0.5305673),
    (22, 'T', -0.8770074), (23, 'C', -0.8762358), (23, 'G', 0.27891626), (23, 'T', -0.4031022),
    (24, 'A', -0.0773007), (24, 'C', 0.28793562), (24, 'T', -0.2216372), (27, 'G', -0.6890167),
    (27, 'T', 0.11787758), (28, 'C', -0.1604453), (29, 'G', 0.38634258), (1, 'GT', -0.6257787),
    (4, 'GC', 0.30004332), (5, 'AA', -0.8348362), (5, 'TA', 0.76062777), (6, 'GG', -0.4908167),
    (11, 'GG', -1.5169074), (11, 'TA', 0.7092612), (11, 'TC', 0.49629861), (11, 'TT', -0.5868739),
    (12, 'GG', -0.3345637), (13, 'GA', 0.76384993), (13, 'GC', -0.5370252), (16, 'TG', -0.7981461),
    (18, 'GG', -0.6668087), (18, 'TC', 0.35318325), (19, 'CC', 0.74807209), (19, 'TG', -0.3672668),
    (20, 'AC', 0.56820913), (20, 'CG', 0.32907207), (20, 'GA', -0.8364568), (20, 'GG', -0.7822076),
    (21, 'TC', -1.029693), (22, 'CG', 0.85619782), (22, 'CT', -0.4632077), (23, 'AA', -0.5794924),
    (23, 'AG', 0.64907554), (24, 'AG', -0.0773007), (24, 'CG', 0.28793562), (24, 'TG', -0.2216372),
    (26, 'GT', 0.11787758), (28, 'GG', -0.69774)]

intercept = 0.59763615
gcHigh = -0.1665878
gcLow = -0.2026259


class DoenchScorer(Scorer):

    def __init__(self):
        super().__init__()

    def score(self, target: Target):
        score = intercept
        seq = target.model_sequence
        guide_seq = seq[4:24]
        gc_count = guide_seq.count("G") + guide_seq.count("C")

        if gc_count <= 10:
            gc_weight = gcLow
        if gc_count > 10:
            gc_weight = gcHigh
        score += abs(10 - gc_count) * gc_weight

        for pos, modelSeq, weight in params:
            sub_seq = seq[pos:pos + len(modelSeq)]

            if sub_seq == modelSeq:
                score += weight

        final_score = 1.0 / (1.0 + math.exp(-score))
        return float("{0:.2f}".format(final_score))


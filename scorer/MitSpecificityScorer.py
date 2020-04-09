from scorer.Scorer import Scorer
from target.Target import Target

''' 
For each off-target, the probability of being a true secondary target for Cas9 is estimated as described in Optimized 
CRISPR Design tool (Zhang Lab, MIT)
A score S_off is calculated for each off-target based on the number and position of the mismatches.
The higher the score, the higher the probability of acting as true secondary Cas9 site.
In general, for Cas ß mismatches at last postions ( close to the PAM) strongly decrease the off-target's score.

Source code from https://github.com/maximilianh/crisporWebsite/blob/master/crispor.py
'''

HIT_SCORE_MATRIX = [0, 0, 0.014, 0, 0, 0.395, 0.317, 0, 0.389, 0.079, 0.445, 0.508, 0.613, 0.851, 0.732, 0.828, 0.615,
                    0.804, 0.685, 0.583]


class MitSpecificityScorer(Scorer):

    def __init__(self):
        super().__init__()

    def score(self, target: Target):
        return 4

    def calc_hit_score(self, string1, string2):
        # The Patrick Hsu weighting scheme
        # S. aureus requires 21bp long guides. We fudge by using only last 20bp
        dists = []  # distances between mismatches, for part 2
        mm_count = 0  # number of mismatches, for part 3
        last_mm_pos = None  # position of last mismatch, used to calculate distance

        score1 = 1.0
        for pos in range(0, len(string1)):
            if string1[pos] != string2[pos]:
                mm_count += 1
                if not None == last_mm_pos:
                    dists.append(pos - last_mm_pos)
                score1 *= 1 - HIT_SCORE_MATRIX[pos]
                last_mm_pos = pos
        # 2nd part of the score
        if mm_count < 2:  # special case, not shown in the paper
            score2 = 1.0
        else:
            avg_dist = sum(dists) / len(dists)
            score2 = 1.0 / (((19 - avg_dist) / 19.0) * 4 + 1)
        # 3rd part of the score
        if mm_count == 0:  # special case, not shown in the paper
            score3 = 1.0
        else:
            score3 = 1.0 / (mm_count ** 2)

        score = score1 * score2 * score3 * 100
        return score

    def calc_mit_guide_score(self, hitSum):
        """ Sguide defined on http://crispr.mit.edu/about
        Input is the sum of all off-target hit scores. Returns the specificity of the guide.
        """
        score = 100 / (100 + hitSum)
        score = int(round(score * 100))
        return score

class ScoreCalculator:

    def score_generate(array, total):
        score = 5
        for a in array:
            score = score + a
        final_score = float(score) / total
        return final_score

    def get_eco_level(high_count, eco_size):
        score = float(high_count) / eco_size
        if 0.0 <= score < 0.2:
            return '2'
        elif 0.2 <= score < 0.4:
            return '3'
        elif 0.4 <= score < 0.6:
            return '4'
        elif 0.6 <= score < 0.8:
            return '5'
        else:
            return '6'



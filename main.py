from assignment3 import Ranking

if __name__ == '__main__':

    rnk = Ranking('./judge.txt')
    threshold = 2
    ret = rnk.prec(1, threshold)
    print(ret)
    ret = rnk.recall(1, threshold)
    print(ret)
    ret = rnk.f1_score(1, threshold)
    print(ret)
    ret = rnk.rr_score(1, threshold)
    print(ret)
    ret = rnk.ndcg(1)
    print(ret)
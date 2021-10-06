"""
    Ryan Paulos
    CS 454 - Information Retrieval
    Assignment 3



    Need to read from the sample.txt and judgement document.

"""

import math
import csv


class Ranking(object):
    """
        Initialized with a filepath to the judgement file.
        Hardcoded ingestion of ./sample.txt for query lines.
    """

    def __init__(self, judgement_file: str):
        self.sample_lines: dict = {}  # {<line #>: {'query': <query>, 'urls': [url, url, ...], ...} }
        self.judged_urls: dict = {}  # {'query': {<url>: <judgement>, .. } }
        # Loading judgements (judged_urls)
        with open(judgement_file, 'r') as j_file:
            d_reader: csv.DictReader = csv.DictReader(j_file
                                                      , fieldnames=['query', 'url', 'judgement']
                                                      , delimiter='\t')
            for row in d_reader:
                query: str = row['query']
                url: str = row['url']
                judgement: str = row['judgement']
                if query in self.judged_urls:
                    if judgement in self.judged_urls[query]:
                        self.judged_urls[query][url].append(judgement)
                    else:
                        self.judged_urls[query][url] = judgement
                else:
                    self.judged_urls[query] = {url: judgement}
        # Loading sample.txt
        with open('./sample.txt', 'r') as sample_file:
            fieldnames: list = ['query', 'cookie', 'timestamp']
            for x in range(1, 11):
                fieldnames.append(f'url{x}')
            d_reader: csv.DictReader = csv.DictReader(sample_file
                                                      , fieldnames=fieldnames
                                                      , delimiter='\t')
            line_count = 1
            for row in d_reader:
                query: str = row['query']
                urls: list = []
                for x in range(1, 11):
                    fkey = f'url{x}'
                    urls.append(row[fkey])
                self.sample_lines[line_count] = {'query': query, 'urls': urls}
                line_count += 1

    def _rel(self, query_line: int, thresh: int) -> int:
        # Pulling out required info
        query_deets: dict = self.sample_lines[query_line]
        query: str = query_deets['query']
        judgements: dict = self.judged_urls[query]
        returned_urls: list = query_deets['urls']
        relevant_urls: int = 0
        for url in returned_urls:
            if url in judgements and int(judgements[url]) >= thresh:
                relevant_urls += 1
        return relevant_urls

    def prec(self, query_line: int, thresh: int) -> float:
        """
            rel/k

            # of relevant urls returned over the number of returned urls.

            Assumes k is always 10
        """
        # Calculating score
        relevant_urls: int = self._rel(query_line, thresh)
        k: int = 10
        return relevant_urls / k

    def recall(self, query_line: int, thresh: int) -> float:
        """ relevant urls returned / relevant urls in the dataset"""
        query: str = self.sample_lines[query_line]['query']
        judged_urls: dict = self.judged_urls[query]
        total_rel: int = 0
        for url in judged_urls.keys():
            if int(judged_urls[url]) >= thresh:
                total_rel += 1
        relevant_urls: int = self._rel(query_line, thresh)
        if total_rel == 0:
            return 0
        return relevant_urls / total_rel

    def f1_score(self, query_line: int, thresh: int) -> float:
        """
            1 / ((alpha/prec) + (1-alpha)/recall)
            Assumes alpha to be .5
        """

        alpha: float = .5
        prec: float = self.prec(query_line, thresh)
        recall: float = self.recall(query_line, thresh)
        # den1 - first denominator term
        den1: float
        if prec == 0:
            den1 = 0
        else:
            den1 = alpha / prec
        # den2 - second denominator term
        den2: float
        if recall == 0:
            den2 = 0
        else:
            den2 = (1 - alpha) / recall
        # f1
        f1: float
        if den1 == 0 or den2 == 0:
            return 0
        else:
            f1: float = 1 / (den1 + den2)
        return f1

    def rr_score(self, query_line: int, thresh: int) -> float:
        """
            1/ pos_r     pos_r being the position of the first relevant URL
        :param query_line:
        :param thresh:
        :return:
        """
        # Pulling out required info
        query_deets: dict = self.sample_lines[query_line]
        query: str = query_deets['query']
        judgements: dict = self.judged_urls[query]
        returned_urls: list = query_deets['urls']
        for i, url in enumerate(returned_urls):
            if url in judgements and int(judgements[url]) >= thresh:
                return 1 / (i + 1)
        # @TODO what if no relevant URLS exist? Seems 0
        return 0

    def _dcg(self, judgements: dict, returned_urls: list) -> float:
        sum: float = 0
        for i, url in enumerate(returned_urls):
            if url in judgements:
                rel_i: int = int(judgements[url])
                denom: float = math.log(((i+1) + 1), 2)  # extra +1 to account for zero indexing
                sum += rel_i / denom
        return sum

    def _idcg(self, judgements: dict, returned_urls: list) -> float:
        """ Calls _dcg after ordering top urls """

        # Building list of top-10 scoring urls
        score_pairs: list = []  # list of tuples. (<judgement>, <url>)
        for url in judgements:
            tup: tuple = (judgements[url], url)
            score_pairs.append(tup)
        score_pairs.sort(key=lambda val: int(val[0]))
        score_pairs.reverse()
        # Building url-only list for _dcg consumption
        score_pairs = score_pairs[:10]  # Pruning unneeded values
        urls_only: list = [pair[1] for pair in score_pairs]
        return self._dcg(judgements, urls_only)

    def ndcg(self, query_line: int) -> float:
        """
            dcg / idcg
        """
        # Pulling out required info
        query_deets: dict = self.sample_lines[query_line]
        query: str = query_deets['query']
        judgements: dict = self.judged_urls[query]
        returned_urls: list = query_deets['urls']
        # Calculating value
        dcg: float = self._dcg(judgements, returned_urls)
        idcg: float = self._idcg(judgements, returned_urls)
        return dcg / idcg




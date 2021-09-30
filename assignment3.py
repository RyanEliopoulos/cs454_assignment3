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

    def prec(self, query_line: int, thresh: int) -> float:
        """
            rel/k

            # of relevant urls returned over the number of returned urls.

            Assumes k is always 10
        """
        query_deets: dict = self.sample_lines[query_line]
        query: str = query_deets['query']
        judgements: dict = self.judged_urls[query]
        returned_urls: list = query_deets['urls']
        # Tallying relevant urls
        relevant_urls: int = 0
        for url in returned_urls:
            if url in judgements and int(judgements[url]) >= thresh:
                relevant_urls += 1
        k: int = 10
        return relevant_urls / k


if __name__ == '__main__':

    rnk = Ranking('./judge.txt')
    ret = rnk.prec(1, 3)
    print(ret)
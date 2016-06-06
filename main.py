#!/usr/bin/python3
import argparse
import importlib

parser = argparse.ArgumentParser()

parser.add_argument('-y',
                    '--year',
                    dest="year",
                    help='year to grab',
                    type=int,
                    required=True)
parser.add_argument('-n',
                    '--normalizer',
                    dest="normalizer",
                    help='data normalizer',
                    type=str,
                    default='core.normalizers.BasicNormalizer')
parser.add_argument('-c',
                    '--crawler',
                    dest="crawler",
                    help='data crawler',
                    type=str,
                    default='crawler.uefa.UefaCrawler')

parser.add_argument('-l',
                    '--length',
                    dest="match_count",
                    help='data length',
                    type=int,
                    default=None)


def main(year, normalizer_class, crawler_class):
    normalizer_instance = normalizer_class()
    return crawler_class(year, normalizer_instance)


def get_normalizer_from_str(path_to_class):

    module_name, class_name = path_to_class.rsplit('.', 1)
    mod = importlib.import_module(module_name)
    return getattr(mod, class_name)

if __name__ == "__main__":
    args = parser.parse_args()
    year = args.year
    normalizer_class_name = args.normalizer
    crawler_class_name = args.crawler

    normalizer_class = get_normalizer_from_str(normalizer_class_name)
    crawler_class = get_normalizer_from_str(crawler_class_name)

    crawler = main(year, normalizer_class, crawler_class)
    match_data_list = crawler.get_normalized_game_data_collection(
        args.match_count
        )

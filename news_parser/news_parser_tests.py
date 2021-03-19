import sys
sys.path.insert(0, '..')

from news_parser.news_parser import parse_mailru_news, \
    parse_lentaru_news, parse_yandex_news

mailru_news_data = parse_mailru_news(to_mongo = True)
lentaru_news_data = parse_lentaru_news()
yandex_news_data = parse_yandex_news()
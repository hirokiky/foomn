""" Module for handling and defining what shorten key is.
"""
import math
import re

from sqlalchemy.orm.exc import NoResultFound

from foomn.models import URLMapping

shortenkey_possibility = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
shortenkey_regexp = re.compile(r'^[a-zA-Z0-9]{2,}$')


class InvalidShortenKey(Exception):
    pass


class ShortenKeyDoesNotExist(Exception):
    pass


def mapping_code_to_id(mapping_code):
    """ Translate mapping code to id value of URLMapping.
    """
    ret = 0
    base = len(shortenkey_possibility)
    for digit, character in enumerate(reversed(mapping_code)):
        index = shortenkey_possibility.find(character)
        if index == -1:
            raise InvalidShortenKey
        ret += index * base ** digit
    return ret


def mapping_id_to_code(mapping_id):
    """ Translate mapping id to code
    """
    if not isinstance(mapping_id, int) or mapping_id <= 0:
        raise ValueError('Apply int more than 0')

    base = len(shortenkey_possibility)
    return ''.join([shortenkey_possibility[(mapping_id//base**i) % base]
                    for i in range(int(math.log(mapping_id, base)), -1, -1)])


def parse_shortenkey(shortenkey):
    """ Return region code and mapping code
    """
    if shortenkey_regexp.match(shortenkey) is None:
        raise InvalidShortenKey

    region_code = shortenkey[0]
    mapping_code = shortenkey[1:]
    return region_code, mapping_code


def generate_shortenkey(url):
    """ Save a given url and return it's shorten key
    """


def expand_shortenkey(shortenkey):
    """ Return URL to correspond to a given shorten key
    """
    region_code, mapping_code = parse_shortenkey(shortenkey)
    mapping_id = mapping_code_to_id(mapping_code)

    try:
        mapping = URLMapping.query.filter(
            (URLMapping.region_code == region_code) & (URLMapping.mapping_id == mapping_id)
        ).one()
    except NoResultFound:
        raise ShortenKeyDoesNotExist
    return mapping.url

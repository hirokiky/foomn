import re

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    validates,
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

region_code_possibility = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
url_regexp = re.compile(
    r'^(?:http|ftp)s?://'  # schema
    r'(?P<host>(?:[A-Z0-9-]+?\.)+[A-Z]+)'  # host
    r'(?::\d+)?'  # port
    r'(?:/?|[/?]\S+)$',  # path
    re.IGNORECASE
)
IGNORING_HOSTS = ['foo.mn', 'bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly', 'htn.to', 'p.tl']


class URLMapping(Base):
    """ Table for mapping URL and mapping id
    mapping id is calculated from shorten key
    """
    __tablename__ = 'urlmapping'
    query = DBSession.query_property()

    mapping_id = sa.Column(sa.Integer(), primary_key=True)
    region_code = sa.Column(sa.String(1))
    url = sa.Column(sa.String(1024))

    @validates('region_code')
    def validate_region_code(self, key, region_code):
        if region_code not in region_code_possibility:
            raise ValueError('Invalid region code')
        return region_code

    @validates('url')
    def validate_url(self, key, url):
        matched = url_regexp.match(url)
        if matched is None:
            raise ValueError('Invalid URL')
        if matched.group('host') in IGNORING_HOSTS:
            raise ValueError('Host of specified URL was ignored')
        return url

    __table_args__ = (
        sa.UniqueConstraint('mapping_id', 'region_code'),
        sa.Index('idx__mapping_id__region_code', 'mapping_id', 'region_code')
    )

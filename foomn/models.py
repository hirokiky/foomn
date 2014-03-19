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
url_regexp = re.compile(r'^$')


class URLMapping(Base):
    """ Table for mapping URL and mapping id
    mapping id is calculated from shorten key
    """
    __tablename__ = 'urlmapping'
    query = DBSession.query_property()

    mapping_id = sa.Column(sa.SmallInteger(), nullable=False, primary_key=True)
    region_code = sa.Column(sa.String(1))
    url = sa.Column(sa.String(1024))

    @validates('region_code')
    def validate_region_code(self, key, region_code):
        if region_code not in region_code_possibility:
            raise ValueError('Invalid region code')
        return region_code

#     @validates('url')
#     def validate_url(self, key, url):
#         if url_regexp.match(url) is None:
#             raise ValueError('Invalid URL')
#         return url

    __table_args__ = (
        sa.UniqueConstraint('mapping_id', 'region_code'),
        sa.Index('idx__mapping_id__region_code', 'mapping_id', 'region_code')
    )

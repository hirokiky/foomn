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
uri_regexp = re.compile(r'^$')


class URIMapping(Base):
    """ Table for mapping URI and mapping id
    mapping id is calculated from shorten key
    """
    __tablename__ = 'urimapping'
    query = DBSession.query_property()

    mapping_id = sa.Column(sa.SmallInteger(), nullable=False, primary_key=True)
    region_code = sa.Column(sa.String(1))
    uri = sa.Column(sa.String(1024))

    @validates('region_code')
    def validate_region_code(self, key, region_code):
        if region_code not in region_code_possibility:
            raise ValueError('Invalid region code')
        return region_code

#     @validates('uri')
#     def validate_uri(self, key, uri):
#         if uri_regexp.match(uri) is None:
#             raise ValueError('Invalid URI')
#         return uri

    __table_args__ = (
        sa.UniqueConstraint('mapping_id', 'region_code'),
        sa.Index('idx__mapping_id__region_code', 'mapping_id', 'region_code')
    )

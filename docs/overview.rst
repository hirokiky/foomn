========
Overview
========

Core implementation of a URL shortening service named 'foomn'.
foomn is one of open source distributed URL shortening service.

core
====

This foomn project is for implementing of core features.
It will solve shorten URLs and cooperate with another nodes.
Features like tracking user accesses should be provided
by some another projects.
This foomn project only provide some hook points to be able to
be expanded and extended more easily.

DUSS
====

DUSS is short for distributed URL shortening service which provides
indissoluble URL shortening service.
Generally, shorten URLs are depending one service and if the service
end, all of them will be unavailable.

Each nodes of foomn have 'region' and generate own shorten URLs for each
regions.
Duplicated URL never generated between different regions.

Mapping file for registered URL and shorten URL should be downloaded
with it's checksum at all times.
When your server ends, you should entrust the mapping file to another
node and redirect requests to it.

Of cause you can't entrust it to a node which has same region you've used.

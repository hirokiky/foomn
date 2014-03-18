========
Overview
========

Core implementation of a URI shortening service named 'foomn'.
foomn is one of open source distributed URI shortening service.

core
====

This foomn project is for implementing of core features.
It will solve shorten URIs and cooperate with another nodes.
Features like tracking user accesses should be provided
by some another projects.
This foomn project only provide some hook points to be able to
be expanded and extended more easily.

DUSS
====

DUSS is short for distributed URI shortening service which provides
indissoluble URI shortening service.
Generally, shorten URIs are depending one service and if the service
end, all of them will be unavailable.

Each nodes of foomn have 'region' and generate own shorten URIs for each
regions.
Duplicated URI never generated between different regions.

Mapping file for registered URI and shorten URI should be downloaded
with it's checksum at all times.
When your server ends, you should entrust the mapping file to another
node and redirect requests to it.

Of cause you can't entrust it to a node which has same region you've used.

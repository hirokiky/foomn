===========
Shorten key
===========

overview
========

Way to generate shorten key

* The URLs managed by some of sequence value
* It is constructed by characters 0-9a-zA-Z (62 characters)
* The length of shorten key will increase infinitely
* A shorter URLs is used ahead
* The first character is used as region code

The structure of a shorten URL will be like this::

   Names of each parts

                  region code (One character)
                  |
                  |  mapping code
                  |  |
                  |<-+->
    http://foo.mn/0AcBEu
                  <--+->
                     |
           shorten key

    <-- shorten url -->


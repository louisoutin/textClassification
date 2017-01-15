#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rstr_max import *
import sys

#str1 = "a"*2000
#str1 = open('/home/rbrixtel/SVN/py-rstr-max/002.art','r').read()*2
#str1_unicode = unicode(str1,'utf-8','replace')
#a = str1_unicode.split(" ")
def test():
 for i in xrange(10) :
  rstr = Rstr_max()
  for m in a[:100] :
    rstr.add_str(m)
  rstr.add_str(str1_unicode)
  rstr.add_str(str1_unicode[::-1])

  r = rstr.go()
  for (offset_end, nb), (l, start_plage) in r.iteritems():
    ss = rstr.global_suffix[offset_end-l:offset_end]

#  id_chaine = rstr.idxString[offset_end-1]
#  s = rstr.array_str[id_chaine]

    for o in xrange(start_plage, start_plage + nb) :
      offset_global = rstr.res[o]
      offset = rstr.idxPos[offset_global]
      id_str = rstr.idxString[offset_global]
      sss = rstr.array_str[id_str][offset:offset+l]

str1 = "tititoto"
str1 = "MISSISSIPPI"
# str1 = open('carafe','r').read()
str1 = "Sur la table d’un bouge noir où l’on va boire du vin rouge. "
str1_unicode = unicode(str1,'utf-8','replace')
print(str1_unicode)

rstr = Rstr_max()
rstr.add_str(str1_unicode) #str1
r = rstr.go()
liste = []
for (offset_end, nb), (l, start_plage) in r.iteritems():
  ss = rstr.global_suffix[offset_end-l:offset_end]
  id_chaine = rstr.idxString[offset_end-1]
  s = rstr.array_str[id_chaine]
  print '[%s] %d'%(ss.encode('utf-8'), nb)
  for o in range(start_plage, start_plage + nb) :
    offset_global = rstr.res[o]
    offset = rstr.idxPos[offset_global]
    id_str = rstr.idxString[offset_global]
    print '   (%i, %i)'%(offset, id_str)
  t = (len(ss),ss)
  liste.append(t)
a = sorted(liste,reverse=True)
for l,s in a[:30]:
  print l,s

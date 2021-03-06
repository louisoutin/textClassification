#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('./rstr_max')
from rstr_max.rstr_max import *

def exploit_rstr(r, rstr, dic_occur, options):
  l_str = []
  liiste = [" " for x in xrange(0,len(dic_occur))]
  #print liiste
  cpt_ss = 0
  for (offset_end, nb), (l, start_plage) in r.iteritems():
    ss = rstr.global_suffix[offset_end-l:offset_end]
    if len(ss)<options['minlen'] or len(ss)>options['maxlen']:
      continue
    cpt_ss+=1
    set_occur = set()
    for o in xrange(start_plage, start_plage+nb) :
      id_str = rstr.idxString[rstr.res[o]]
      dic_occur[id_str][cpt_ss]=dic_occur[id_str].setdefault(cpt_ss,0)+1
      set_occur.add(id_str)
    if len(set_occur)>=options['minsup'] and len(set_occur)<=options['maxsup'] :
      occurences = [[x,dic_occur[x][cpt_ss]] for x in set_occur]
      #print ss
      #print occurences
      for x in occurences:

          ss = ss.replace(" ", "SPACE")
          ss = ss.replace("'", "APPOS")
          ss = ss.replace(";", "DOTCOM")
          ss = ss.replace(".", "DOT")
          ss = ss.replace(",", "COMMA")
          liiste[x[0]]+= (ss+" ")*x[1]
      sortie = [ss, ["%s (%s)"%(x,y) for x,y in occurences]]
      l_str.append(sortie)

  return liiste

def get_motifs(lignes_texte,options = { 'minsup':3,
            'maxsup':7,
            'minlen':2,
            'maxlen':10}):
  rstr = Rstr_max()
  for ligne in lignes_texte:
    rstr.add_str(ligne.body)
  dic_occur= {x:{} for x in xrange(0,len(lignes_texte))}
  r=rstr.go()
  l_motifs = exploit_rstr(r, rstr, dic_occur, options)
  return l_motifs

if __name__=="__main__":
    from textTypes.textDelfi import *

    liste_motifs = get_motifs([TextDelfi("1", "HATTIVATTAATTI"),TextDelfi("1", "ATII ATTA"), TextDelfi("1", "AT")])
    # get_motifs prend comme paramètre une liste de chaines et des options
    # chaque chaine étant une ligne généralement
    # on peut ajouter un dictionnaire d'options en donnant des valeurs de support (effectif) minimal et maximal (minsup et maxsup) de même pour la longueur en caractères du motif (minlen et maxlen)
    #Sinon, les valeurs par défaut sont utilisées: options = { 'minsup':2, 'maxsup':10, 'minlen':1, 'maxlen':10}
    # la fonction retourne une liste de paires : motif, liste de paires chaine (effectif)
    #chaine1 = open(sys.argv[1]).read()
    #chaine2 = open(sys.argv[2]).read()
    #liste_motifs = get_motifs([chaine1,chaine2])

    print(liste_motifs)


   # ["A A A A I I T T T T T T AT AT AT AT ","A A A ","A "]
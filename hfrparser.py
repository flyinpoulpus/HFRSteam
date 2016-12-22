import os
import sys

import domparser
import stringutils
import web


def get_post():
    HFR_URL      = 'http://forum.hardware.fr/hfr/JeuxVideo/Achat-Ventes/gratuit-origin-download-sujet_171605_1.htm#t8945000'

    status, html = web.get_utf8_web_page(HFR_URL)
    document     = domparser.load_html(html)
    post         = domparser.get_element(document, 'div', id = 'para8945000')

    return str(post)


def clean_tags(games):
    striked       = False
    BEGIN_STRIKED = '<strike><span style=color:#FF0000>'
    END_STRIKED   = '</span></strike>'
    for index, game in enumerate(games):
        game = game.strip()
        if (game.startswith(BEGIN_STRIKED)):
            if (not game.endswith(END_STRIKED)):
                striked = True
                game    += END_STRIKED
        else:
            if (striked):
                if (game.endswith(END_STRIKED)):
                    striked = False
                else:
                    game    += END_STRIKED
                game = BEGIN_STRIKED + game

        games[index] = game

    return


def get_list(post):
    START = '<strong>Clefs  <img alt="[:icon4]" src="http://forum-images.hardware.fr/images/perso/icon4.gif" title="[:icon4]"/> Steam <img alt="[:icon4]" src="http://forum-images.hardware.fr/images/perso/icon4.gif" title="[:icon4]"/> :</strong> <br/><strong> <br/>'
    END   = '<strong>Clefs  <img alt="[:icon4]" src="http://forum-images.hardware.fr/images/perso/icon4.gif" title="[:icon4]"/> Desura <img alt="[:icon4]" src="http://forum-images.hardware.fr/images/perso/icon4.gif" title="[:icon4]"/> :</strong>'

    subpost = stringutils.substringafter(post, START)
    subpost = stringutils.substringbefore(subpost, END)

    cleansubpost = subpost.replace('<br/>', '\r\n')
    cleansubpost = cleansubpost.replace('&amp;', "&")
    cleansubpost = cleansubpost.replace('"', '')
    cleansubpost = cleansubpost.replace('--', '')
    cleansubpost = cleansubpost.strip()

    # the separator is \x1c
    games = cleansubpost.splitlines()
    games = list(filter(None, games))
    clean_tags(games)
    return games


def parse_hfr():
    post  = get_post()
    games = get_list(post)
    #list(map(print, games))
    return games


if __name__ == '__main__':
    parse_hfr()

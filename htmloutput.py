import datetime
import math
import os


_indentcount = 4
_INDENTSTEP = 4


def writeline(line):
    newline = ''
    for i in range(0, _INDENTSTEP * _indentcount):
        newline += ' '
    newline += line + os.linesep
    return newline


def increase_indent_count():
    global _indentcount
    _indentcount += 1


def decrease_indent_count():
    global _indentcount
    _indentcount -= 1


def get_data(games):
    reviewMapping = dict()
    reviewMapping[10] = 'Overwhelmingly Positive'
    reviewMapping[9]  = 'Very Positive'
    reviewMapping[8]  = 'Positive'
    reviewMapping[7]  = 'Mostly Positive'
    reviewMapping[6]  = 'Mixed'
    reviewMapping[5]  = 'Mostly Negative'
    reviewMapping[4]  = 'Negative'
    reviewMapping[3]  = 'Very Negative'
    reviewMapping[2]  = 'Overwhelmingly Negative'
    data = ''
    justifyFormat = '<div style=\\"white-space: normal; text-align: justify; text-justify: inter-word; line-height: 150%\\">{0}</div>'

    for gameName in sorted(games):
        game = games[gameName]
        if (not game.hfr.is_available):
            continue

        data += writeline('var row = {')
        increase_indent_count()
        data += writeline('name: "{0}",'.format(gameName))
        if (game.store.link):
            if(game.store.image):
                data += writeline('nameFormat: "<a href=\\"{0}\\"><b>{1}</b><img src=\\"{2}\\" width=\\"100%\\"/></a>",'
                                  .format(game.store.link, justifyFormat, game.store.image))
            else:
                data += writeline('nameFormat: "<a href=\\"{0}\\"><b>{1}</b></a>",'
                                  .format(game.store.link, justifyFormat))
        else:
            data += writeline('nameFormat: "<b>{0}</b>",'.format(justifyFormat))
        if(game.store.description):
            data += writeline('description: "{0}",'.format(
                game.store.description.replace(os.linesep, '<br/>')))
        if (game.store.category):
            data += writeline('category: "{0}",'.format(game.store.category.name))
        if (len(game.store.os) > 0):
            data += writeline('os: "{0}",'.format(', '.join(game.store.os).replace('OS X', 'OS')))
        if (game.store.price != None):
            data += writeline('price: {0},'.format(str(game.store.price)))
            if (game.store.price == 0):
                data += writeline('priceFormat: "{0}",'
                                  .format(justifyFormat.replace('{0}', 'Free')))
            elif (game.store.price < 0):
                data += writeline('priceFormat: "{0}",'
                                  .format(justifyFormat.replace('{0}', 'N/A')))
            else:
                data += writeline('priceFormat: "{0}",'.
                                  format(justifyFormat.replace('{0}', '${0}')))

        if (len(game.store.genres) > 0):
            data += writeline('genres: "{0}",'.format(', '.join(game.store.genres)))
        if (game.store.release_date):
            date, errors = game.store.release_date
            # if errors has more than whitespace or empty strings
            errors = tuple(filter(lambda x: x.strip(), errors))
            if (len(errors)):
                fmt = '%Y'
            else:
                fmt = '%Y-%m-%d'
            data += writeline('date: "{0}",'.format(date.strftime(fmt).replace('-', '&#8209;')))
        if (game.store.avg_review) and (game.store.avg_review in reviewMapping):
            avg_review_text = reviewMapping[game.store.avg_review]
            MIN_POW         = 6
            avg_review_p    = math.pow(10, MIN_POW) * game.store.avg_review
            # if we have average negative reviews, we reduce the average review's power per review
            if (game.store.avg_review < 6):
                avg_review = str(avg_review_p - game.store.cnt_review)
            # if we have average positive reviews, we increment the average review's power per review
            else:
                avg_review = str(avg_review_p + game.store.cnt_review)
            if (game.store.avg_review < 10):
                avg_review = '0{0}'.format(avg_review)
            data += writeline('review: "{0} {1}",'.
                              format(avg_review, avg_review_text))
            data += writeline('reviewFormat: "{0}",'.
                              format(justifyFormat.replace('{0}',
                                                           '{0} ({1})'.
                                                           format(avg_review_text,
                                                                  game.store.cnt_review))))
        else:
            if (game.store.avg_review):
                print('The average review {0} for game {1} is not in the mapping!'.
                      format(game.store.avg_review, gameName))

        if (game.hfr.requirements):
            if (game.hfr.requirements.lower() in ['standard', 'nouveauté']):
                stars = '*'
            else:
                stars = '**'
            
            data += writeline('requirements: "{0}<sup><b>{1}</b></sup>",'.format(game.hfr.requirements, stars))

        if (len(game.store.tags) > 0):
            data += writeline('tags: "{0}",'.format(', '.join(game.store.tags)))

        if (len(game.store.details) > 0):
            data += writeline('details: "{0}",'.format(', '.join(game.store.details)))

        if (game.hfr.gift_date):
            data += writeline('giftdate: "{0}",'.format(game.hfr.gift_date.strftime("%Y-%m-%d")))

        decrease_indent_count()
        data += writeline('};')
        data += writeline('rows.push(row);')

    return data


def output_to_html(games, file):
    TEMPLATE_FILE   = 'templates/index.html.t'
    TEXT_TO_REPLACE = '$TEMPLATE$'
    DATE_TO_REPLACE = '$DATE$'

    f            = open(TEMPLATE_FILE, 'r')
    templatetext = f.read()
    f.close()

    data = get_data(games)

    text = templatetext.replace(TEXT_TO_REPLACE, data)

    text = text.replace('$DATE$', datetime.date.today().isoformat())

    # These 2 chars proc a unicode encode error on Windows so we replace them
    text = text.replace('\x97', '')
    text = text.replace('\u2032', '\'')

    f = open(file, 'w')
    f.write(text)
    f.close()

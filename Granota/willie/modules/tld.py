# -*- coding:utf-8 -*-

from willie import web
from willie.module import commands, example
import re

uri = 'https://en.wikipedia.org/wiki/List_of_Internet_top-level_domains'
r_tag = re.compile(r'<(?!!)[^>]+>')


@commands('tld')
@example('.tld ru')
def gettld(bot, trigger):
    """Show information about the given Top Level Domain."""
    page = web.get(uri)
    search = r'(?i)<td><a href="\S+" title="\S+">\.{0}</a></td>\n(<td><a href=".*</a></td>\n)?<td>([A-Za-z0-9].*?)</td>\n<td>(.*)</td>\n<td[^>]*>(.*?)</td>\n<td[^>]*>(.*?)</td>\n'
    search = search.format(trigger.group(2))
    re_country = re.compile(search)
    matches = re_country.findall(page)
    if not matches:
        search = r'(?i)<td><a href="\S+" title="(\S+)">\.{0}</a></td>\n<td><a href=".*">(.*)</a></td>\n<td>([A-Za-z0-9].*?)</td>\n<td[^>]*>(.*?)</td>\n<td[^>]*>(.*?)</td>\n'
        search = search.format(trigger.group(2))
        re_country = re.compile(search)
        matches = re_country.findall(page)
    if matches:
        matches = list(matches[0])
        i = 0
        while i < len(matches):
            matches[i] = r_tag.sub("", matches[i])
            i += 1
        desc = matches[2]
        if len(desc) > 400:
            desc = desc[:400] + "..."
        reply = "%s -- %s. IDN: %s, DNSSEC: %s" % (matches[1], desc,
                matches[3], matches[4])
        bot.reply(reply)
    else:
        search = r'<td><a href="\S+" title="\S+">.{0}</a></td>\n<td><span class="flagicon"><img.*?\">(.*?)</a></td>\n<td[^>]*>(.*?)</td>\n<td[^>]*>(.*?)</td>\n<td[^>]*>(.*?)</td>\n<td[^>]*>(.*?)</td>\n<td[^>]*>(.*?)</td>\n'
        search = search.format(unicode(trigger.group(2)))
        re_country = re.compile(search)
        matches = re_country.findall(page)
        if matches:
            matches = matches[0]
            dict_val = dict()
            dict_val["country"], dict_val["expl"], dict_val["notes"], dict_val["idn"], dict_val["dnssec"], dict_val["sld"] = matches
            for key in dict_val:
                if dict_val[key] == "&#160;":
                    dict_val[key] = "N/A"
                dict_val[key] = r_tag.sub('', dict_val[key])
            if len(dict_val["notes"]) > 400:
                dict_val["notes"] = dict_val["notes"][:400] + "..."
            reply = "%s (%s, %s). IDN: %s, DNSSEC: %s, SLD: %s" % (dict_val["country"], dict_val["expl"], dict_val["notes"], dict_val["idn"], dict_val["dnssec"], dict_val["sld"])
        else:
            if bot.config.lang == 'ca':
                reply = "Cap resultat per TLD: {0}".format(unicode(trigger.group(2)))
            elif bot.config.lang == 'es':
                reply = u"Ningún resultado por TLD: {0}".format(unicode(trigger.group(2)))
            else:
                reply = "No results for TLD: {0}".format(unicode(trigger.group(2)))
        bot.reply(reply)

# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/PezDispenser
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.1
# Prototype version, low priority


# Icons can be any image, but must be placed in the media folder
# and renamed to this format: "_tag_TAGNAME.ico" where
# TAGNAME is the tag and :(colon) are replaced by _(underscore).
# Also make sure images are large enough to allow for zooming.

CSS = """
<style>
img.pez_icon {
  cursor:pointer;
  height:1.2em;
}
</style>
"""



from aqt import mw
from anki.template import Template
from anki.hooks import wrap
import re, os

from anki import version
ANKI21=version.startswith("2.1.")


def render_sections(self, template, context, _old):
    arr=[]; kbd=[];
    deck=context['Deck']
    for t in context['Tags'].split():
        img="_tag_%s.ico"%t.replace(':','_')
        path=os.path.join(mw.pm.profileFolder(),"collection.media",img)
        img=img if os.path.exists(path) else None
        html,imgType=getHtmlTags(img,t,deck)
        if imgType:
            arr.append(html)
        else:
            kbd.append(html)
    template=re.sub("{{Tags}}", ''.join(arr+kbd), template)
    template+=CSS
    return _old(self, template, context)

Template.render_sections = wrap(Template.render_sections, render_sections, 'around')



#javascript code is handled by addon:clickable_tags
def getHtmlTags(img,t,d):
    if ANKI21:
        if img:
            html="""
<img class="pez_icon" src="%s" ondblclick='ct_dblclick("%s","%s")' 
onclick='ct_click("%s")' 
title="%s" />"""%(img,t,d,t,t)
        else:
            html="""
<kbd ondblclick='ct_dblclick("%s","%s")' 
onclick='ct_click("%s")'>%s</kbd>"""%(t,d,t,t)

    else:
        if img:
            html="""
<img class="pez_icon" src="%s" 
ondblclick='dblclick_func("_tagdblclick_%s_tagdblclick_%s")' 
onclick='click_func("tagclick_%s")' 
title="%s" />"""%(img,d,t,t,t)
        else:
            html="""
<kbd ondblclick='dblclick_func("_tagdblclick_%s_tagdblclick_%s")' 
onclick='click_func("tagclick_%s")'>%s</kbd>"""%(d,t,t,t)

    return html,img


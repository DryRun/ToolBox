from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import logging

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.fed_enablemask_start = False
        self.start = False
        self.stop = False
        self.feds = []

    def handle_starttag(self, tag, attrs):
        try:
            logging.debug("Start tag:" + tag)
            if self.fed_enablemask_start and tag=="textarea":
                self.start = True
            for attr in attrs:
                logging.debug("     attr: " + attr)
        except Exception as exc:
            logging.debug(exc.args)

    def handle_endtag(self, tag):
        try:
            logging.debug("End tag  :" + tag)
            if self.start and not self.stop and tag=="textarea":
                self.stop=True
        except Exception as exc:
            logging.debug(exc.args)

    def handle_data(self, data):
        logging.debug("Data     :"+data)
        if "FED_ENABLE_MASK" in data:
            self.fed_enablemask_start = True
        if self.start and not self.stop:
            self.feds += data

    def handle_comment(self, data):
        logging.debug("Comment  :"+data)

    def handle_entityref(self, name):
        try:
            c = unichr(name2codepoint[name])
            logging.debug("Named ent:"+c)
        except Exception as exc:
            logging.debug(exc.args)

    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        logging.debug("Num ent  :"+c)

    def handle_decl(self, data):
        logging.debug("Decl     :"+data)

    def unknown_decl(self, data):
        logging.debug("Unknown :"+data)

parser = MyHTMLParser()

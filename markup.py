from handlers import *
from rules import *
from util import *

import sys, re

class Parser():
    def __init__(self, handler):
        self.handler = handler
        self.rules = []
        self.filters = []
    def addRule(self, rule):
        self.rules.append(rule)
    def addFilter(self, pattern, name):
        def filter(block, handler):
            return re.sub(pattern, handler.sub(name), block)
        self.filters.append(filter)
    def parse(self, file):
        self.handler.start('document')
        for block in blocks(file):
            for filter in self.filters:
                block = filter(block, self.handler)
            for rule in self.rules:
                if rule.condition(block): 
                    last = rule.action(block, self.handler)
                    if last: break
        self.handler.end('document')
         
class BasicParser(Parser):
    def __init__(self, handler):
        Parser.__init__(self, handler)
        self.addRule(ListRule())
        self.addRule(ListitemRule())
        self.addRule(TitleRule())
        self.addRule(HeadingRule())
        self.addRule(ParagraphRule())
    
        self.addFilter(r'\*(.+?)\*', 'emphasis')
        self.addFilter(r'(http://[\.a-zA-Z]+)','url')
        self.addFilter(r'[\.a-zA-Z]+@[a-zA-Z]+','mail')
                            
handler = HTMLRenderer()
#print(re.sub(r'\*(.+?)\*', handler.sub('emphasis'), 'hello *liyaozong*'))
parser = BasicParser(handler)


html_file = open("./output.html",'w+')
sys.stdout = html_file

f = open("./input_test.txt", 'r')
parser.parse(f)

f.close()
html_file.close()


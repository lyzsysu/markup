#encoding:utf-8

# 基类定义无须小括号
class Rule:
    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True

class HeadingRule(Rule):
    type = 'heading'
    # 不包含\n，也就是说不是最后一个block；长度小于70；不以冒号结尾
    def condition(self, block):
        return not '\n' in block and len(block) <= 70 and not block[-1] == ';'

class TitleRule(Rule):
    type = 'title'
    first = True		 
    def condition(self, block):
        # 善用not使代码更简洁
        if not self.first: return False
        self.first = False
        return HeadingRule.condition(self, block)
    
class ListRule(Rule):
    type = 'list'
    liststart = True
    def condition(self, block):
        return True
    def action(self, block, handler):
        if self.liststart and ListitemRule.condition(self, block):
            self.liststart = False
            handler.start(self.type)
        elif not self.liststart and not ListitemRule.condition(self, block):
            self.liststart = True
            handler.end(self.type)
        return False
	        

class ListitemRule(Rule):
    type = 'listitem'
    # 函数次序最好有先后顺序
    def condition(self, block):
        return block[0] == '-'
    def action(self,block, handler):
        handler.start(self.type)
        handler.feed(block[1:])
        handler.end(self.type)
        return True

class ParagraphRule(Rule):
    type = 'paragraph'
    def condition(self, block):
        return True

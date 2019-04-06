#encoding:utf-8

class Handler:
    def callback(self, prefix, name, *args):
        method = getattr(self, prefix+name, None)
        if callable(method):
            return method(*args)
    def start(self, name):
        self.callback('start_', name)
    def end(self, name):
        self.callback('end_', name)
    def sub(self, name):
        # 定义一个函数来返回
        def substitution(match):
            # 调用callback函数调用其他sub函数，如果结果为空，使用match返回，
            # 即没有找到匹配项
            result = self.callback('sub_', name, match)
            if result is None: result = match.group(0)
            return result
        # 返回函数无需小括号
        return substitution

class HTMLRenderer(Handler):
    def start_document(self):
        print('<html><title>MyTitle</title><body>')
    def end_document(self):
        print('</body></html>')
    def start_title(self):
        print('<h1>')
    def end_title(self):
        print('</h1>')
    def start_list(self):
        print('<ul>')
    def end_list(self):
        print('</ul>')
    def start_listitem(self):
        print('<li>')
    def end_listitem(self):
        print('</li>')
    def start_paragraph(self):
        print('<p>')
    def end_paragraph(self):
        print('</p>')
    def sub_emphasis(self, match):
        return '<em>%s</em>' % match.group(1)
    def sub_url(self, match):
        return '<a href="%s">%s</a>' % (match.group(1), match.group(1))
    def sub_mail(self, match):
        return '<a href="mailto:%s">%s</a>' % (match.group(1), match.group(1))
    def feed(self, block):
        print(block)

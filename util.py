#encoding:utf-8

def lines(file):
    for line in file: yield line
    yield "\n"

def blocks(file):
    #初始化空列表
    block = []
    for line in lines(file):
        #如果行非空。
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip()
            block = []

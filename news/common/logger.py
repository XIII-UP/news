 # -*- coding: utf-8 -*- 
import logging
import os
import time
import logging.handlers


class Logger(logging.Logger):
    def __init__(self, filename=None):
        super(Logger, self).__init__(self)
        # 日志文件名
        if filename is None:
            realpath  = os.path.dirname(os.path.realpath(__file__)).replace("\\", '/') + "/log/"
            filename  = realpath + str(time.strftime("%Y-%m-%d", time.localtime())) + '.log'
        self.filename = filename

        # 创建一个handler，用于写入日志文件 (每天生成1个，保留30天的日志)
        fh = logging.handlers.TimedRotatingFileHandler(self.filename, 'D', 1, 30)
        fh.suffix = "%Y%m%d-%H%M.log"
        fh.setLevel(logging.DEBUG) 

        # 再创建一个handler，用于输出到控制台 
        ch = logging.StreamHandler() 
        ch.setLevel(logging.DEBUG) 

        # 定义handler的输出格式 
        formatter = logging.Formatter('[%(asctime)s] %(filename)s[Line:%(lineno)d] [%(levelname)s] %(message)s')
        fh.setFormatter(formatter) 
        ch.setFormatter(formatter) 

        # 给logger添加handler 
        self.addHandler(fh) 
        self.addHandler(ch)



if __name__ == '__main__':
    pass
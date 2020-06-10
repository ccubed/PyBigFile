import io
import json
from multiprocessing import Pool
from datetime import timedelta
import time


def write_file(idnum, text):
    with open('/home/hestia/Entries/entry{}.json'.format(idnum), 'w') as output:
        output.write(text)


class BigOlFiles:
    def __init__(self, src="../yasp.json", pool=None):
        self.src = src
        self.pool = pool
        self.entry = 0

    def test_read(self):
        if self.pool is None:
            return False
        stream = bytearray(1024)
        tempstr = ""
        with open(self.src, 'rb', buffering=0) as data:
            while data.readinto(stream):
                if ',\n'.encode() in stream:
                    temp = stream.decode('utf-8', 'ignore')
                    pos = temp.find(',\n')
                    self.pool.apply(write_file, (self.entry, tempstr + temp[:pos-2]))
                    self.entry += 1
                    tempstr = temp[pos+2:]
                else:
                    tempstr += stream.decode('utf-8', 'ignore')

if __name__ == '__main__':
    with Pool() as p:
        react = BigOlFiles(pool=p)
        start = time.time()
        react.test_read()
        end = time.time() - start
        print(str(timedelta(seconds=end)))

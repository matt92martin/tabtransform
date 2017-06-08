#!/usr/bin/env python

import sys, os, traceback, argparse, textwrap
import logging as log
from csv import DictReader
# from guppy import hpy

class Row(object):
    """
    Row Object, placeholder
    """

class Main:

    def __init__(self, opts):
        self.opts = opts
        self.reader = self.load_file()
        self.reader2 = self.load_file()
        self.fieldnames = self.reader.fieldnames
        self.log = log.basicConfig(format="%(message)s", level=log.INFO)

        if not os.path.isfile('tabtrans.py'):
            log.info("Define a tabtrans.py")
            sys.exit(0)


    def load_file(self):
        return DictReader(open(self.opts.file, 'rb'), delimiter="\t")

    def gen_line(self):
        code = compile(open('tabtrans.py').read(), 'tabtrans.py', 'exec')

        extra = {}
        fieldnames = set(self.fieldnames)
        seenvariables = set()
        for line in self.reader:

            d = line.copy()
            for k,v in d.iteritems():
                if v.isdigit():
                    d[k] = int(v)

            d['row'] = Row()
            exec(code, d)
            extra[self.reader.line_num] = vars( d['row'] )
            seenvariables.update( vars( d['row'] ).keys() )

        self.fieldnames += list(seenvariables - fieldnames)

        yield '\t'.join(self.fieldnames)
        for line in self.reader2:
            line.update(extra[self.reader.line_num])
            yield '\t'.join([line.get(var, '') for var in self.fieldnames])


    def main(self):
        for line in self.gen_line():
            print line


def options():
    parser = argparse.ArgumentParser(
        description=textwrap.dedent( '''
            Command:
            tabtransform <file>
        ''' ),
        add_help=False,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument( '--help', help=argparse.SUPPRESS, action='help' )
    parser.add_argument( 'file', help='File to parse', type=str )

    return parser.parse_args( )




if __name__ == '__main__':
    try:
        main = Main( options() )
        # h = hpy()
        # print h.heap()
        sys.exit( main.main() )
    except KeyboardInterrupt, e:
        raise e
    except SystemExit, e:
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)
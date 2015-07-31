# coding: utf-8
from string import Template

PRETTY_INDENT = 4
BASE_INDENT_SPACE = ' '

def _quote( s ):
    return ''.join( [ '"', s, '"' ] )

class ConfBase( object ):
    def __init__( self ):
        super( ConfBase, self ).__init__()

def _dump( d, pretty=False, indent=0 ):
    if isinstance( d, int ) or isinstance( d, float ) or isinstance( d, bool ):
        return d

    elif isinstance( d, basestring ): # str and unicode
        return _quote( d )

    elif isinstance( d, list ):
        arr = []
        for ele in d:
            arr.append( _dump( ele ) )

        t = Template( '[ $arr ]' )
        return t.substitute( arr=', '.join( arr ) )

    elif isinstance( d, dict ):
        p = ' '
        indent_spaces = ''
        if pretty:
            p = '\n'
            indent_spaces = BASE_INDENT_SPACE * indent       

        res = '{' + p
        for k, v in d.items():
            t = Template( '$indent$key => $val$p' )

            key_indent_spaces = BASE_INDENT_SPACE * ( indent + PRETTY_INDENT )
            val_indent = indent + PRETTY_INDENT * 2
            res += t.substitute( indent=key_indent_spaces, key=k, val=_dump( v, pretty, indent=val_indent ), p=p )

        res += indent_spaces + '}' + p

        return res


class Plugin( ConfBase ):
    def __init__( self, name, **kwargs ):
        super( Plugin, self ).__init__()
        self.name = name
        self.settings = kwargs

    def __str__( self ):
        return self.name

    def dumps( self, pretty=False, indent=0 ):
        p = ' '
        indent_spaces = ''
        if pretty:
            p = '\n'
            indent_spaces = BASE_INDENT_SPACE * indent

        res = indent_spaces + self.name + ' {' + p
        for k, v in self.settings.items():
            sub_indent = indent + PRETTY_INDENT
            v_dumped = _dump( v, pretty, indent=sub_indent )
            res += BASE_INDENT_SPACE * sub_indent + Template( '$key => $val' ).substitute( key=k, val=v_dumped ) + p

        res += indent_spaces + '}' + p

        return res            

class Comment( ConfBase ):
    def __init__( self, c ):
        super( Comment, self ).__init__()
        self.c = c

    def dumps( self, pretty=False, indent=0 ):
        p = ' '
        indent_spaces = ''
        if pretty:
            p = '\n'
            indent_spaces = BASE_INDENT_SPACE * indent

        t = Template( '$indent#$comment$p' )
        return t.substitute( indent=indent_spaces, comment=self.c, p=p)

# 可以考虑合并If, ElseIf, Else为一个class
# __init__(self, if_expr_blocks, elseif_expr_blocks, else_expr_blocks )

class If( ConfBase ):
    def __init__( self, expression, *blocks ):
        super( If, self ).__init__()
        self.expression = expression
        self.child_blocks = blocks

    def dumps( self, pretty=False, indent=0 ):
        p = ' '
        indent_spaces = ''
        if pretty:
            p = '\n'
            indent_spaces = BASE_INDENT_SPACE * indent

        res = indent_spaces + 'if ' + self.expression + ' {' + p
        for blk in self.child_blocks:
            res += blk.dumps( pretty, indent=indent + PRETTY_INDENT )

        res += indent_spaces + '}' + p

        return res

class ElseIf( ConfBase ):
    def __init__( self, expression, *blocks ):
        super( ElseIf, self ).__init__()
        self.expression = expression
        self.child_blocks = blocks

    def dumps( self, pretty=False, indent=0 ):
        p = ' '
        indent_spaces = ''
        if pretty:
            p = '\n'
            indent_spaces = BASE_INDENT_SPACE * indent

        res = indent_spaces + 'else if ' + self.expression + ' {' + p
        for blk in self.child_blocks:
            res += blk.dumps( pretty, indent=indent + PRETTY_INDENT )

        res += indent_spaces + '}' + p

        return res

class Else( ConfBase ):
    def __init__( self, *blocks ):
        super( Else, self ).__init__()
        self.child_blocks = blocks

    def dumps( self, pretty=False, indent=0 ):
        p = ' '
        indent_spaces = ''
        if pretty:
            p = '\n'
            indent_spaces = BASE_INDENT_SPACE * indent

        res = indent_spaces + 'else {' + p
        for blk in self.child_blocks:
            res += blk.dumps( pretty, indent=indent + PRETTY_INDENT )

        res += indent_spaces + '}' + p

        return res


class LogstashConf( object ):
    """
    配置的顺序很重要
    """

    def __init__( self ):
        self.conf = { 'input': [], 'filter': [], 'output': [] }

    def input( self, *blocks ):
        self.conf[ 'input' ].extend( blocks )

    def filter( self, *blocks ):
        self.conf[ 'filter' ].extend( blocks )

    def output( self, *blocks ):
        self.conf[ 'output' ].extend( blocks )

    def dumps_dict( self, pretty=True ):
        return self.conf

    def dumps( self, pretty=False ):
        p = ' ' if pretty is False else '\n'

        res = 'input {' + p
        res += self._dumps( self.conf[ 'input' ], pretty )
        res += '}' + p
        res += 'filter {' + p
        res += self._dumps( self.conf[ 'filter' ], pretty )
        res += '}' + p
        res += 'output {' + p
        res += self._dumps( self.conf[ 'output' ], pretty )
        res += '}'
        return res

    def _dumps( self, d, pretty=False, indent=PRETTY_INDENT ):
        p = ' ' if pretty is False else '\n'

        res = ''
        for blk in d:
            res += blk.dumps( pretty, indent=indent )

        return res

"""
# Let me show you a example, Run the following command:
$ python logstash_conf_api.py

# Then you get this output:
 
input {
    #This is a test comment
    kafka{
        zk_connect => "<zk_connect>"
        group_id => "<group_id>"
        codec => "plain"
        topic_id => "<topic_id>"
    }
}
filter {
    ruby{
        code => "puts event"
    }
    grok{
        match => {
            "message" => [ "%{NUMBER:http_status} %{WORD:method}", "%{DATA:access_log}" ]
        }

    }
}
output {
    if [type]== "type_1" {
        elasticsearch{
                index => "test.yingju1-%{type}-%{+YYYY.MM.dd}"
                host => [ "1002.es.dip.sina.com.cn" ]
                protocol => "http"
                workers => 2
                flush_size => 20000
        }
    }
    else if [type]== "type_2" {
        elasticsearch{
                index => "test.yingju1-%{type}-%{+YYYY.MM.dd}"
                host => [ "1002.es.dip.sina.com.cn" ]
                protocol => "http"
                workers => 2
                flush_size => 20000
        }
    }
    else {
        elasticsearch{
                index => "test.yingju1-%{type}-%{+YYYY.MM.dd}"
                host => [ "1002.es.dip.sina.com.cn" ]
                protocol => "http"
                workers => 2
                flush_size => 20000
        }
    }
}
"""


if __name__ == '__main__':
    conf = LogstashConf()

    conf.input( Comment( 'This is a test comment' ) )

    kafka = { 'topic_id': '<topic_id>', 'group_id': '<group_id>', 'zk_connect': '<zk_connect>', 'codec': 'plain' }
    conf.input( Plugin( 'kafka', **kafka ) )

    ruby = { 'code': 'puts event' }
    conf.filter( Plugin( 'ruby', **ruby ) )

    # use _quote() if specific string is a field reference, such as _quote( 'message' )
    grok = { 'match': { _quote( 'message' ): [ '%{NUMBER:http_status} %{WORD:method}', '%{DATA:access_log}' ] } }
    conf.filter( Plugin( 'grok', **grok ) )

    es = { 'host': [ '1002.es.dip.sina.com.cn' ], 'index': 'test.yingju1-%{type}-%{+YYYY.MM.dd}', 'protocol': 'http', 'flush_size': 20000, 'workers': 2 }
    es_plugin = Plugin( 'elasticsearch', **es )
    # you can do this
    # conf.output( es_plugin )

    # or using if block
    if_blk = If( '[type]== "type_1"', es_plugin )
    elseif_blk = ElseIf( '[type]== "type_2"', es_plugin )
    else_blk = Else( es_plugin )
    conf.output( if_blk, elseif_blk, else_blk )
    
    # print conf.dumps()
    print conf.dumps( pretty=True )

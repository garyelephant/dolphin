# coding:utf-8
from flask import Flask,request
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/index")
def index():
    return render_template( 'index.html' )

@app.route( "/parse_log", methods=[ 'POST' ] )
def parse_log():
    import json
    from pygrok import grok_match

    form = request.get_data()
    app.logger.warning( "form:%s", form )

    form = json.loads( form )

    grok_pat = build_grok_pattern( form[ 'log_format' ] )
    app.logger.warning( 'grok_pat:%s', grok_pat )
    
    logs = form[ 'log_examples' ].split( "\n" )
    
    pls = []
    for l in logs:
        pl = grok_match( l, grok_pat )
        pls.append( pl )
        app.logger.warning('pl:%s', json.dumps( pl, indent=4 ) )

    data = { 'parsed_logs': pls }

    ls_conf = build_logstash_conf( form[ 'log_format' ] )
    app.logger.warning( 'ls_conf:%s', ls_conf )

    return json.dumps( data )

def build_logstash_conf( log_format ):
    from logstash_conf_api import LogstashConf, Plugin, If, Else, _quote
    conf = LogstashConf()

    grok_pat = build_grok_pattern( log_format )
    grok = { 'match': { _quote( 'message' ): [ grok_pat ] } }
    conf.filter( Plugin( 'grok', **grok ) )

    # TODO refine log format definition

    # 类型转换 logstash-filter-mutate

    # string to json logstash-filter-josn

    # 时间戳: logstash-filter-date

    # geoip: logstash-filter-geoip2

#     if [tags] {
#         if ( "_grokparsefailure" not in [tags] ) and ( "_jsonparsefailure" not in [tags] ) {
#             mutate {
#                 remove_field => [ "message" ]
#             }
#         }
#     }
#     else {
#         mutate {
#             remove_field => [ "message" ]
#         }
#     }
    remove_message = Plugin( 'mutate', **{ 'remove_field': [ 'message' ] } )
    if_not_failure = If( '( "_grokparsefailure" not in [tags] ) and ( "_jsonparsefailure" not in [tags] )', remove_message )
    if_blk = If( '[tags]', if_not_failure )
    else_blk = Else( remove_message )
    conf.filter( if_blk, else_blk )

    return conf.dumps( pretty=True )

def build_grok_pattern( log_format ):
    from string import Template
    from grok_pat_config import GROK_PATTERN_CONF, CaseInsensitiveKey

    pat = ''
    for i in range( 1, len( log_format ) + 1 ):
        ele = log_format[ str( i ) ]
        if ele[ 'type' ] == 'field':
            t = Template( '%{$field_pat:$field_name}' )
            field_pat = GROK_PATTERN_CONF[ CaseInsensitiveKey( ele[ 'field_type' ] ) ]
            pat += t.substitute( field_pat=field_pat, field_name=ele[ 'name' ] )
        elif ele[ 'type' ] == 'placeholder':
            if ele[ 'name' ] == 'space':
                pat += ' '
            else:
                pat += ele[ 'name' ]
        else:
            app.logger.error( "unexpected log format element type(%s) in %s", str( ele[ 'type' ] ), json.dumps( ele ) )
            # TODO return exception in response

    pat += '$'

    return pat


@app.route("/sortable_example")
def sortable_example():
    return render_template( 'sortable_example.html' )

ep = 'select'
@app.route("/{endpoint}".format(endpoint=ep))
def flat_ui():
    return render_template( '{endpoint}.html'.format(endpoint=ep) )

if __name__ == "__main__":
    app.debug = True
    app.run( host='0.0.0.0' )
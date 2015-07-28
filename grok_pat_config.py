class CaseInsensitiveKey( object ):
    def __init__( self, key ):
        self.key = key
    def __hash__( self ):
        return hash( self.key.lower() )
    def __eq__( self, other ):
        return self.key.lower() == other.key.lower()
    def __str__( self ):
        return self.key

GROK_PATTERN_CONF = dict()
# Basic String
GROK_PATTERN_CONF[ CaseInsensitiveKey( 'String' ) ] = 'DATA' # DATA or NOTSPACE ?
GROK_PATTERN_CONF[ CaseInsensitiveKey( 'Quote String' ) ] = 'QS'
GROK_PATTERN_CONF[ CaseInsensitiveKey( 'UUID' ) ] = 'UUID'
GROK_PATTERN_CONF[ CaseInsensitiveKey( 'Log Level' ) ] = 'LOGLEVEL'
# Networking
GROK_PATTERN_CONF[ CaseInsensitiveKey( 'IP' ) ] = 'IP'
GROK_PATTERN_CONF[ CaseInsensitiveKey( 'Host/Domain' ) ] = 'HOST'
GROK_PATTERN_CONF[ CaseInsensitiveKey( 'Host:Port' ) ] = 'HOSTPORT'
GROK_PATTERN_CONF[ CaseInsensitiveKey( 'IP or Host/Domain' ) ] = 'IPORHOST'
# Path
GROK_PATTERN_CONF[ CaseInsensitiveKey( 'Full URL' ) ] = 'URI' # http://www.google.com?search=mj
GROK_PATTERN_CONF[ CaseInsensitiveKey( 'Url Path' ) ] = 'URIPATHPARAM'
GROK_PATTERN_CONF[ CaseInsensitiveKey( 'Unix Path' ) ] = 'UNIXPATH'
# Json
# GROK_PATTERN_CONF[ CaseInsensitiveKey( 'json' ) ] = 
# Number
GROK_PATTERN_CONF[ CaseInsensitiveKey( 'Number' ) ] = 'NUMBER' # Integer/Long OR Float/Double
GROK_PATTERN_CONF[ CaseInsensitiveKey( 'Integer/Long' ) ] = 'INT'
# GROK_PATTERN_CONF[ CaseInsensitiveKey( 'Float/Double' ) ] = 
# Date
GROK_PATTERN_CONF[ CaseInsensitiveKey( 'Year' ) ] = 'YEAR'
GROK_PATTERN_CONF[ CaseInsensitiveKey( 'Month' ) ] = 'MONTH'
GROK_PATTERN_CONF[ CaseInsensitiveKey( 'Month Number' ) ] = 'MONTHNUM'
GROK_PATTERN_CONF[ CaseInsensitiveKey( 'Day' ) ] = 'DAY'
GROK_PATTERN_CONF[ CaseInsensitiveKey( 'Hour' ) ] = 'HOUR'
GROK_PATTERN_CONF[ CaseInsensitiveKey( 'Minute' ) ] = 'MINUTE'
GROK_PATTERN_CONF[ CaseInsensitiveKey( 'Second' ) ] = 'SECOND'
# GROK_PATTERN_CONF[ CaseInsensitiveKey(  ) ] = 'TZ'
GROK_PATTERN_CONF[ CaseInsensitiveKey( 'ISO8601' ) ] = 'TIMESTAMP_ISO8601'
GROK_PATTERN_CONF[ CaseInsensitiveKey( 'HTTPDATE' ) ] = 'HTTPDATE'
# GROK_PATTERN_CONF[ CaseInsensitiveKey( 'custom' ) ] = # custom # TODO


# GROK_PATTERN_CONF = {
#     # Basic String
#     'String': 'DATA', # DATA or NOTSPACE ?
#     'Quote String': 'QS',
#     'UUID': 'UUID',
#     'Log Level': 'LOGLEVEL',
    
#     # Networking
#     'IP': 'IP',
#     'Host/Domain': 'HOST',
#     'Host:Port': 'HOSTPORT',
#     'IP or Host/Domain': 'IPORHOST',
    
#     # Path
#     'Full URL': 'URI', # http://www.google.com?search=mj
#     'Url Path': 'URIPATHPARAM',
#     'Unix Path': 'UNIXPATH',

#     # Json
#     'json': '', # TODO json regular expression
    
#     # Number
#     'Number': 'NUMBER', # Integer/Long OR Float/Double
#     'Integer/Long': 'INT',
#     'Float/Double': '',
    
#     # Date
#     'Year': 'YEAR',
#     'Month': 'MONTH',
#     'Month Number': 'MONTHNUM',
#     'Day': 'DAY',
#     'Hour': 'HOUR',
#     'Minute': 'MINUTE',
#     'Second': 'SECOND',
#     '': 'TZ',
#     'ISO8601': 'TIMESTAMP_ISO8601',
#     'HTTPDATE': 'HTTPDATE',
#     'custom': '', # custom # TODO
# }

import sys
import ply.lex as lex

class CTokenizer:


    # --------------------
    #  - - - Tokens - - -
    # --------------------

    tokens = (

        # Sets
        'STARTSET', 'ENDSET', 'EMPTYSET',

        # Urelements
        'INTEGER',

        # Identifiers
        'IDENTIFIER',

        # XML Tags
        'STARTTAG', 'ENDTAG',

        # Algorithmic Operators
        'SUCHTHAT', 'DENOTES', 
        'LPAREN', 'RPAREN', 'COMMA', 
        'COMMENT',

        # Set Operators
        'UNION', 'INTERSECTION', 'COMPLIMENT', 'POWERSET', 
        'CARDINALITY',

        # Urelemental Operators
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 
        'GT', 'LT', 'GE', 'LE',

        # Joint Operators
        'EQUALS'

    )


    # ----------------------------
    #  - - - Basic Patterns - - -
    # ----------------------------

    t_STARTSET     = r'\{'
    t_ENDSET       = r'\}'
    t_EMPTYSET     = r'ø|Ø'
    t_IDENTIFIER   = r'[\w_][\w\d_]*(\.[\w_][\w\d_]*)*'
    t_STARTTAG     = r'\['
    t_ENDTAG       = r'\]'
    t_SUCHTHAT     = r'\|'
    t_DENOTES      = r':'
    t_LPAREN       = r'\('
    t_RPAREN       = r'\)'
    t_COMMA        = r','
    t_COMMENT      = r'(\#{3})(([^\#])|(\#\#?[^\#]))*(\#{3})\#*'
    t_UNION        = r'∪'
    t_INTERSECTION = r'∩'
    t_COMPLIMENT   = r'\\'
    t_POWERSET     = r'ℙ'
    t_CARDINALITY  = r'\#'
    t_PLUS         = r'\+'
    t_MINUS        = r'-'
    t_TIMES        = r'\*'
    t_DIVIDE       = r'/'
    t_GT           = r'>'
    t_LT           = r'<'
    t_GE           = r'≥'
    t_LE           = r'≤'
    t_EQUALS       = r'=(=)?'
    t_ignore       = ' \t'


    # -----------------------------
    #  - - - Imbued Patterns - - -
    # -----------------------------

    def t_INTEGER( self, t ):
        r'\d+'
        t.value = int( t.value )


    # ----------------------
    #  - - - Specials - - -
    # ----------------------

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)


    # -------------------
    #  - - - Lexer - - -
    # -------------------

    # Constructor

    def __init__ ( self ):

        self.build()

    # Build the lexer

    def build(self,**kwargs):
        
        self.lex = lex.lex(module=self, **kwargs)

    # Tokenize files

    def tokenize( self, filename ):
        
        with open( filename, "r" ) as file:

            self.lex.input( str( file.read() ) )
            
            tokens = []
            while True:
                tok = self.lex.token()
                if not tok:
                    break
                tokens.append( tok )

            return tokens


# -------------------
#  - - - Main - - -
# -------------------

def main( ):

    if( len( sys.argv) > 1 ):
        tokenizer = CTokenizer(  )
        for t in tokenizer.tokenize( sys.argv[1] ):
            print(t)
    else:
        print( "Error: invalid arguments " )


if __name__ == '__main__':

    main()



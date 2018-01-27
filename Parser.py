

# ------------------------
#  - - - Structures - - -
# ------------------------

class C_Set :

    def __init__ ( self, set_string ):

        self.cardinality = 0

    def union ( self, s ):

        pass

    def intersection ( self, s ):

        pass

    def compliment ( self, s ):

        pass

    def powerset ( self ):

        pass




# -----------------------
#  - - - Variables - - -
# -----------------------

definitions = { }


# ------------------------
#  - - - Precedence - - -
# ------------------------

precedence = (

)




# -----------------------------
#  - - - Parser Patterns - - -
# -----------------------------

# Elements with urelemental values
def p_urelemental ( p ):
    '''urelemental : LPAREN urelemental RPAREN
                   | CARDINALITY set
                   | urelemental PLUS urelemental
                   | urelemental MINUS urelemental
                   | urelemental TIMES urelemental
                   | urelemental DIVIDE urelemental
                   | urelemental GT urelemental
                   | urelemental LT urelemental
                   | urelemental GE urelemental
                   | urelemental LE urelemental
                   | INTEGER
    '''

    # INTEGER
    if( len(p) == 2 ):
        p[0] = int( p[1] )
    
    # CARDINALITY_BRACE set CARDINALITY_BRACE
    elif p[1] == '|':
        p[0] = p[2].cardinality

    # LPAREN urelemental RPAREN
    elif p[1] == '(':
        p[0] = p[2]

    # urelemental OPERATION urelemental
    elif p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '<':
        p[0] = 1 if (p[1]< p[3]) else 0
    elif p[2] == '>':
        p[0] = 1 if (p[1]> p[3]) else 0
    elif p[2] == '≤':
        p[0] = 1 if (p[1]<=p[3]) else 0
    elif p[2] == '≥':
        p[0] = 1 if (p[1]>=p[3]) else 0


# Elements with C_Set values
def p_set( p ):
    '''set : LPAREN set RPAREN
           | set UNION set
           | set INTERSECTION set
           | set COMPLIMENT set
           | POWERSET set
           | EMPTYSET
    '''

    







from Tokenizer import CTokenizer
import ply.yacc as yacc

tokenizer = CTokenizer()
tokens = CTokenizer.tokens


# ------------------------
#  - - - Structures - - -
# ------------------------

class Name_Engine:

  def __init__ ( self, label ):

    self.namespace   = label
    self.subspaces   = {}
    self.definitions = {}

    self.scope = []
    self.usings = [[]]

  def using ( self, namespace ):
    self.usings.append( namespace )

  def hang ( self, namespace ):
    space = self
    for ns in namespace[:-1]:
      space = space.subspaces[ns]
    space.subspaces[namespace[-1]] = Name_Engine( namespace[-1] )

  def store ( self, key, value, namespace = None ):
    if( namespace == None ): namespace = self.scope
    space = self
    for p in namespace:
      space = space.subspaces[p]
    
    space.definitions[key] = value

  def retrieve ( self, key, namespace = None ):
    if( namespace == None ): namespace = self.scope

    tor = None
    if( key in self.definitions ):
      tor =  self.definitions[key]
    space = self
    for p in namespace:
      space = space.subspaces[p]
      if( key in space.definitions ):
        tor = space.definitions[key]

    return tor


class Registry_Entry:
  
  def __init__( self, hash, data ):

    self.id = 0
    self.hash = hash
    self.data = data

class Registry:

  def __init__ ( self ):

    self.hash_table = { }
    self.id_table = []

  def insert( self, entry ):

    if ( not( entry.hash in self.hash_table) ):
      entry.id = len( self.hash_table )
      self.hash_table[ entry.hash ] = entry
      self.id_table.append( entry )
    else:
      entry = self.hash_table[entry.hash]

    return entry.id

  def register( self, data ):

    hash = ''
    if( isinstance( data, int ) ):
      hash = 'u%s' % data

    elif( isinstance( data, C_Set) ):
      hash = r'{'+str(data.data)[1:-1]+'}'

    tor =  self.insert( Registry_Entry( hash, data ) )
    return tor

  def retrieve_raw( self, addr ):
    d = self.id_table[addr]
    return d

  def show( self ):
    print ( "\nTable - %s"%len(self.id_table))
    for x in self.id_table:
      print ( "%s : %s : %s" %( x.id, x.hash, x.data ) )

registry = Registry()

class C_Set:

  def __init__ ( self, data = [] ):

      self.data = data

  def union ( self, s ):

      return C_Set( self.data + [ x for x in s.data if not( x in self.data) ] )

  def intersection ( self, s ):

      return C_Set( [ x for x in self.data if x in s.data ] )

  def complement ( self, s ):

      return C_Set( [x for x in self.data if not(x in s.data) ] )

  def powerset ( self ):

    return C_Set( [] )

  def add ( self, expression ):

      if not( expression in self.data ):
        self.data.append( expression )

  def addAll ( self, expressions ):

      self.data += [ x for x in expressions if not( x in self.data ) ]

  def cardinality( self ):

    return len( self.data )


class C_Function :

  def __init__ ( self, param ):

    self.param = param

  def resolve ( self, params ):

    pass


# -----------------------
#  - - - Variables - - -
# -----------------------

names = Name_Engine('global')


# ------------------------
#  - - - Precedence - - -
# ------------------------

precedence = (
  ('left','PLUS','MINUS','UNION','INTERSECTION'),
  ('left','TIMES','DIVIDE'),
  ('right','POWERSET'),
  ('nonassoc','CARDINALITY', 'UMINUS')
)






# -----------------------------
#  - - - Parser Patterns - - -
# -----------------------------

def p_block_body ( p ):
  '''body : 
          | block body 
          | definition body 
          | expression body
          | comment body
  '''

  p[0] = []
  if( len( p ) > 1 ):
    if( p[1] != None ):
      p[0].append( p[1] )
    p[0] += p[2]

def p_block ( p ):
  
  'block : block_open body block_close'

  if ( p[1] == "query" ):
    print( registry.id_table[p[2][0]].data )

  elif( p[1] == "using" ):
    names.using( p[2][0] )

  elif( p[1] == "export" ):
    pass

  elif( p[1] == "import" ):
    pass

def p_block_open ( p ):  
  '''block_open : STARTOPENTAG IDENTIFIER IDENTIFIER ENDTAG
                | STARTOPENTAG IDENTIFIER ENDTAG'''

  p[0] = p[2]

  if( p[2] == "namespace" ):
    names.scope.append( p[3] )
    names.hang( names.scope )

  elif( p[2] == "pretty_printer" ):
    pass

  elif( p[2] == "replace" ):
    pass

def p_block_close ( p ):
  
  '''block_close : STARTCLOSETAG IDENTIFIER ENDTAG'''

  p[0] = p[2]

  if( p[2] == "namespace" ):
    names.scope.pop()

  elif( p[2] == "pretty_printer" ):
    pass

# ----------------
# || definition ||
# ----------------

def p_definition_variable ( p ):
  'definition : IDENTIFIER DENOTES expression'
  names.store( p[1], p[3] )

# ----------------
# || expression ||
# ----------------

def p_expression ( p ):
  '''expression : set 
                | urelemental
                | IDENTIFIER'''

  if ( isinstance( p[1], str ) ):

    q = p[1].split('::')

    val = names.retrieve( q[-1], names.scope + q[:-1] )
    if (p[0] != None):
      val = names.retrieve( q[-1], q[:-1] )
    if( val != None ):
      p[0] = val
    #else:
    #  p[0] = C_Function( p[1] )

  else:
    p[0] = p[1]


# -----------------
# || urelemental ||
# -----------------

def p_urelemental ( p ):
    '''urelemental : LPAREN urelemental RPAREN
                   | CARDINALITY expression
                   | expression PLUS expression
                   | expression MINUS expression
                   | expression TIMES expression
                   | expression DIVIDE expression
                   | expression GT expression
                   | expression LT expression
                   | expression GE expression
                   | expression LE expression
                   | expression EQUALS expression
                   | MINUS expression %prec UMINUS
                   | INTEGER
    '''

    urel = None

    # INTEGER
    if( len(p) == 2 ):
        
        urel = p[1]
    
    # Unaries
    elif p[1] == '#':
      assert( isinstance( p[1], C_Set ) )
      urel = registry.id_table[p[1]].data.cardinality()

    elif p[1] == '-':
      assert( isinstance( registry.id_table[p[1]].data, int ) )
      urel = -registry.id_table[p[1]].data

    # LPAREN urelemental RPAREN
    elif p[1] == '(':
        urel = p[2].data

    # urelemental OPERATION urelemental
    else:

      assert( isinstance( p[1], int ) and isinstance( p[3], int ) )
      
      if p[2] == '+':
        urel = registry.id_table[p[1]].data + registry.id_table[p[3]].data
      elif p[2] == '-':
        urel = registry.id_table[p[1]].data - registry.id_table[p[3]].data
      elif p[2] == '*':
        urel = registry.id_table[p[1]].data * registry.id_table[p[3]].data
      elif p[2] == '/':
        urel = registry.id_table[p[1]].data / registry.id_table[p[3]].data
      elif p[2] == '<':
        urel = 1 if (registry.id_table[p[1]].data < registry.id_table[p[3]].data ) else 0
      elif p[2] == '>':
        urel = 1 if (registry.id_table[p[1]].data > registry.id_table[p[3]].data ) else 0
      elif p[2][0] == '=':
        urel = 1 if (registry.id_table[p[1]].data == registry.id_table[p[3]].data ) else 0

    p[0] = registry.register( urel )

# ---------
# || set ||
# ---------

def p_set( p ):
  '''set : LPAREN set RPAREN
         | expression UNION expression
         | expression INTERSECTION expression
         | expression COMPLEMENT expression
         | POWERSET expression
  '''

  newset = None

  if( len(p) == 3 ):
    newset = p[2].powerset()
  elif ( p[1] == '(' ):
    assert( isinstance( p[2], C_Set ) )
    newset = p[2]
  else:

    a = registry.id_table[p[1]].data
    b = registry.id_table[p[3]].data

    if ( p[2] == '∪' ):
      newset = a.union( b )
    elif ( p[2] == '∩' ):
      newset = a.intersection( b )
    elif ( p[2] == '\\' ):
      newset = a.complement( b )

  if( newset != None):
    p[0] = registry.register( newset )


def p_emptyset( p ):
  'set : EMPTYSET'
  empty = C_Set([])
  p[0] = registry.register( empty )

def p_rawset( p ):
    '''set : STARTSET ENDSET
           | STARTSET expression setinsidetail ENDSET
    '''

    rawset = C_Set([])
    
    if( len( p ) > 3 ):
      rawset.add ( p[2] )
      rawset.addAll ( p[3] )

    

    p[0] = registry.register( rawset )

def p_setinsidetail( p ):
  '''setinsidetail : 
                   | COMMA expression setinsidetail'''

  rawsetinside = [ ]

  if( len(p) > 1 ):
    rawsetinside.append( p[2] )
    rawsetinside += p[3]

  p[0] = rawsetinside

# -------------
# || comment ||
# -------------

def p_comment( p ):
  'comment : COMMENT'
  return None

yacc.yacc()

while True:
    try:
        s = input('\n\n\n> ')   # use input() on Python 3
    except EOFError:
        break
    output = yacc.parse(s)
    print( output )
    registry.show()




# Cantor

## Declarative Programming in Straight Up Set Theory



```
[namespace booleans]

    ### Boolean Primitives ###

    false : {}
    true  : {{}}

    ### Logical Operators ###

    not ( a ) : true \ a
    and ( a, b ) : a ∩ b
    or  ( a, b ) : a ∪ b
    xor ( a, b ) : ( a \ b) ∪ (b \ a )

    nand ( a, b ) : not( and( a, b) )
    nor  ( a, b ) : not( or ( a, b) )
    nxor ( a, b ) : not( xor( a, b) )

[/namespace]


### Printer Replacements ###

[pretty_printer]

    ### Print Boolean Primitives by name instead of set ###

    [replace True] booleans::true [/replace]
    [replace False] booleans::false [/replace]

    ### Query for True xor False ###

    [query true_nxor_false]

        booleans::nxor( booleans::true, booleans::false )

    [/query]

[/pretty_printer]


### Console Output:
> true_nxor_false = False
###
```

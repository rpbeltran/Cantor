
# Cantor

## Declarative Programming in Straight Up Set Theory

Cantor is a programming language built around basic set-theoretic operators and syntax and namespacing rules. After formal definitions are formally declared, values may be queried in a method which is in many ways reminiscent of Prolog. Cantor is designed to run efficiently with minimal room for errors. Cantor was originally conceived as a way of simplifying the task of writing algorithms to achieve automated software verification for developing provably bug-free code.

Cantor is a versatile language capable of being used in many real applications. It is also surprisingly well suited to hardware description tasks, and a simple isomorphism to boolean algebra would likely make a synthesis pipeline for FPGA feasible (if an FPGA manufacturer were ever to embrace open source tooling).

Cantor can interpret whole programs or run inside a REPL environment.

## Example Cantor Program

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

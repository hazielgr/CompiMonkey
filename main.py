from gramatic import *

def main():
    # Test it out
    data = '''
    3 + 4 * 10
      20 *2
    '''

    # Give the lexer some input
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok)
        try:
            s = data
        except EOFError:
            break
        if not s: continue
        result = parser.parse(s)
        print(result)


    print("Hello World!")


if __name__ == "__main__":
    main()

    # Test it out
    #data = '''
    #3 + 4 * 10
    #  + -20 *2
    #'''

    # Give the lexer some input
    #lexer.input(data)

    # Tokenize
    #while True:
    #    tok = lexer.token()
    #    if not tok:
    #        break  # No more input
    #    print(tok)
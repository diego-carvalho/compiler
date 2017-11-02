import lexical_analyzer
import syntactic_analyzer

if __name__ == '__main__':
    lexical_analyzer.run()
    tokens, program = lexical_analyzer.getOut()
    print(tokens)
    syntactic_analyzer.run(tokens)
    
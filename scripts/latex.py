class Foo(object):
    def __init__(self,
                 gov2,
                 min_terms,
                 max_terms,
                 docs,
                 terms,
                 postings,
                 bytes):
        self.gov2_directors = gov2
        self.min_terms_per_document = min_terms
        self.max_terms_per_document = max_terms
        self.documents = docs
        self.terms = terms
        self.postings = postings
        self.bytes = bytes

a = Foo(273, 128, 255, 12345, 987654, 645678, 7654321233)
b = Foo(273, 1024, 2047, 212345, 4987654, 72345678, 3476543233)
c = Foo(273, 2048, 4096, 312345, 5987654, 345678, 1276543233)

corpora = [a, b, c]

def latex_row(text_width, text, columns, field_name, format_string, filter = lambda x : x):
    print("    {{:<{}}}".format(text_width).format(text), end='')
    for i, column in enumerate(columns):
#        print(" & {{{}}}".format(format_string))
        print(" & {{{}}}".format(format_string).format(filter(getattr(column, field_name))), end='')
    print(r" \\")


def latex_corpora(corpora):
    print(r"\begin{table}[h]")
    print(r"  \caption{Corpora}")
    print(r"  \vspace{ - 04 mm}")
    print(r"  \label{tab:corpora}")
    print(r"  \begin{{tabular}}{{l{}}}".format('r' * len(corpora)))

    # Header
    print("    ", end = '')
    for i, corpus in enumerate(corpora):
        print(" & {}".format(chr(ord('A') + i)), end='')
    print(r" \\")

    print(r"    \hline")

#    latex_row(25, "Gov2 directories", corpora, "gov2_directors", ":>10,d")
    latex_row(25, "Min terms", corpora, "min_terms_per_document", ":>10,d")
    latex_row(25, "Max terms", corpora, "max_terms_per_document", ":>10,d")
    latex_row(25, "Documents", corpora, "documents", ":>10,d")
    latex_row(25, "Total terms", corpora, "terms", ":>10,d")
    latex_row(25, "Total postings", corpora, "postings", ":>10,d")
    latex_row(25, "Input text (GB)", corpora, "bytes", ":>10,.2f", lambda x: x / 1.0e9)

    print(r"    \hline")

    print(r"  \end{tabular}")
    print(r"\end{table}")

# latex_corpora(corpora)

def foobar():
    width = 17
    def row_format(field_format):
        return r"{{:<{1}}} & {{{0}}} & {{{0}}} & {{{0}}} & {{{0}}} \\".format(field_format, width)
    return row_format(":10,.2f")

# print(foobar())

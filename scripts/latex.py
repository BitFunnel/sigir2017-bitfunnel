import math

# class Foo(object):
#     def __init__(self,
#                  gov2,
#                  min_terms,
#                  max_terms,
#                  docs,
#                  terms,
#                  postings,
#                  bytes):
#         self.gov2_directors = gov2
#         self.min_terms_per_document = min_terms
#         self.max_terms_per_document = max_terms
#         self.documents = docs
#         self.terms = terms
#         self.postings = postings
#         self.bytes = bytes
#
# a = Foo(273, 128, 255, 12345, 987654, 645678, 7654321233)
# b = Foo(273, 1024, 2047, 212345, 4987654, 72345678, 3476543233)
# c = Foo(273, 2048, 4096, 312345, 5987654, 345678, 1276543233)
#
# corpora = [a, b, c]

def latex_row(text_width, text, columns, field_name, format_string, filter = lambda x : x):
    print("    {{:<{}}}".format(text_width).format(text), end='')
    for i, column in enumerate(columns):
#        print(" & {{{}}}".format(format_string))
        print(" & {{{}}}".format(format_string).format(filter(getattr(column, field_name))), end='')
    print(r" \\")


def latex_corpora(experiments):
    corpora = [experiment.analyze_bf_corpus(273) for experiment in experiments]
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
    latex_row(25, "Postings (M)", corpora, "postings", ":>10,.0f", lambda x: x / 1.0e6)
    latex_row(25, "Matches/query", corpora, "matches_per_query", ":>10,.0f")
    latex_row(25, "Input text (GB)", corpora, "bytes", ":>10,.2f", lambda x: x / 1.0e9)

    print(r"    \hline")

    print(r"  \end{tabular}")
    print(r"\end{table}")


def latex_performance_one(experiment_number, experiment, thread):
    bf = experiment.analyze_bf_index()
    lucene = experiment.analyze_lucene_index()
    mg4j = experiment.analyze_mg4j_index()
    pef = experiment.analyze_pef_index()

    print(r"    \multirow{{5}}{{*}}{{{}}}".format(chr(ord('A') + experiment_number)), end='')
    print(r"& {:<25} & {:>10,.0f} & {:>10,.0f} & {:>10,.0f} & {:>10,.0f} \\".format(
        "QPS",
        bf.qps[thread],
        pef.qps[thread],
        mg4j.qps[thread],
        lucene.qps[thread]))

    print(r"                      ", end='')
    print(r"& {:<25} & {:>10,.2f} & {:>10,.2f} & {:>10,.2f} & {:>10,.2f} \\".format(
        "Fixed overhead (\%)",
        bf.planning_overhead[thread] * 100,
        pef.planning_overhead[thread] * 100,
        mg4j.planning_overhead[thread] * 100,
        lucene.planning_overhead[thread] * 100))

    print(r"                      ", end='')
    print(r"& {:<25} & {:>10,.2f} & {:>10,.2f} & {:>10,.2f} & {:>10,.2f} \\".format(
        "False positives (\%)",
        bf.false_positive_rate * 100,
        pef.false_positive_rate * 100,
        mg4j.false_positive_rate * 100,
        lucene.false_positive_rate * 100))

    print(r"                      ", end='')
    print(r"& {:<25} & {:>10,.2f} & {:>10,.2f} & {:>10,.2f} & {:>10,.2f} \\".format(
        "Bits per posting",
        bf.bits_per_posting,
        pef.bits_per_posting,
        mg4j.bits_per_posting,
        lucene.bits_per_posting))

    print(r"                      ", end='')
    print(r"& {:<25} & {:>10,.0f} & {:>10,.0f} & {:>10,.0f} & {:>10,.0f} \\".format(
        "DQ",
        bf.qps[thread] / bf.bits_per_posting,
        pef.qps[thread] / pef.bits_per_posting,
        mg4j.qps[thread] / mg4j.bits_per_posting,
        math.nan))


def latex_performance(experiments):
    print(r"\begin{table}[h]")
    print(r"  \caption{Query Processing Performance}")
    print(r"  \vspace{ - 04 mm}")
    print(r"  \label{tab:query-processing}")
    print(r"  \centering")
    print(r"  \begin{tabular}{llrrrr}")
    print(r"  & & BitFunnel & PEF & MG4J & Lucene \\")
    print(r"    \hline")

    for experiment_number, experiment in enumerate(experiments):
        latex_performance_one(experiment_number, experiment, 6)
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

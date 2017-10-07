import numpy
import os
import random


# Writes a collection of documents as a GOV2 collection if  HTML documents.
class HTMLWriter:
    def __init__(self):
        pass

    def on_file_enter(self, stream):
        self.stream = stream

    def on_document_enter(self, id):
        template = ( "<DOC>\n"
                     "<DOCNO>{0}</DOCNO>\n"
                     "<DOCHDR>\n"
                     "</DOCHDR>\n"
                     "<html>\n" )

        text = template.format(id)
        self.stream.write(text.encode('utf-8'))


    def on_stream_enter(self, id):
        self.stream_id = id
        if id == 0:
            # This is the body
            text = ("  <body>\n"
                    "    ")
        elif id == 1:
            # This is the title
            text = ("  <head>\n"
                    "    <title>\n"
                    "      ")
        else:
            raise ValueError('Expected id value of 0 or 1.')

        self.stream.write(text.encode('utf-8'))


    def on_term(self, term):
        text = ' ' + term
        self.stream.write(text.encode('utf-8'))


    def on_stream_exit(self):
        if self.stream_id == 0:
            # This is the body
            text = ("\n"
                    "  </body>\n")
        elif self.stream_id == 1:
            # This is the title
            text = ("\n"
                    "    </title>\n"
                    "  </head>\n")
        else:
            raise ValueError('Expected id value of 0 or 1.')

        self.stream.write(text.encode('utf-8'))


    def on_document_exit(self):
        text = ( "</html>\n"
                 "</DOC>\n" )

        self.stream.write(text.encode('utf-8'))


    def on_file_exit(self):
        pass


# Writes a collection of documents as a BitFunnel chunk file.
class ChunkWriter:
    def __init__(self):
        pass

    def on_file_enter(self, stream):
        self.stream = stream

    def on_document_enter(self, id):
        # print("  Document({0})".format(id))
        text = '{0:016x}'.format(id)
        self.stream.write(text.encode('utf-8'))
        self.write_end_mark()

    def on_stream_enter(self, id):
        self.term_count = 0
        text = '{0:02x}'.format(id)
        self.stream.write(text.encode('utf-8'))
        self.write_end_mark()

    def on_term(self, term):
        # print("    {0}: {1}".format(self.term_count, term))
        self.term_count += 1
        self.stream.write(term.encode('utf-8'))
        self.write_end_mark()

    def on_stream_exit(self):
        self.write_end_mark()

    def on_document_exit(self):
        self.write_end_mark()

    def on_file_exit(self):
        self.write_end_mark()

    def write_end_mark(self):
        self.stream.write(bytes([0]))


# Simple test generates the example chunk file described at
# http://bitfunnel.org/corpus-file-format/
def test():
    writer = ChunkWriter();
    with open(r'c:\temp\somefile.bin', 'wb') as file:
        writer.on_file_enter(file)

        writer.on_document_enter(18)
        writer.on_stream_enter(0)
        writer.on_term('Dogs')
        writer.on_stream_exit()

        writer.on_stream_enter(1)
        writer.on_term('Dogs')
        writer.on_term('are')
        writer.on_term("man's")
        writer.on_term('best')
        writer.on_term('friend.')
        writer.on_stream_exit()

        writer.on_document_exit()

        writer.on_document_enter(200)
        writer.on_stream_enter(0)
        writer.on_term('Cat')
        writer.on_term('Tacts')
        writer.on_stream_exit()

        writer.on_stream_enter(1)
        writer.on_term('The')
        writer.on_term('internet')
        writer.on_term('is')
        writer.on_term('made')
        writer.on_term('of')
        writer.on_term('cats.')
        writer.on_stream_exit()

        writer.on_document_exit()

        writer.on_file_exit()

# test()

# Appends a document to writer (current choices are HTMLWriter and ChunkWriter).
def append_document(id,
                    min_terms,
                    max_terms,
                    writer):
    writer.on_document_enter(id)

    # Keep track of the number of terms added.
    term_count = 0;

    # Write the title, which takes the form "tID" where ID is the document's id.
    # The title format is chosen so that it is different from every other term
    # in the document.
    title = 't{0}'.format(id)
    writer.on_stream_enter(1)
    writer.on_term(title)
    term_count += 1
    writer.on_stream_exit()

    writer.on_stream_enter(0)

    # Use a random number gnerator to determine the number of unique terms
    # in this document.
    term_target = random.randrange(min_terms, max_terms + 1)

    # Now, generate terms corresponding to bits that are set in the
    # document id. These terms can be used to easily verify the that the
    # matcher returns the correct set of documents.
    # For each id bit B that is set, add a term of the form "xB".
    x = id
    for i in range(0, 64):
        if x % 2 != 0:
            term = "x{0}".format(i)
            writer.on_term(term)
            term_count += 1
        x //= 2

    # Now pad document with terms selected from a zipfian distribution.
    # Repeatedly sample a zipfian distribution of integer terms until we've
    # selected the desired number of unique terms.
    # These terms are just the text representation of non-negative integers.
    terms = set()
    for i in range(term_count, term_target):
        l = len(terms)
        while (len(terms) == l):
            terms.add(numpy.random.zipf(1.2,1)[0])
        l += 1

    for term in sorted(terms):
        writer.on_term("{0}".format(term))

    writer.on_stream_exit()
    writer.on_document_exit()


# Generates synthetic documents and writes them to a corpus file.
# Documents are appended to the corpus using a writer which can generate
# GOV2 format HTML or BitFunnel chunks.
#
# The number of unique terms in the document will be in the range
#   [min_terms, max_terms]
# Note that min_terms cannot be less than 65. The reason for this restriction
# is that each synthetic document contains a term corresponding to the document
# id and each bit that is set in the binary representation of the 64-bit
# document id. These terms are used to simplify the verification of correctness
# of the matching algorithm. These terms are encoded as "xB" where B is the
# integer bit position. So, for example, the document with id=9 would contain
# the terms "x0" and "x3".
#
# Terms not corresponding to bit positions are selected from a Zipfian
# distribution. Note that terms in a document won't have a perfect Zipfian
# distribution because of the terms associated with bits in the document id.
#
def create_index(path,
                 basename,
                 chunk_count,
                 documents_per_chunk,
                 min_terms,
                 max_terms,
                 writer):

    if min_terms < 65:
        raise ValueError("min_terms cannot be less than 64.")

    if max_terms < min_terms:
        raise ValueError("max_terms cannot be less than min_terms.")

    # Ensure that the function generates same index for each call with the
    # same parameters.
    random.seed(1234567)
    numpy.random.seed(1234567)

    if not os.path.exists(path):
        os.makedirs(path)

    # Generate document ids, starting at 0.
    id = 0;

    for chunk in range(0, chunk_count):
        filename = os.path.join(path, '{0}-{1}'.format(basename, chunk))
        print(filename)
        with open(filename, 'wb') as stream:
            writer.on_file_enter(stream)

            for i in range(0, documents_per_chunk):
                append_document(id, min_terms, max_terms, writer)
                id += 1

            writer.on_file_exit()



# create_index(r'c:\temp\corpus',
#              'chunk',
#              3,
#              5,
#              64,
#              127,
#              ChunkWriter())


create_index(r'c:\temp\corpus',
             'chunk',
             1,
             1000,
             65,
             127,
             ChunkWriter())


# create_index(r'c:\temp\corpus',
#              'chunk',
#              1,
#              4,
#              10,
#              10,
#              ChunkWriter())

import csv
import itertools
import math
import os
import platform
import re
from bf_utilities import run
from latex import latex_corpora


def execute(command, log_file = None):
    print(command)
    run(command, os.getcwd(), log_file)
    print("Finished")
    print()


class Experiment:
    def __init__(self,
                 bf_executables,
                 mg4j_repo,
                 pef_executables,
                 index_root,
                 basename,
                 chunk_dir,
                 chunk_pattern,
                 queries,
                 ingestion_thread_count,
                 min_thread_count,
                 max_thread_count):

        self.bf_executable = bf_executables
        self.mg4j_repo = mg4j_repo
        self.pef_executable = pef_executables

        self.index_root = index_root

        self.chunk_dir = chunk_dir
        self.chunk_pattern = chunk_pattern
        self.basename = basename
        self.queries = queries;

        self.ingestion_thread_count = ingestion_thread_count

        self.min_thread_count = min_thread_count
        self.max_thread_count = max_thread_count
        self.pef_index_type = 'opt'

        self.update()


    # update() recalculates properties derived from constructor parameters.
    # For convenience, one can change any of the members directly initialized
    # in the constructor and then call update() to regenerate the derived
    # members.
    def update(self):
        # TODO: Consider copying manifest into root.
        # TODO: What if manifest already exists? Consider pre-verification step that catches errors up front.
        # TODO: Consider basing root name off of manifest name.
        self.root = os.path.join(self.index_root, self.basename)

        self.bf_index_path = os.path.join(self.root, "bitfunnel")
        self.lucene_index_path = os.path.join(self.root, "lucene")
        self.mg4j_index_path = os.path.join(self.root, "mg4j")
        self.pef_index_path = os.path.join(self.root, "pef")

        self.manifest = os.path.join(self.root, self.basename + "-manifest.txt")

        # Java classpath for both mg4j and Lucene.
        # TODO: why does -shaded only show up on Windows? Can this be fixed in pom.xml or something?
        if (platform.system() == 'Windows'):
            self.classpath = os.path.join(self.mg4j_repo, "target", "mg4j-1.0-SNAPSHOT-shaded.jar")
        else:
            self.classpath = os.path.join(self.mg4j_repo, "target", "mg4j-1.0-SNAPSHOT.jar")

        self.thread_counts = range(self.min_thread_count, self.max_thread_count + 1)

        # Query-related variables
        self.queries_basename = os.path.basename(self.queries)
        self.query_path = os.path.join(self.root, "queries")
        self.root_query_file = os.path.join(self.query_path, self.queries_basename)

        # BitFunnel variables
        # TODO: don't hard code density.
        self.bf_density = 0.15
        self.bf_repl_script = os.path.join(self.bf_index_path, self.basename + "-repl.script")
        self.bf_shard_definition = os.path.join(self.bf_index_path, "ShardDefinition.csv")
        self.bf_build_statistics_log = os.path.join(self.bf_index_path, "build_bf_statistics_log.txt")
        self.bf_build_term_table_log = os.path.join(self.bf_index_path, "build_bf_term_table_log.txt")
        self.bf_run_queries_log = os.path.join(self.bf_index_path, "run_bf_queries_log.txt")

        # Lucene variables.
        self.lucene_build_index_log = os.path.join(self.lucene_index_path, "build_lucene_index_log.txt")
        self.lucene_results_file = []
        self.lucene_run_queries_log = []
        for i, threads in enumerate(self.thread_counts):
            filename = "{0}-results-{1}.csv".format(self.queries_basename, threads)
            self.lucene_results_file.append(os.path.join(self.lucene_index_path, filename))
            filename = "run_lucene_queries_log-{0}.txt".format(threads)
            self.lucene_run_queries_log.append(os.path.join(self.lucene_index_path, filename))

        # mg4j variables
        self.mg4j_basename = os.path.join(self.mg4j_index_path, self.basename)
        self.mg4j_build_index_log = os.path.join(self.mg4j_index_path, "build_mg4j_index_log.txt")
        self.mg4j_results_file = []
        self.mg4j_run_queries_log = []
        self.mg4j_filter_queries_log = os.path.join(self.mg4j_index_path, "filter_mg4j_queries_log.txt")
        for i, threads in enumerate(self.thread_counts):
            filename = "{0}-results-{1}.csv".format(self.queries_basename, threads)
            self.mg4j_results_file.append(os.path.join(self.mg4j_index_path, filename))
            filename = "run_mg4j_queries_log-{0}.txt".format(threads)
            self.mg4j_run_queries_log.append(os.path.join(self.mg4j_index_path, filename))

        # Partitioned ELias-Fano variables
        self.pef_basename = os.path.join(self.pef_index_path, self.basename)
        self.pef_collection = os.path.join(self.pef_index_path, self.basename)
        # TODO: don't hard-code opt
        self.pef_index_file = os.path.join(self.pef_index_path, self.basename + ".index." + self.pef_index_type)
        self.pef_creator = os.path.join(self.pef_executable, "create_freq_index")
        self.pef_runner = os.path.join(self.pef_executable, "Runner")
        self.pef_results_file = os.path.join(self.pef_index_path, self.queries_basename + "-results.csv")
        self.pef_build_collection_log = os.path.join(self.pef_index_path, "build_pef_collection_log.txt")
        self.pef_build_index_log = os.path.join(self.pef_index_path, "build_pef_index_log.txt")
        self.pef_run_queries_log = os.path.join(self.pef_index_path, "run_pef_queries_log.txt")

        # TODO: mapping to filtered query file is in Java right now. Can this be moved here?
        self.pef_query_file = os.path.join(self.query_path, self.queries_basename + "-in-index-ints.txt")
        self.filtered_query_file = os.path.join(self.query_path, self.queries_basename + "-in-index.txt")


    ###########################################################################
    #
    # Query log cleaning
    #
    ###########################################################################

    def fix_query_log(self):
        if not os.path.exists(self.query_path):
            os.makedirs(self.query_path)
        print("fixing {0} ==> {1}".format(self.queries, self.root_query_file))
        # We use this encoding because the default is UTF-8 and trec efficiency is not UTF-8.
        # We don't know if this is the correct encoding and may read bogus queries.
        with open(self.queries, 'r', encoding="ISO-8859-1") as f, open(self.root_query_file, 'w') as out:
            for line in f:
                # Remove leading line numbers.
                step1 = re.sub(r"\A\d+:", '', line)

                # Remove punctuation and then coalesce spaces and remove
                # leading and trailing spaces.
                step2 = ' '.join(re.sub(r"[-;:,&'\+\./\(\)]", ' ', step1).split())

                # Write to output file.
                if len(step2) > 0:
                    print(step2, file=out)


    ###########################################################################
    #
    # BitFunnel
    #
    ###########################################################################
    def build_bf_index(self):
        if not os.path.exists(self.bf_index_path):
            os.makedirs(self.bf_index_path)

        # We're currently restricted to a single shard,
        # so create an empty ShardDefinition file.
        open(self.bf_shard_definition, "w").close()

        # Run statistics builder
        args = ("{0} statistics {1} {2} -text").format(self.bf_executable,
                                                       self.manifest,
                                                       self.bf_index_path)
        execute(args, self.bf_build_statistics_log)

        # Run termtable builder
        # TODO: don't hard code Optimal.
        # TODO: don't hard code SNR.
        args = ("{0} termtable {1} {2} Optimal").format(self.bf_executable,
                                                        self.bf_index_path,
                                                        self.bf_density)
        execute(args, self.bf_build_term_table_log)


    def run_bf_queries(self):
        # Create script file
        # TODO: reinstate following lines.
        with open(self.bf_repl_script, "w") as file:
            file.write("threads {0}\n".format(self.ingestion_thread_count))
            file.write("load manifest {0}\n".format(self.manifest));
            file.write("status\n");
            file.write("compiler\n");
            for index, threads in enumerate(self.thread_counts):
                results_dir = os.path.join(self.bf_index_path, "results-{0}".format(threads))
                if not os.path.exists(results_dir):
                    print("mkdir " + results_dir)
                    os.makedirs(results_dir)
                file.write("threads {0}\n".format(threads))
                file.write("cd {0}\n".format(results_dir))
                file.write("query log {0}\n".format(self.filtered_query_file))

            file.write("quit\n")

        # Start BitFunnel repl
        args = ("{0} repl {1} -script {2}").format(self.bf_executable,
                                                   self.bf_index_path,
                                                   self.bf_repl_script)
        execute(args, self.bf_run_queries_log)


    def analyze_bf_index(self):
        results = IndexCharacteristics("BitFunnel", self.ingestion_thread_count, self.thread_counts)

        with open(self.bf_run_queries_log, 'r') as myfile:
            run_queries_log = myfile.read()
            results.set_float_field("bits_per_posting", "Bits per posting:", run_queries_log)
            results.set_float_field("total_ingestion_time", "Total ingestion time:", run_queries_log)

        for i, threads in enumerate(self.thread_counts):
            query_summary_statistics = os.path.join(self.bf_index_path,
                                                    "results-{0}".format(threads),
                                                    "QuerySummaryStatistics.txt")
            with open(query_summary_statistics, 'r') as myfile:
                data = myfile.read()
                results.append_float_field("planning_overhead", r"Planning overhead:", data)
                results.append_float_field("qps", "QPS:", data)
                results.append_float_field("mean_query_latency", "Mean query latency:", data)

        self.compute_false_positive_rate(results);

        return results


    def analyze_bf_corpus(self, gov2_directories, min_terms_per_document, max_terms_per_document):
        results = CorpusCharacteristics(gov2_directories, min_terms_per_document, max_terms_per_document)

        with open(self.bf_build_statistics_log, 'r') as myfile:
            build_statistics_log = myfile.read()
            results.set_int_field("documents", "Document count:", build_statistics_log)
            results.set_int_field("terms", "Raw DocumentFrequencyTable count:", build_statistics_log)
            results.set_int_field("postings", "Posting count:", build_statistics_log)
            results.set_int_field("bytes", "Total bytes read:", build_statistics_log)

        return results


    ###########################################################################
    #
    # Lucene
    #
    ###########################################################################
    def build_lucene_index(self):
        if not os.path.exists(self.lucene_index_path):
            print("mkdir " + self.lucene_index_path)
            os.makedirs(self.lucene_index_path)
        args = ("java -cp {0} "
                "org.bitfunnel.runner.IndexBuilder "
                "{1} {2} {3}").format(self.classpath,
                                      self.lucene_index_path,
                                      self.manifest,
                                      self.ingestion_thread_count, )
        print(args)
        execute(args, self.lucene_build_index_log)


    def run_lucene_queries(self):
        for i, threads in enumerate(self.thread_counts):
            args = ("java -cp {0} "
                    "org.bitfunnel.reproducibility.QueryLogRunner "
                    "lucene {1} {2} {3} {4}").format(self.classpath,
                                                     self.lucene_index_path,
                                                     self.filtered_query_file,
                                                     self.lucene_results_file[i],
                                                     threads)
            print(args)
            execute(args, self.lucene_run_queries_log[i])


    def analyze_lucene_index(self):
        results = IndexCharacteristics("Lucene", self.ingestion_thread_count, self.thread_counts)
        results.index_type = "Lucene"

        # Don't know how to determine bits per posting for Lucene.
        results.bits_per_posting = math.nan

        with open(self.lucene_build_index_log, 'r') as myfile:
            build_index_log = myfile.read()
            results.total_ingestion_time = \
                float(re.findall("Ingested \d+ chunk files in (\d+\.?\d+) seconds.", build_index_log)[0])

        for i, threads in enumerate(self.thread_counts):
            run_queries_log = self.lucene_run_queries_log[i]
            with open(run_queries_log, 'r') as myfile:
                data = myfile.read()
                results.append_float_field("qps", "QPS:", data)
                results.append_float_field("mean_query_latency", "Mean query latency:", data)
                results.append_float_field("planning_overhead", r"Planning overhead:", data)

        # Lucene false positive rate is always zero.
        results.false_positive_rate = 0;
        results.false_negative_rate = 0;

        return results


    ###########################################################################
    #
    # MG4J
    #
    ###########################################################################
    def build_mg4j_index(self):
        if (platform.system() == 'Windows'):
            args = ("java -cp {0} "
                "it.unimi.di.big.mg4j.tool.IndexBuilder "
                "-o org.bitfunnel.reproducibility.ChunkManifestDocumentSequence({1}) "
                "{2}").format(self.classpath, self.manifest, self.mg4j_basename)
        else:
            args = ("java -cp {0} "
                "it.unimi.di.big.mg4j.tool.IndexBuilder "
                "-o org.bitfunnel.reproducibility.ChunkManifestDocumentSequence\({1}\) "
                "{2}").format(self.classpath, self.manifest, self.mg4j_basename)
        if not os.path.exists(self.mg4j_index_path):
            os.makedirs(self.mg4j_index_path)
        execute(args, self.mg4j_build_index_log)


    def run_mg4j_queries(self):
        for i, threads in enumerate(self.thread_counts):
            args = ("java -cp {0} "
                    "org.bitfunnel.reproducibility.QueryLogRunner "
                    "mg4j {1} {2} {3} {4}").format(self.classpath,
                                                   self.mg4j_basename,
                                                   self.filtered_query_file,
                                                   self.mg4j_results_file[i],
                                                   threads)
            execute(args, self.mg4j_run_queries_log[i])


    def filter_query_log(self):
        args = ("java -Xmx16g -cp {0} "
                "org.bitfunnel.reproducibility.IndexExporter "
                "{1} {2} "
                "--queries {3}").format(self.classpath,
                                        self.mg4j_basename,
                                        self.query_path,
                                        self.root_query_file);
        execute(args, self.mg4j_filter_queries_log)


    def analyze_mg4j_index(self):
        results = IndexCharacteristics("MG4J", self.ingestion_thread_count, self.thread_counts)

        # Compute bits/posting.
        with open(self.mg4j_run_queries_log[0], 'r') as myfile:
            run_queries_log = myfile.read()

            posting_count = float(re.findall("postings=(\d+\.?\d+)", run_queries_log)[0])
            pointers = os.path.join(self.mg4j_index_path, self.basename + "-text.pointers");
            results.bits_per_posting = os.path.getsize(pointers) / posting_count * 8.0

        # Need to annotate build log from Python since Java code doesn't print time.
        results.total_ingestion_time = math.nan

        for i, threads in enumerate(self.thread_counts):
            run_queries_log = self.mg4j_run_queries_log[i]
            with open(run_queries_log, 'r') as myfile:
                data = myfile.read()
            results.append_float_field("qps", "QPS:", data)
            results.append_float_field("mean_query_latency", "Mean query latency:", data)
            results.planning_overhead.append(math.nan)

        # MG4J false positive rate is always zero.
        results.false_positive_rate = 0;
        results.false_negative_rate = 0;

        return results


    ###########################################################################
    #
    # Partitioned Elias-Fano (PEF)
    #
    ###########################################################################
    def build_pef_collection(self):
        if not os.path.exists(self.pef_index_path):
            os.makedirs(self.pef_index_path)

        args = ("java -cp {0} -Xmx16g "
                "org.bitfunnel.reproducibility.IndexExporter "
                "{1} {2} --index").format(self.classpath, self.mg4j_basename, self.pef_basename);
        execute(args, self.pef_build_collection_log)


    def build_pef_index(self):
        args = ("{0} {1} {2} {3}").format(self.pef_creator,
                                          self.pef_index_type,
                                          self.pef_collection,
                                          self.pef_index_file)
        execute(args, self.pef_build_index_log)


    def run_pef_queries(self):
        # TODO: rework PEF Runner and run_pef_queries to put the for-loop over threads here.
        # This will allow us to loop over a collection of thread counts instead of range(0, threadCount)
        # which we do today.
        args = ("{0} {1} {2} {3} {4} {5}").format(self.pef_runner,
                                                  self.pef_index_type,
                                                  self.pef_index_file,
                                                  self.pef_query_file,
                                                  self.max_thread_count,
                                                  self.pef_results_file)
        execute(args, self.pef_run_queries_log)


    def analyze_pef_index(self):
        results = IndexCharacteristics("PEF", self.ingestion_thread_count, self.thread_counts)

        with open(self.pef_build_index_log, 'r') as myfile:
            build_index_log = myfile.read()
            results.set_float_field("bits_per_posting", '"bits_per_doc":', build_index_log)
            results.set_float_field("total_ingestion_time", "collection built in", build_index_log)

        for i, threads in enumerate(self.thread_counts):
            query_summary_statistics = os.path.join(
                self.pef_index_path,
                "{0}-results.csv-summary-{1}.txt".format(self.queries_basename, threads))
            with open(query_summary_statistics, 'r') as myfile:
                data = myfile.read()
                results.append_float_field("qps", "QPS:", data)
                results.append_float_field("mean_query_latency", "Mean query latency:", data)

                # PEF does no parsing and planning.
                results.planning_overhead.append(0)

        # PEF false positive rate is always zero.
        results.false_positive_rate = 0;
        results.false_negative_rate = 0;

        return results


    ###########################################################################
    #
    # Chunk manifests
    #
    ###########################################################################
    def build_chunk_manifest(self):
        if not os.path.exists(self.root):
            os.makedirs(self.root)

        regex = re.compile(self.chunk_pattern)
        chunks = [os.path.join(self.chunk_dir, f)
                  for root, dirs, files in os.walk(self.chunk_dir)
                  for f in files
                  if regex.search(f) is not None]

        for chunk in chunks:
            print(chunk)

        print("Writing manifest {0}".format(self.manifest))
        with open(self.manifest, 'w') as file:
            for chunk in chunks:
                file.write(chunk + '\n')


    ###########################################################################
    #
    # False positive rate
    #
    ###########################################################################
    def compute_false_positive_rate(self, results):
        # TODO: Put this path in the constructor.
        # TODO: why is this results-1 and not all results?
        if (platform.system() == 'Windows'):
            bf = os.path.join(self.bf_index_path, "results-1\QueryPipelineStatistics.csv");
        else:
            bf = os.path.join(self.bf_index_path, "results-1/QueryPipelineStatistics.csv");
        mg4j = self.mg4j_results_file[0]

        count = 0;
        total_matches = 0
        total_queries = 0
        false_positives = 0
        false_positive_queries = 0
        false_negatives = 0
        false_negative_queries = 0

        with open(bf, newline='') as bf_results, open(mg4j, newline='') as mg4j_results:
            # Discard header line.
            bf_results.readline()
            mg4j_results.readline()
            bf_reader = csv.reader(bf_results, delimiter=',', quotechar='|')
            mg4j_reader = csv.reader(mg4j_results, delimiter=',', quotechar='|')
            for bfRow, mg4jRow in itertools.zip_longest(bf_reader, mg4j_reader):
                bf_matches = int(bfRow[2])
                mg4j_matches = int(mg4jRow[1])

                total_queries += 1
                total_matches += mg4j_matches

                if (bf_matches > mg4j_matches):
                    false_positives += (bf_matches - mg4j_matches)
                    false_positive_queries += 1
                elif (bf_matches < mg4j_matches):
                    false_negatives += (mg4j_matches - bf_matches)
                    false_negative_queries += 1

        results.total_matches = total_matches
        results.total_queries = total_queries
        results.false_positives = false_positives
        results.false_positive_queries = false_positive_queries
        results.false_positive_rate = false_positives / total_matches
        results.false_negatives = false_negatives
        results.false_negative_queries = false_negative_queries
        results.false_negative_rate = false_negatives / total_matches


    ###########################################################################
    #
    # Analyze
    #
    ###########################################################################
    def anayze_corpus(self):
        # Documents
        # Terms
        # Postings
        pass


    def summarize(self, thread):
        bf = self.analyze_bf_index()
        lucene = self.analyze_lucene_index()
        mg4j = self.analyze_mg4j_index()
        pef = self.analyze_pef_index()

        header = r"{:<25} & {:>10} & {:>10} & {:>10} & {:>10} \\"
        row = r"{:<25} & {:>10,.2f} & {:>10,.2f} & {:>10,.2f} & {:>10,.2f} \\"
        row_ints = r"{:<25} & {:>10,d} & {:>10,d} & {:>10,d} & {:>10,d} \\"

        first_column_width = 25
        def row_format(field_format):
            return r"{{:<{1}}} & {{{0}}} & {{{0}}} & {{{0}}} & {{{0}}} \\".format(field_format, first_column_width)

        print(header.format("", bf.index_type, pef.index_type, mg4j.index_type, lucene.index_type))
        # print(row_ints.format("Ingestion threads",
        #                       bf.ingestion_thread_count,
        #                       pef.ingestion_thread_count,
        #                       mg4j.ingestion_thread_count,
        #                       lucene.ingestion_thread_count))
        # print(row.format("Ingestion time (s)",
        #                  bf.total_ingestion_time,
        #                  pef.total_ingestion_time,
        #                  mg4j.total_ingestion_time,
        #                  lucene.total_ingestion_time))
        # print(row_ints.format("Query threads",
        #                       bf.thread_counts[thread],
        #                       pef.thread_counts[thread],
        #                       mg4j.thread_counts[thread],
        #                       lucene.thread_counts[thread]))
        print(row.format("QPS ({} threads)".format(bf.thread_counts[thread]),
                         bf.qps[thread],
                         pef.qps[thread],
                         mg4j.qps[thread],
                         lucene.qps[thread]))
        print(row.format("Mean Latency (us)",
                         bf.mean_query_latency[thread] * 1e6,
                         pef.mean_query_latency[thread] * 1e6,
                         mg4j.mean_query_latency[thread] * 1e6,
                         lucene.mean_query_latency[thread] * 1e6))
        print(row.format(r"Planning overhead (\%)",
                         bf.planning_overhead[thread] * 100,
                         pef.planning_overhead[thread] * 100,
                         mg4j.planning_overhead[thread] * 100,
                         lucene.planning_overhead[thread] * 100))
        print(row.format(r"False positives (\%)",
                         bf.false_positive_rate * 100,
                         pef.false_positive_rate * 100,
                         mg4j.false_positive_rate * 100,
                         lucene.false_positive_rate * 100))
        print(row.format("Bits/posting",
                         bf.bits_per_posting,
                         pef.bits_per_posting,
                         mg4j.bits_per_posting,
                         lucene.bits_per_posting))
        print(row.format("DQ",
                         bf.qps[thread] / bf.bits_per_posting,
                         pef.qps[thread] / pef.bits_per_posting,
                         mg4j.qps[thread] / mg4j.bits_per_posting,
                         math.nan))


    def summarize_corpus(self, gov2_directories, min_terms_per_document, max_terms_per_document):
        corpus = self.analyze_bf_corpus(gov2_directories,
                                        min_terms_per_document,
                                        max_terms_per_document)

        header = "{:<25} {:>15}"
        row_floats = "{:<25} {:>15.2f}"
        row_ints = "{:<25} {:>15,d}"

        print(header.format("", "A"))
        print(row_ints.format("Gov2 directories",
                              corpus.gov2_directors))
        print(row_ints.format("Min terms/document",
                              corpus.min_terms_per_document))
        print(row_ints.format("Max terms/document",
                              corpus.max_terms_per_document))
        print(row_ints.format("Documents",
                              corpus.documents))
        print(row_ints.format("Total terms",
                              corpus.terms))
        print(row_ints.format("Total postings",
                              corpus.postings))
        print(row_floats.format("Plain text input (GB)",
                                corpus.bytes / 1e9))


###########################################################################
#
# IndexCharacteristics
#
###########################################################################
class IndexCharacteristics(object):
    def __init__(self, index_type, ingestion_thread_count, thread_counts):
        self.index_type = index_type
        self.ingestion_thread_count = ingestion_thread_count
        self.thread_counts = thread_counts
        self.bits_per_posting = math.nan
        self.total_ingestion_time = math.nan
        self.false_positive_rate = math.nan
        self.false_negative_rate = math.nan
        self.qps = []
        self.mean_query_latency = []
        self.planning_overhead = []



    def set_float_field(self, property, text, log_data):
        result = re.findall("{0} (\d+\.?\d+)".format(text), log_data)
        if (len(result) > 0):
            value = float(result[0])
            setattr(self, property, value)
        else:
            print("ERROR: failed to extract", text, log_data)


    def append_float_field(self, property, text, log_data):
        result = re.findall("{0} (\d+\.?\d+)".format(text), log_data)
        if (len(result) > 0):
            value = float(result[0])
            value_list = getattr(self, property)
            value_list.append(value)
        else:
            print("ERROR: failed to extract", text, log_data)


    def print(self):
        print("Index type: {0}".format(self.index_type))
        print("Bits/posting: {0}".format(self.bits_per_posting))
        print("Ingestion threads: {0}".format(self.ingestion_thread_count))
        print("Ingestion time: {0}".format(self.total_ingestion_time))
        print("False positive rate: {0}".format(self.false_positive_rate))
        print("False negative rate: {0}".format(self.false_negative_rate))
        for i, threads in enumerate(self.thread_counts):
            print("{0} query threads:".format(threads))
            print("  QPS: {0}".format(self.qps[i]))
            print("  Mean query latency: {0}".format(self.mean_query_latency[i]))
            print("  Planning overhead: {0}".format(self.planning_overhead[i]))


###########################################################################
#
# CorpusCharacteristics
#
###########################################################################
class CorpusCharacteristics(object):
    def __init__(self, gov2_directories, min_terms_per_document, max_terms_per_document):
        self.gov2_directors = gov2_directories
        self.min_terms_per_document = min_terms_per_document
        self.max_terms_per_document = max_terms_per_document
        self.documents = math.nan
        self.terms = math.nan
        self.postings = math.nan
        self.bytes = math.nan

    def set_int_field(self, property, text, log_data):
        value = int(re.findall("{0} (\d+\.?\d+)".format(text), log_data)[0])
        setattr(self, property, value)

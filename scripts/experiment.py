import os
import re
import sys
from bf_utilities import run

def execute(command):
    print(command)
    print()
    # TODO: reinstate following line
    # run(command)


class Experiment:
    def __init__(self,
                 bf_executables,
                 mg4j_repo,
                 pef_executables,
                 bf_index_path,
                 mg4j_index_path,
                 pef_index_path,
                 manifest,
                 queries):

        self.bf_executable = bf_executables
        self.mg4j_repo = mg4j_repo
        self.pef_executable = pef_executables

        self.bf_index_path = bf_index_path
        self.mg4j_index_path = mg4j_index_path
        self.pef_index_path = pef_index_path

        self.manifest = manifest
        self.queries = queries;

        self.thread_count = 8
        self.pef_index_type = 'opt'

        self.update()


    # update() recalculates properties derived from constructor parameters.
    # For convenience, one can change any of the members directly initialized
    # in the constructor and then call update() to regenerate the derived
    # members.
    def update(self):
        self.basename = os.path.basename(self.manifest).split('.')[0];

        # BitFunnel variables
        self.bf_repl_script = os.path.join(self.bf_index_path, self.basename + "-repl.script")
        self.bf_shard_definition = os.path.join(self.bf_index_path, self.basename + "ShardDefinition.csv")

        # mg4j variables
        self.mg4j_classpath = os.path.join(self.mg4j_repo, "target", "mg4j-1.0-SNAPSHOT-jar-with-dependencies.jar")
        self.mg4j_basename = os.path.join(self.mg4j_index_path, self.basename)

        # Partitioned ELias-Fano variables
        self.pef_basename = os.path.join(self.pef_index_path, self.basename)
        self.pef_collection = os.path.join(self.pef_index_path, self.basename)
        # TODO: don't hard-code opt
        self.pef_index_file = os.path.join(self.pef_index_path, self.basename + ".index." + self.pef_index_type)
        self.pef_creator = os.path.join(self.pef_executable, "create_freq_index")
        self.pef_runner = os.path.join(self.pef_executable, "Runner")

        # TODO: mapping to filtered query file is in Java right now. Can this be moved here?
        self.queries_basename = os.path.basename(self.queries)
        self.pef_query_file = os.path.join(self.pef_index_path, self.queries_basename + "-ints.txt")
        self.filtered_query_file = os.path.join(self.pef_index_path, self.queries_basename + "-filtreed.txt")

        self.pef_results_file = os.path.join(self.pef_index_path, self.queries_basename + "-results.csv")
        self.mg4j_results_file = os.path.join(self.mg4j_index_path, self.queries_basename + "-results.csv")


    def build_mg4j_index(self):
        args = ("java -cp {0} "
                "it.unimi.di.big.mg4j.tool.IndexBuilder "
                "-o org.bitfunnel.reproducibility.ChunkManifestDocumentSequence({1}) "
                "{2}").format(self.mg4j_classpath, self.manifest, self.mg4j_basename)
        execute(args)


    def run_mg4j_queries(self):
        args = ("java -cp {0} "
                "org.bitfunnel.reproducibility.QueryLogRunner "
                "-t {1} {2} {3} {4}").format(self.mg4j_classpath,
                                             self.thread_count,
                                             self.mg4j_basename,
                                             self.filtered_query_file,
                                             self.mg4j_results_file)
        execute(args)


    def build_pef_collection(self):
        if (self.queries is None):
            args = ("java -cp {0} "
                    "org.bitfunnel.reproducibility.IndexExporter "
                    "{1} {2} --index").format(self.mg4j_classpath, self.mg4j_basename, self.pef_index_path);
        else:
            args = ("java -cp {0} "
                    "org.bitfunnel.reproducibility.IndexExporter "
                    "{1} {2} --index "
                    "--queries {3}").format(self.mg4j_classpath, self.mg4j_basename, self.pef_index_path, self.queries);
        execute(args)


    def build_pef_index(self):
        args = ("{0} {1} {2} {3}").format(self.pef_creator,
                                          self.pef_index_type,
                                          self.pef_collection,
                                          self.pef_index_file)
        execute(args)


    def pef_index_from_mg4j_index(params):
        params.build_pef_collection()
        params.build_pef_index()


    def run_pef_queries(self):
        args = ("{0}{1} {2} {3} {4} {5}").format(self.pef_runner,
                                               self.pef_index_type,
                                               self.pef_index_file,
                                               self.pef_query_file,
                                               self.thread_count,
                                               self.pef_results_file)
        execute(args)


    def build_bf_index(self):
        # Run statistics builder
        args = ("{0} statistics {1} {2}").format(self.bf_executable,
                                             self.manifest,
                                             self.bf_index_path)
        execute(args)

        # Run termtable builder
        # TODO: don't hard code density.
        # TODO: don't hard code Optimal.
        # TODO: don't hard code SNR.
        args = ("{0} termtable {1} 0.1 Optimal").format(self.bf_executable,
                                                        self.bf_index_path)
        execute(args)


    def run_bf_queries(self):
        # We're currently restricted to a single shard,
        # so create an empty ShardDefinition file.
        # TODO: reinstate following line.
        # open(self.bf_shard_definition, "w").close()

        # Create script file
        # TODO: reinstate following lines.
        # with open(self.bf_repl_script, "w") as file:
        file = sys.stdout
        for i in range(0,1):
            file.write("load manifest {0}\n".format(self.manifest));
            file.write("compiler\n");
            for t in range(1, self.thread_count + 1):
                results_dir = os.path.join(self.bf_index_path, "results-{0}".format(t))
                if not os.path.exists(results_dir):
                    print("mkdir " + results_dir)
                    # os.makedirs(results_dir)
                file.write("threads {0}\n".format(t));
                file.write("cd {0}".format(results_dir))
                file.write("query log {0}\n".format(self.filtered_query_file));
                file.write("\n")

        # Start BitFunnel repl
        args = ("{0} repl {1}").format(self.bf_executable,
                                       self.bf_index_path)
        execute(args)


    def build_lucene_index(self):
        print("TODO: Implement build_lucene_index")


    def run_lucene_queries(self):
        print("TODO: Implement run_lucene_queries")


def build_chunk_manifest(chunk_root, pattern, manifest_file):
    regex = re.compile(pattern)
    chunks = [os.path.join(chunk_root, f)
              for root, dirs, files in os.walk(chunk_root)
              for f in files
              if regex.search(f) is not None]

    for chunk in chunks:
        print(chunk)

    with open(manifest_file, 'w') as file:
        for chunk in chunks:
            file.write(chunk + '\n')


experiment = Experiment(
    r"D:\git\BitFunnel\build-msvc\tools\BitFunnel\src\Release\BitFunnel.exe",
    r"D:\git\mg4j-workbook",
    r"/home/mhop/git/partitioned_elias_fano/bin",
    r"/data/bitfunnel",
    r"/data/mg4j",
    r"/data/pef",
    r"c:\temp\foobar.txt",
    r"D:\git\mg4j-workbench\data\trec-terabyte\06.efficiency_topics.all"
)

experiment.build_mg4j_index()
experiment.run_mg4j_queries()

experiment.pef_index_from_mg4j_index()
experiment.run_pef_queries()

experiment.build_bf_index()
experiment.run_bf_queries()

experiment.build_lucene_index()
experiment.run_lucene_queries()



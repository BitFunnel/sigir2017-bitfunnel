import os
import re
from bf_utilities import run


class Params:
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
        self.mg4j_classpath = os.path.join(self.mg4j_repo, "target", "mg4j-1.0-SNAPSHOT-jar-with-dependencies.jar")
        self.pef_executable = pef_executables

        self.thread_count = 8
        self.pef_index_type = 'opt'

        self.bf_index_path = bf_index_path
        self.mg4j_index_path = mg4j_index_path
        self.pef_index_path = pef_index_path

        self.manifest = manifest
        self.queries = queries;

        self.basename = os.path.basename(self.manifest).split('.')[0];
        self.mg4j_basename = os.path.join(self.mg4j_index_path, self.basename)
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

        print(args)
        print()


    def run_mg4j_queries(self):
        args = ("java -cp {0} "
                "org.bitfunnel.reproducibility.QueryLogRunner "
                "-t {1} {2} {3} {4}").format(self.mg4j_classpath,
                                             self.thread_count,
                                             self.mg4j_basename,
                                             self.filtered_query_file,
                                             self.mg4j_results_file)

        print(args)
        print()


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

        print(args)
        print()


    def build_pef_index(self):
        args = ("{0} {1} {2} {3}").format(self.pef_creator,
                                          self.pef_index_type,
                                          self.pef_collection,
                                          self.pef_index_file)

        print(args)
        print()


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

        print(args)
        print()


    def build_bf_index(self):
        # Run statistics builder
        # Run termtable builder


    def run_bf_queries(self):
        # Create script file
        # Create ShardDefinition.csv
        # Create config directory
        # Start BitFunnel repl

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


params = Params(
    r"D:\git\BitFunnel\build-msvc\tools\BitFunnel\src\Release\BitFunnel.exe",
    r"D:\git\mg4j-workbook",
    r"/home/mhop/git/partitioned_elias_fano/bin",
    r"/data/bitfunnel",
    r"/data/mg4j",
    r"/data/pef",
    r"c:\temp\foobar.txt",
    r"D:\git\mg4j-workbench\data\trec-terabyte\06.efficiency_topics.all"
)

params.build_mg4j_index()
params.run_mg4j_queries()
params.pef_index_from_mg4j_index()
params.run_pef_queries()


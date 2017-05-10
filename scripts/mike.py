from experiment import Experiment

###########################################################################
#
# Experiments
#
###########################################################################

experiment_windows_273_150_100 = Experiment(
    # Paths to tools
    r"D:\git\BitFunnel\build-msvc\tools\BitFunnel\src\Release\BitFunnel.exe",
    r"D:\git\mg4j-workbench",
    r"/home/mhop/git/partitioned_elias_fano/bin",

    # The directory containing all indexes and the basename for this index
    r"D:\temp\indexes",
    r"273-150-100",

    # The directory with the gov2 chunks and the regular expression pattern
    # used to determine which chunks will be used for this experiment.
    r"d:\sigir\chunks-100-150",
    r"GX.*",  # Use all chunks

    # The query log to be used for this experiment.
    r"D:\sigir\queries\06.efficiency_topics.all",

    # Min and max thread counts
    8,
    1,
    8
)

experiment_windows_273_128_255 = Experiment(
    # Paths to tools
    r"D:\git\BitFunnel\build-msvc\tools\BitFunnel\src\Release\BitFunnel.exe",
    r"D:\git\mg4j-workbench",
    r"/home/mhop/git/partitioned_elias_fano/bin",

    # The directory containing all indexes and the basename for this index
    r"D:\temp\indexes",
    r"273_128_255",

    # The directory with the gov2 chunks and the regular expression pattern
    # used to determine which chunks will be used for this experiment.
    r"d:\sigir\chunks-128-255",
    r"GX.*",  # Use all chunks

    # The query log to be used for this experiment.
    r"D:\sigir\queries\06.efficiency_topics.all",

    # Min and max thread counts
    8,
    1,
    8
)

experiment_windows_273_1000_1500 = Experiment(
    # Paths to tools
    r"D:\git\BitFunnel\build-msvc\tools\BitFunnel\src\Release\BitFunnel.exe",
    r"D:\git\mg4j-workbench",
    r"/home/mhop/git/partitioned_elias_fano/bin",

    # The directory containing all indexes and the basename for this index
    r"D:\temp\indexes",
    r"273-1000-1500",

    # The directory with the gov2 chunks and the regular expression pattern
    # used to determine which chunks will be used for this experiment.
    r"d:\sigir\chunks-1000-1500",
    r"GX.*",  # Use all chunks

    # The query log to be used for this experiment.
    r"D:\sigir\queries\06.efficiency_topics.all",

    # Min and max thread counts
    8,
    1,
    8
)

experiment_windows_273_1024_2047 = Experiment(
    # Paths to tools
    r"D:\git\BitFunnel\build-msvc\tools\BitFunnel\src\Release\BitFunnel.exe",
    r"D:\git\mg4j-workbench",
    r"/home/mhop/git/partitioned_elias_fano/bin",

    # The directory containing all indexes and the basename for this index
    r"D:\temp\indexes",
    r"273-1024-2047",

    # The directory with the gov2 chunks and the regular expression pattern
    # used to determine which chunks will be used for this experiment.
    r"d:\sigir\chunks-1024-2047",
    r"GX.*",  # Use all chunks

    # The query log to be used for this experiment.
    r"D:\sigir\queries\06.efficiency_topics.all",

    # Min and max thread counts
    8,
    1,
    8
)


experiment_linux_273_1024_2047 = Experiment(
    # Paths to tools
    r"/home/mhop/git/BitFunnel/build-make/tools/BitFunnel/src/BitFunnel",
    r"/home/mhop/git/mg4j-workbench",
    r"/home/mhop/git/partitioned_elias_fano/bin",

    # The directory containing all indexes and the basename for this index
    r"/mnt/d/temp/indexes",
    r"273-1024-2047",

    # The directory with the gov2 chunks and the regular expression pattern
    # used to determine which chunks will be used for this experiment.
    r"/mnt/d/sigir/chunks-100-150",
    r"GX.*",  # Use all chunks

    # The query log to be used for this experiment.
    r"/home/mhop/git/mg4j-workbench/data/trec-terabyte/06.efficiency_topics.all",

    # Min and max thread counts
    1,
    8
)


experiment_linux = Experiment(
    # Paths to tools
    r"/home/mhop/git/BitFunnel/build-make/tools/BitFunnel/src/BitFunnel",
    r"/home/mhop/git/mg4j-workbench",
    r"/home/mhop/git/partitioned_elias_fano/bin",

    # The directory containing all indexes and the basename for this index
    r"/mnt/d/temp/indexes",
    r"273-150-100",

    # The directory with the gov2 chunks and the regular expression pattern
    # used to determine which chunks will be used for this experiment.
    r"/mnt/d/sigir/chunks-100-150",
    r"GX000.*",  # Use all chunks

    # The query log to be used for this experiment.
    r"/home/mhop/git/mg4j-workbench/data/trec-terabyte/06.efficiency_topics.all",

    # Min and max thread counts
    8,
    1,
    8
)


def runxxx(experiment):
    # experiment.fix_query_log()
    # experiment.build_chunk_manifest()
    #
    # # Must build the mg4j index before filtering the query log
    # # Must also build mg4j before building PEF which takes the MG4J export
    # # as input.
    # experiment.build_mg4j_index()
    #
    # # Build the other indexes at this point
    # experiment.build_bf_index()
    # experiment.build_lucene_index()
    # experiment.build_pef_collection()
    # experiment.build_pef_index()
    #
    # # Must filter the query log before running any queries.
    # experiment.filter_query_log()
    #
    # # Now we're ready to run queries.
    #
    # experiment.run_bf_queries()
    # experiment.run_lucene_queries()
    # experiment.run_mg4j_queries()
    # experiment.run_pef_queries()

    experiment.summarize(7)
    print()

# runxxx(experiment_windows_273_128_255)
# runxxx(experiment_windows_273_150_100)
# runxxx(experiment_windows_273_1000_1500)
# runxxx(experiment_windows_273_1024_2047)
# runxxx(experiment_linux_273_1024_2047)
# latex_corpora([
#     experiment_windows_273_150_100.analyze_bf_corpus(273, 100, 150),
#     experiment_windows_273_128_255.analyze_bf_corpus(273, 128, 255),
#     experiment_windows_273_1024_2047.analyze_bf_corpus(273, 1024, 2047)])

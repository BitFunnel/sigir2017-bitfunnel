from build_filtered_chunks import process_chunk_list
from experiment import Experiment
from innovations import measure_innovations, analyze_innovations
from latex import latex_corpora, latex_performance


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
    100,
    150,
    r"273-150-100",

    # The directory with the gov2 chunks and the regular expression pattern
    # used to determine which chunks will be used for this experiment.
    r"d:\sigir\chunks-100-150",
    r"GX.*",  # Use all chunks

    # The query log to be used for this experiment.
    r"D:\sigir\queries\06.efficiency_topics.all",

    # BitFunnel density
    0.15,

    # Min and max thread counts
    8,
    1,
    8
)


experiment_windows_273_64_127 = Experiment(
    # Paths to tools
    r"D:\git\BitFunnel\build-msvc\tools\BitFunnel\src\Release\BitFunnel.exe",
    r"D:\git\mg4j-workbench",
    r"/home/mhop/git/partitioned_elias_fano/bin",

    # The directory containing all indexes and the basename for this index
    r"D:\temp\indexes",
    64,
    127,
    r"273-64-127",

    # The directory with the gov2 chunks and the regular expression pattern
    # used to determine which chunks will be used for this experiment.
    r"d:\sigir\chunks-64-127",
    r"GX.*",  # Use all chunks

    # The query log to be used for this experiment.
    r"D:\sigir\queries\06.efficiency_topics.all",

    # BitFunnel density
    0.15,

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
    128,
    255,
    r"273_128_255",

    # The directory with the gov2 chunks and the regular expression pattern
    # used to determine which chunks will be used for this experiment.
    r"d:\sigir\chunks-128-255",
    r"GX.*",  # Use all chunks

    # The query log to be used for this experiment.
    r"D:\sigir\queries\06.efficiency_topics.all",

    # BitFunnel density
    0.15,

    # Min and max thread counts
    8,
    1,
    8
)


experiment_windows_273_256_511 = Experiment(
    # Paths to tools
    r"D:\git\BitFunnel\build-msvc\tools\BitFunnel\src\Release\BitFunnel.exe",
    r"D:\git\mg4j-workbench",
    r"/home/mhop/git/partitioned_elias_fano/bin",

    # The directory containing all indexes and the basename for this index
    r"D:\temp\indexes",
    256,
    511,
    r"273-256-511",

    # The directory with the gov2 chunks and the regular expression pattern
    # used to determine which chunks will be used for this experiment.
    r"d:\sigir\chunks-256-511",
    r"GX.*",  # Use all chunks

    # The query log to be used for this experiment.
    r"D:\sigir\queries\06.efficiency_topics.all",

    # BitFunnel density
    0.15,

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
    1000,
    1500,
    r"273-1000-1500",

    # The directory with the gov2 chunks and the regular expression pattern
    # used to determine which chunks will be used for this experiment.
    r"d:\sigir\chunks-1000-1500",
    r"GX.*",  # Use all chunks

    # The query log to be used for this experiment.
    r"D:\sigir\queries\06.efficiency_topics.all",

    # BitFunnel density
    0.15,

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
    1024,
    2047,
    r"273-1024-2047",

    # The directory with the gov2 chunks and the regular expression pattern
    # used to determine which chunks will be used for this experiment.
    r"d:\sigir\chunks-1024-2047",
    r"GX.*",  # Use all chunks

    # The query log to be used for this experiment.
    r"D:\sigir\queries\06.efficiency_topics.all",

    # BitFunnel density
    0.15,

    # Min and max thread counts
    8,
    1,
    8
)


experiment_windows_273_2048_4095 = Experiment(
    # Paths to tools
    r"D:\git\BitFunnel\build-msvc\tools\BitFunnel\src\Release\BitFunnel.exe",
    r"D:\git\mg4j-workbench",
    r"/home/mhop/git/partitioned_elias_fano/bin",

    # The directory containing all indexes and the basename for this index
    r"D:\temp\indexes",
    2048,
    4095,
    r"273-2048-4095",

    # The directory with the gov2 chunks and the regular expression pattern
    # used to determine which chunks will be used for this experiment.
    r"d:\sigir\chunks-2048-4095",
    r"GX.*",  # Use all chunks

    # The query log to be used for this experiment.
    r"D:\sigir\queries\06.efficiency_topics.all",

    # BitFunnel density
    0.15,

    # Min and max thread counts
    8,
    1,
    8
)


experiment_linux_273_64_127 = Experiment(
    # Paths to tools
    r"/home/mhop/git/BitFunnel/build-make/tools/BitFunnel/src/BitFunnel",
    r"/home/mhop/git/mg4j-workbench",
    r"/home/mhop/git/partitioned_elias_fano/bin",

    # The directory containing all indexes and the basename for this index
    r"/mnt/d/temp/indexes",
    64,
    127,
    r"273-64-127",

    # The directory with the gov2 chunks and the regular expression pattern
    # used to determine which chunks will be used for this experiment.
    r"/mnt/d/sigir/chunks-64-127",
    r"GX.*",  # Use all chunks

    # The query log to be used for this experiment.
    r"/mnt/d/sigir/queries/06.efficiency_topics.all",

    # BitFunnel density
    0.15,

    # Min and max thread counts
    8,
    1,
    8
)


experiment_linux_273_128_255 = Experiment(
    # Paths to tools
    r"/home/mhop/git/BitFunnel/build-make/tools/BitFunnel/src/BitFunnel",
    r"/home/mhop/git/mg4j-workbench",
    r"/home/mhop/git/partitioned_elias_fano/bin",

    # The directory containing all indexes and the basename for this index
    r"/mnt/d/temp/indexes",
    128,
    255,
    r"273_128_255",

    # The directory with the gov2 chunks and the regular expression pattern
    # used to determine which chunks will be used for this experiment.
    r"/mnt/d/sigir/chunks-128-255",
    r"GX.*",  # Use all chunks

    # The query log to be used for this experiment.
    r"/mnt/d/sigir/queries/06.efficiency_topics.all",

    # BitFunnel density
    0.15,

    # Min and max thread counts
    8,
    1,
    8
)


experiment_linux_273_256_511 = Experiment(
    # Paths to tools
    r"/home/mhop/git/BitFunnel/build-make/tools/BitFunnel/src/BitFunnel",
    r"/home/mhop/git/mg4j-workbench",
    r"/home/mhop/git/partitioned_elias_fano/bin",

    # The directory containing all indexes and the basename for this index
    r"/mnt/d/temp/indexes",
    256,
    511,
    r"273-256-511",

    # The directory with the gov2 chunks and the regular expression pattern
    # used to determine which chunks will be used for this experiment.
    r"/mnt/d/sigir/chunks-256-511",
    r"GX.*",  # Use all chunks

    # The query log to be used for this experiment.
    r"/mnt/d/sigir/queries/06.efficiency_topics.all",

    # BitFunnel density
    0.15,

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
    1024,
    2047,
    r"273-1024-2047",

    # The directory with the gov2 chunks and the regular expression pattern
    # used to determine which chunks will be used for this experiment.
    r"/mnt/d/sigir/chunks-100-150",
    r"GX.*",  # Use all chunks

    # The query log to be used for this experiment.
    r"/mnt/d/sigir/queries/06.efficiency_topics.all",

    # BitFunnel density
    0.15,

    # Min and max thread counts
    8,
    1,
    8
)


experiment_linux_273_2048_4095 = Experiment(
    # Paths to tools
    r"/home/mhop/git/BitFunnel/build-make/tools/BitFunnel/src/BitFunnel",
    r"/home/mhop/git/mg4j-workbench",
    r"/home/mhop/git/partitioned_elias_fano/bin",

    # The directory containing all indexes and the basename for this index
    r"/mnt/d/temp/indexes",
    2048,
    4095,
    r"273-2048-4095",

    # The directory with the gov2 chunks and the regular expression pattern
    # used to determine which chunks will be used for this experiment.
    r"/mnt/d/sigir/chunks-2048-4095",
    r"GX.*",  # Use all chunks

    # The query log to be used for this experiment.
    r"/mnt/d/sigir/queries/06.efficiency_topics.all",

    # BitFunnel density
    0.15,

    # Min and max thread counts
    8,
    1,
    8
)


def runxxx(experiment):
    pass
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
    # # # experiment.build_pef_index()
    # #
    # # Must filter the query log before running any queries.
    # experiment.filter_query_log()
    #
    # # Now we're ready to run queries.
    #
    # experiment.run_bf_queries()
    # experiment.run_lucene_queries()
    # experiment.run_mg4j_queries()
    # # experiment.run_pef_queries()

    # experiment.summarize(7)
    # print()


def run_windows(experiment):
    experiment.run_bf_queries()
    experiment.run_lucene_queries()
    experiment.run_mg4j_queries()

def run_linux(experiment):
    experiment.run_pef_queries()


def linux(experiment):
    experiment.build_pef_index()
    experiment.run_pef_queries()


def finish(experiment):
    experiment.summarize(7)


process_chunk_list(r"d:\data\gov2",
                   "*",
                   r"d:\temp\chunks",
                   r"D:\git\mg4j-workbench",
                   r"D:\git\BitFunnel\build-msvc\tools\BitFunnel\src\Release\BitFunnel.exe",
                   0,
                   100000,
                   8)

# process_chunk_list(r"d:\data\gov2",
#                    r"d:\temp\chunks",
#                    r"D:\git\mg4j-workbench",
#                    r"D:\git\BitFunnel\build-msvc\tools\BitFunnel\src\Release\BitFunnel.exe",
#                    64,
#                    127,
#                    8)

# process_chunk_list(r"d:\data\gov2",
#                    r"d:\temp\chunks",
#                    r"D:\git\mg4j-workbench",
#                    r"D:\git\BitFunnel\build-msvc\tools\BitFunnel\src\Release\BitFunnel.exe",
#                    512,
#                    1023,
#                    8)


# process_chunk_list(r"d:\data\gov2",
#                    r"d:\temp\chunks",
#                    r"D:\git\mg4j-workbench",
#                    r"D:\git\BitFunnel\build-msvc\tools\BitFunnel\src\Release\BitFunnel.exe",
#                    2048,
#                    4095,
#                    7)


# process_chunk_list(r"d:\data\gov2",
#                    r"d:\temp\chunks",
#                    r"D:\git\mg4j-workbench",
#                    r"D:\git\BitFunnel\build-msvc\tools\BitFunnel\src\Release\BitFunnel.exe",
#                    1024,
#                    2047,
#                    7)


# process_chunk_list(r"/home/danluu/dev/gov2",
#                    r"/home/danluu/dev/what-is-this",
#                    r"/home/danluu/dev/mg4j-workbench",
#                    r"/home/danluu/dev/BitFunnel/build-ninja/tools/BitFunnel/src/BitFunnel",
#                    128,
#                    255,
#                    7)

# runxxx(experiment_windows_273_64_127)

# runxxx(experiment_windows_273_128_255)
# runxxx(experiment_windows_273_150_100)
# runxxx(experiment_windows_273_1000_1500)
# runxxx(experiment_windows_273_1024_2047)
# runxxx(experiment_linux_273_1024_2047)

# runxxx(experiment_windows_273_256_511)
# linux(experiment_linux_273_256_511)

# runxxx(experiment_windows_273_2048_4095)
# linux(experiment_linux_273_2048_4095)
# finish(experiment_windows_273_2048_4095)

# print()

# runxxx(experiment_windows_273_64_127)
# linux(experiment_linux_273_64_127)
# experiment_windows_273_64_127.run_lucene_queries()
# finish(experiment_windows_273_64_127)


def run_innovations(experiments):
    labels = ["BSS", "BSS-FC", "BTFNL"]
    treatments = ["ClassicBitsliced", "PrivateSharedRank0", "Optimal"]
    densities = [0.05, 0.10, 0.15, 0.20, 0.25, 0.3, 0.35]

    # for experiment in experiments:
    #     measure_innovations(experiment, treatments, densities)

    for experiment in experiments:
        analyze_innovations(experiment, labels, treatments, densities)


experiments = [
    experiment_windows_273_64_127,
    experiment_windows_273_128_255,
    experiment_windows_273_256_511,
    experiment_windows_273_1024_2047,
    experiment_windows_273_2048_4095]

# latex_corpora(experiments)
# latex_performance(experiments)

# run_innovations(experiments)


# run_windows(experiment_windows_273_64_127)
# run_windows(experiment_windows_273_128_255)
# run_windows(experiment_windows_273_1024_2047)
# run_windows(experiment_windows_273_2048_4095)

# run_linux(experiment_linux_273_64_127)
# run_linux(experiment_linux_273_128_255)
# run_linux(experiment_linux_273_1024_2047)
# run_linux(experiment_linux_273_2048_4095)


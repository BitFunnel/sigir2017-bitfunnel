from build_filtered_chunks import process_chunk_list
from experiment import Experiment
from latex import latex_corpora, latex_performance
import math


###########################################################################
#
# Experiments
#
###########################################################################

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

    # Min and max thread counts
    8,
    1,
    8
)


experiments = [ experiment_linux_273_64_127,
                experiment_linux_273_128_255,
                experiment_linux_273_1024_2047,
                experiment_linux_273_2048_4095]

def go(experiments):
    # print("Building Lucene indexes . . .")
    # for experiment in experiments:
    #     experiment.build_lucene_index()

    # print("Running experiments . . .")
    # for experiment in experiments:
    #     experiment.run_bf_queries()
    #     experiment.run_lucene_queries()
    #     experiment.run_mg4j_queries()
    #     experiment.run_pef_queries()

go(experiments)
# latex_corpora(experiments)
# latex_performance(experiments)

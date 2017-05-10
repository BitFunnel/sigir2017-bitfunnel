from experiment import Experiment

###########################################################################
#
# Experiments
#
###########################################################################

experiment_dl_linux = Experiment(
    # Paths to tools
    r"/home/danluu/dev/BitFunnel/build-ninja/tools/BitFunnel/src/BitFunnel",
    r"/home/danluu/dev/mg4j-workbench",
    r"/home/danluu/dev/partitioned_elias_fano/bin",

    # The directory containing all indexes and the basename for this index
    r"/home/danluu/dev/what-is-this",
    # r"273-128-255",
    r"273-2048-4095",

    # The directory with the gov2 chunks and the regular expression pattern
    # used to determine which chunks will be used for this experiment.
    r"/home/danluu/dev/gov2-2048-4095/chunks",
    r"GX000.*",

    # The query log to be used for this experiment.
    r"/home/danluu/Downloads/06.efficiency_topics.all",

    # Min and max thread counts
    8,
    1,
    8
)


runxxx(experiment_dl_linux)



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
    # 128,
    # 255,
    # r"273-128-255",
    2048,
    4095,
    r"273-2048-4095",

    # The directory with the gov2 chunks and the regular expression pattern
    # used to determine which chunks will be used for this experiment.
    r"/home/danluu/dev/gov2-2048-4095/chunks",
    r"GX000.*",

    # The query log to be used for this experiment.
    r"/home/danluu/Downloads/06.efficiency_topics.all",

    # BitFunnel density
    0.15,

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


runxxx(experiment_dl_linux)



from build_filtered_chunks import process_chunk_list
from experiment import Experiment

###########################################################################
#
# Experiments
#
###########################################################################
experiment_windows_273_64_127 = Experiment(
    # Paths to tools
    r"D:\git\BitFunnel\build-msvc\tools\BitFunnel\src\Release\BitFunnel.exe",
    r"D:\git\mg4j-workbench",
    r"/home/mhop/git/partitioned_elias_fano/bin",

    # The directory containing all indexes and the basename for this index
    r"D:\temp\e2e\indexes",
    64,
    127,
    r"273-64-127",

    # The directory with the gov2 chunks and the regular expression pattern
    # used to determine which chunks will be used for this experiment.
    # r"d:\sigir\chunks-64-127",
    r"d:\temp\e2e\chunks\chunks",
    r"GX.*",  # Use all chunks

    # The query log to be used for this experiment.
    r"D:\sigir\queries\06.efficiency_topics.all",

    # BitFunnel density
    0.15,

    # Min and max thread counts
    8,
    1,
    8,
    # New parameter specifies BitFunnel buffer size in KiB.
    # The 64-127 shard of documents from all 273 gov2 directories
    # can be loaded with a 10GiB buffer. Note that the buffer
    # size must be less than the physical memory size of the
    # machine.
    10000000
)



def runxxx(experiment):
    # process_chunk_list(r"d:\data\gov2",
    #                    "GX00[0|1]",
    #                    r"d:\temp\e2e\chunks",
    #                    r"D:\git\mg4j-workbench",
    #                    r"D:\git\BitFunnel\build-msvc\tools\BitFunnel\src\Release\BitFunnel.exe",
    #                    64,
    #                    127,
    #                    8)

    experiment.fix_query_log()
    experiment.build_chunk_manifest()

    #
    # # Must build the mg4j index before filtering the query log
    # # Must also build mg4j before building PEF which takes the MG4J export
    # # as input.
    # experiment.build_mg4j_index()
    #
    # # Build the other indexes at this point

    experiment.build_bf_index()

    # experiment.build_lucene_index()
    # experiment.build_pef_collection()
    # # # experiment.build_pef_index()
    # #
    # # Must filter the query log before running any queries.
    # experiment.filter_query_log()

    ###############################################
    # Didn't want to take the time to use MG4J to
    # filter the query log. For now, just pretend
    # to filter by copying the log.
    ###############################################
    experiment.simulate_filter_query_log()

    #
    # # Now we're ready to run queries.
    #
    experiment.run_bf_queries()
    # experiment.run_lucene_queries()
    # experiment.run_mg4j_queries()
    # # experiment.run_pef_queries()

    # experiment.summarize(7)
    # print()

runxxx(experiment_windows_273_64_127)

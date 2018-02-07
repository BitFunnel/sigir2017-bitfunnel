from build_filtered_chunks import process_chunk_list

process_chunk_list(r"d:\data\gov2",
                   "GX00.",             # TEMPORARY - filter to first 10 .7z files.
                   r"d:\temp\chunks",
                   r"D:\git\mg4j-workbench",
                   r"D:\git\BitFunnel\build-msvc\tools\BitFunnel\src\Release\BitFunnel.exe",
                   None, # 0,
                   None, # 100000,
                   8)

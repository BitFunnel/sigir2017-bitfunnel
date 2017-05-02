import os
import re
from bf_utilities import run


class Mg4jIndexFromChunks:
    def __init__(self, mg4j, chunk_dir, chunk_pattern, root, index_name):
        self.chunk_dir = chunk_dir
        self.chunk_pattern = chunk_pattern
        self.root = root
        self.index_name = index_name
        self.base_name = os.path.join(root, index_name)

        self.classpath = os.path.join(mg4j, "target", "mg4j-1.0-SNAPSHOT-jar-with-dependencies.jar")
        self.manifest = os.path.join(self.root, "manifest.txt")


    def build_manifest(self):
        regex = re.compile(self.chunk_pattern)
        chunks = [os.path.join(root, f)
                  for root, dirs, files in os.walk(self.chunk_dir)
                  for f in files
                  if regex.search(f) is not None]

        for chunk in chunks:
            print(chunk)

        with open(self.manifest, 'w') as file:
            for chunk in chunks:
                file.write(chunk + '\n')



    def build_index(self):
        args = ("java -cp {0} "
                "it.unimi.di.big.mg4j.tool.IndexBuilder "
                "-o org.bitfunnel.reproducibility.ChunkManifestDocumentSequence({1}) "
                "{2}").format(self.classpath, self.manifest, self.base_name)

        print(args)

        run(args, self.root);


    def go(self):
        if not os.path.exists(self.root):
            print("mkdir " + self.root)
            os.makedirs(self.root)

        self.build_manifest()
        self.build_index()


mg4j_index_builder = Mg4jIndexFromChunks(
    r"D:\git\mg4j-workbench",
    r"D:\sigir\chunks",
    r"GX00.*",
    r"D:\temp\mg4jIndex",
    r"tenChunks"
)

mg4j_index_builder.go();

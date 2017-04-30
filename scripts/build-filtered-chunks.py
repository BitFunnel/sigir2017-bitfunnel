import errno
import os
import shutil
import stat
import subprocess


def run(args, working_directory):
    proc = subprocess.Popen(args, cwd=working_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True);
    for line in proc.stdout:
        print(line.decode(), end='')
    proc.stdout.close()
    returncode = proc.wait()

    # Ensure we don't get zombie processes. This had been a problem with the 7z decompression.
    del proc


class Builder:
    def __init__(self, gov2, root, mg4j, bitfunnel, min_postings, max_postings):
        self.gov2 = gov2
        self.root = root
        self.mg4j = mg4j
        self.bitfunnel = bitfunnel
        self.min_postings = min_postings
        self.max_postings = max_postings

        # Use a slightly unusual temp file name to protect against accidental
        # deletions of other directories with the same name.
        self.temp = os.path.join(root, "tempxxx");
        self.chunkdir = os.path.join(root, "chunks")
        self.classpath = os.path.join(self.mg4j, "target", "mg4j-1.0-SNAPSHOT-jar-with-dependencies.jar")

        if not os.path.exists(self.chunkdir):
            print("mkdir " + self.chunkdir)
            os.makedirs(self.chunkdir)


    def make_temp_dir(self):
        if not os.path.exists(self.temp):
            print("mkdir " + self.temp)
            os.makedirs(self.temp)


    def decompress(self, chunk):
        input = os.path.join(self.gov2, chunk + ".7z");

        args = ("7z x {0}").format(input);
        print(args)

        run(args, self.temp);


    def build_collection(self, chunk):
        input = os.path.join(self.temp, chunk)
        bundles = [os.path.join(self.temp, chunk, f) for f in os.listdir(input) if
                   os.path.isfile(os.path.join(input, f)) and f.endswith('.txt')]
        print("  Creating mg4j collection from " + input)

        input = os.path.join(self.temp, chunk, "*.txt")
        output = os.path.join(self.temp, chunk + ".collection")
        args = ("dir /s/b {0} | "
                "java -cp {1} "
                "it.unimi.di.big.mg4j.document.TRECDocumentCollection "
                "-f HtmlDocumentFactory "
                "-p encoding=iso-8859-1 "
                "{2}").format(input, self.classpath, output);

        print(args)

        run(args, self.temp);


    def create_chunk(self, chunk):
        input = os.path.join(self.temp, chunk + ".collection")
        output = os.path.join(self.temp, chunk + ".chunk")

        args = ("java -cp {0} "
                "org.bitfunnel.reproducibility.GenerateBitFunnelChunks "
                "-S {1} {2}").format(self.classpath, input, output)

        print(args)

        run(args, self.temp);


    def create_chunk_manifest(self, chunk):
        # Create the manifest file
        input = os.path.join(self.temp, chunk + ".chunk")
        output = os.path.join(self.temp, "manifest.txt")
        with open(output, 'w') as file:
            file.write(input + '\n')


    def create_filtered_chunk(self, chunk):
        manifest = os.path.join(self.temp, "manifest.txt")
        args = ("{0} filter {1} {2} -size {3} {4}").format(
            self.bitfunnel, manifest, self.chunkdir, self.min_postings, self.max_postings)
        print(args)

        run(args, self.temp);


    def rename_filtered_chunk(self, chunk):
        old_name = os.path.join(self.chunkdir, "Chunk-0.chunk")
        new_name = os.path.join(self.chunkdir, "{0}-{1}-{2}.chunk".format(chunk, self.min_postings, self.max_postings))
        os.rename(old_name, new_name)


    def cleanup(self):
        print("Cleaning up")
        if os.path.exists(self.temp):
            if (self.temp.endswith("tempxxx")):
                def handleRemoveReadonly(func, path, exc):
                    excvalue = exc[1]
                    if excvalue.errno == errno.EACCES:
                        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
                        func(path)
                    else:
                        raise

                shutil.rmtree(self.temp, ignore_errors=False, onerror=handleRemoveReadonly)


    def process_one_chunk(self, chunk):
        print("Building chunk " + chunk)
        self.make_temp_dir()
        self.decompress(chunk)
        self.build_collection(chunk)
        self.create_chunk(chunk)
        self.create_chunk_manifest(chunk)
        self.create_filtered_chunk(chunk)
        self.rename_filtered_chunk(chunk)
        self.cleanup()


    def go(self):
        basenames = [os.path.splitext(f)[0] for f in os.listdir(self.gov2) if os.path.isfile(os.path.join(self.gov2, f)) and f.endswith('.7z')]

        self.cleanup()

        for chunk in basenames:
            self.process_one_chunk(chunk)

builder = Builder(r"d:\data\gov2",
                  r"d:\temp",
#                  r"d:\sigir",
                  r"D:\git\mg4j-workbench",
                  r"D:\git\BitFunnel\build-msvc\tools\BitFunnel\src\Release\BitFunnel.exe",
                  100,
                  150);
builder.go();

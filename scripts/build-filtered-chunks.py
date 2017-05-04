import errno
import os
import platform
import queue
import shutil
import stat
import threading
from bf_utilities import run


class Builder:
    def __init__(self, gov2, root, mg4j, bitfunnel, min_postings, max_postings, thread_id):
        self.gov2 = gov2
        self.root = root
        self.mg4j = mg4j
        self.bitfunnel = bitfunnel
        self.min_postings = min_postings
        self.max_postings = max_postings
        self.thread_id = thread_id

        # Use a slightly unusual temp file name to protect against accidental
        # deletions of other directories with the same name.
        # TODO: consider whether the tempfile module would be useful here.
        # We don't really have a problem generating unique names since they are all
        # under root. The main concern is preventing accidental deletions of important
        # directories because of bugs relating to paths or incorrect command-line
        # arguments.
        self.temp = os.path.join(root, "tempxxx-{0}".format(self.thread_id));
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
        if (platform.system() == 'Windows'):
            command = "dir /s/b"
        else:
            # This command is meaningless and might as well be ls when used this way.
            command = "find "
        args = ("{0} {1} | "
                "java -cp {2} "
                "it.unimi.di.big.mg4j.document.TRECDocumentCollection "
                "-f HtmlDocumentFactory "
                "-p encoding=iso-8859-1 "
                "{3}").format(command, input, self.classpath, output);

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
        output = os.path.join(self.temp, "Manifest.txt")
        with open(output, 'w') as file:
            file.write(input + '\n')


    def create_filtered_chunk(self, chunk):
        manifest = os.path.join(self.temp, "Manifest.txt")
        args = ("{0} filter {1} {2} -size {3} {4}").format(
            self.bitfunnel, manifest, self.temp, self.min_postings, self.max_postings)
        print(args)

        run(args, self.temp);


    def rename_filtered_chunk(self, chunk):
        old_name = os.path.join(self.temp, "Chunk-0.chunk")
        new_name = os.path.join(self.chunkdir, "{0}-{1}-{2}.chunk".format(chunk, self.min_postings, self.max_postings))
        os.rename(old_name, new_name)


    def cleanup(self):
        print("Cleaning up")
        if os.path.exists(self.temp):
            # The check for "tempxxx" is to guard against bugs with path operations
            # and command-line arguments which might lead to the accidental deletion
            # of an important directory.
            if "tempxxx" in self.temp:
                def handleRemoveReadonly(func, path, exc):
                    excvalue = exc[1]
                    if excvalue.errno == errno.EACCES:
                        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
                        func(path)
                    else:
                        raise

                print("rmtree {0}".format(self.temp));
                shutil.rmtree(self.temp, ignore_errors=False, onerror=handleRemoveReadonly)


    def process_one_chunk(self, chunk):
        print("Building chunk " + chunk)

        chunk_name = os.path.join(self.chunkdir, "{0}-{1}-{2}.chunk".format(chunk, self.min_postings, self.max_postings));

        # Only build chunk if it doesn't already exist.
        # This helps with restarting long runs that fail in the middle.
        if (not os.path.exists(chunk_name)):
            self.make_temp_dir()
            self.decompress(chunk)
            self.build_collection(chunk)
            self.create_chunk(chunk)
            self.create_chunk_manifest(chunk)
            self.create_filtered_chunk(chunk)
            self.rename_filtered_chunk(chunk)
            self.cleanup()


    def worker(self, queue):
        while True:
            chunk = queue.get()
            if chunk is None:
                break
            self.process_one_chunk(chunk)
            queue.task_done()

    def go(self):
        basenames = [os.path.splitext(f)[0] for f in os.listdir(self.gov2) if os.path.isfile(os.path.join(self.gov2, f)) and f.endswith('.7z')]

        self.cleanup()

        for chunk in basenames:
            self.process_one_chunk(chunk)


def process_chunk_list(gov2, root, mg4j, bitfunnel, min_postings, max_postings, thread_count):
    q = queue.Queue()

    basenames = [os.path.splitext(f)[0] for f in os.listdir(gov2) if
                 os.path.isfile(os.path.join(gov2, f)) and f.endswith('.7z')]

    print("Processing {0} chunks.".format(len(basenames)))

    for name in basenames:
        q.put(name)

    print("Starting {0} threads.".format(thread_count))

    for thread_id in range(thread_count):
        builder = Builder(gov2, root, mg4j, bitfunnel, min_postings, max_postings, thread_id)
        thread = threading.Thread(target=builder.worker, args = (q, ))
        thread.start()

    q.join()

    print("All threads finished.")


# process_chunk_list(r"d:\data\gov2",
#                    r"d:\temp\multi-threaded",
#                    r"D:\git\mg4j-workbench",
#                    r"D:\git\BitFunnel\build-msvc\tools\BitFunnel\src\Release\BitFunnel.exe",
#                    1000,
#                    1500,
#                    7)


process_chunk_list(r"/home/danluu/dev/gov2",
                   r"/home/danluu/dev/what-is-this",
                   r"/home/danluu/dev/mg4j-workbench",
                   r"/home/danluu/dev/BitFunnel/build-ninja/tools/BitFunnel/src/BitFunnel",
                   128,
                   255,
                   7)
import subprocess

def run(args, working_directory, logfile = None):
    proc = subprocess.Popen(args, cwd=working_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True);

    if logfile is not None:
        with open(logfile, 'w') as log:
            for line in proc.stdout:
                print(line.decode(), end='', file = log)
                print(line.decode(), end='')
            for line in proc.stderr:
                print(line.decode(), end='', file = log)
                print(line.decode(), end='')
    else:
        for line in proc.stdout:
            print(line.decode(), end='')
        for line in proc.stderr:
            print(line.decode(), end='')

    proc.stdout.close()
    returncode = proc.wait()

    # Ensure we don't get zombie processes. This had been a problem with the 7z decompression.
    del proc

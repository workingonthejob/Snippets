import hashlib
import os
import argparse
import sys

'''
Parse the given directory and compare all the files in it and remove the duplicates.
'''
def run(directory):
    md5_list = list()
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            file = os.path.join(root, name)
            md5 = hashlib.md5(open(file, 'rb').read()).hexdigest()
            if md5 in md5_list:
                print("Deleting {}".format(file))
                os.remove(file)
            else:
                md5_list.append(md5)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("{} -h".format(sys.argv[0]))
        sys.exit(0)
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--directory", help="The directory to scan through and parse for duplicates.", required=True)
    parser.add_argument("-l", "--logging", help="Set the log level.")
    args = parser.parse_args()

    run(args.directory)

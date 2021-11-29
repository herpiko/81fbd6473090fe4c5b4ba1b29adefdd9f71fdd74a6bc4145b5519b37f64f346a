#!/usr/bin/env python3

import sys
import os
import hashlib
import codecs
import gc

BUFFER_SIZE = 65536 
TEXTFILES = (
    codecs.BOM_UTF16_BE,
    codecs.BOM_UTF16_LE,
    codecs.BOM_UTF32_BE,
    codecs.BOM_UTF32_LE,
    codecs.BOM_UTF8,
)

def sha256_hash(file_path):
    sha256 = hashlib.sha256()
    is_init = True
    is_binary = True
    data = bytearray()
    try:
    
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(BUFFER_SIZE)
                if not chunk:
                    break
                if is_init:
                        # Find out whether this is a binary or not
                    # by using text bom identifier
                    is_binary = b'\0' in chunk and \
                            not any(chunk.startswith(bom) for bom in TEXTFILES)
                    is_init = False
                data += chunk
                sha256.update(chunk)
    except:
        # This may be a permission related error or missing symlink.
        # Ignore them.
        pass

    hashed = sha256.hexdigest()
    content = ""
    try:
        if is_binary:
            # Printing out the binary content is not cool to look at, 
            # use hash as content/indentifier instead.
            # We can keep the memory footprint small this way.
            content = hashed
        else:
            content = data.decode()
    except:
        # Fallback to hash
        content = hashed 

    # Keep memory clean in case it's a huge file
    del sha256
    del data
    gc.collect()

    return hashed, content

def find_common(target_path):
    hashes = {} # Hash as single source of truth
    contents = {} # Maintain content in separated dict
    for (dirpath, dirnames, filenames) in os.walk(target_path):
        if len(filenames) > 0:
            for filename in filenames:
                hashed, content = sha256_hash(os.path.join(dirpath, filename))
                if hashed in hashes:
                    hashes[hashed] += 1
                else:
                    hashes[hashed] = 1
                if not hashed in contents:
                    contents[hashed] = content

    # Find max
    max_key = max(hashes, key=hashes.get)
    max_val = max(hashes.values())

    # Combine as result
    result = contents[max_key] + " " + str(max_val)
    return result

if __name__ == '__main__':

    if len(sys.argv) < 2:
        raise Exception("Missing path argument")

    target_path = sys.argv[1]

    # In case we are forgot to add ./ for a dir in our current workdir
    if not (target_path.startswith("/") or target_path.startswith(".")):
        target_path = "./" + target_path

    if not os.path.isdir(sys.argv[1]):
        raise Exception("Invalid directory")

    result = find_common(target_path)
    print(result)

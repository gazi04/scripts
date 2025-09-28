import os
import zlib
import glob
from hashlib import sha1

# --- CONFIGURATION ---
# 1. Directory containing ALL the files recovered by PhotoRec. 
#    This should be the parent folder that contains all the 'recup_dir.XXX' subfolders.
#    *** REPLACE THIS WITH YOUR ABSOLUTE PATH ***
srcdir_input = "" 

# 2. Directory for the new, empty Git repository
#    NOTE: You MUST run 'git init' inside this directory first!
#    *** REPLACE THIS WITH YOUR ABSOLUTE PATH ***
dstdir_input = "" 
# ---------------------

# Convert input paths to absolute paths for reliability
srcdir = os.path.abspath(os.path.expanduser(srcdir_input))
dstdir = os.path.abspath(os.path.expanduser(dstdir_input))
git_objects_path = os.path.join(dstdir, '.git', 'objects')


def check_and_save_git_object(filename):
    """
    Tries to decompress a file, validate it as a Git object, 
    and save it in the correct hash-based path.
    """
    if not os.path.isfile(filename): 
        return
    
    # Optimization: Skip files that are clearly too small or not zlib
    if os.path.getsize(filename) < 10: 
        return

    try:
        with open(filename, "rb") as f:
            compressed_contents = f.read()
            
            # 1. Decompress the Zlib stream
            dco = zlib.decompressobj()
            decompressed_contents = dco.decompress(compressed_contents)
            
            # 2. Check the header (All Git objects start with 'blob', 'tree', 'commit', or 'tag')
            # Read first 6 bytes for validation
            header_bytes = decompressed_contents[:6]
            
            # Safely decode the header for checking
            try:
                header_type = header_bytes.decode('ascii')
            except UnicodeDecodeError:
                # If it's not ASCII, it's definitely not a Git header
                return
            
            is_valid_git_object = (
                header_type.startswith("tree") or 
                header_type.startswith("blob") or 
                header_type.startswith("commit") or 
                header_type.startswith("tag")
            )

            if not is_valid_git_object:
                return

            # 3. Calculate the SHA-1 hash of the *decompressed* content
            hash_value = sha1(decompressed_contents).hexdigest()
            print(f"Found object: {filename} -> {header_type[:4]} | Hash: {hash_value}")

            # 4. Save the object in the Git objects directory structure (xx/xxxxxxxx)
            objdir = os.path.join(dstdir, f".git/objects/{hash_value[:2]}")
            objname = os.path.join(objdir, f"{hash_value[2:]}")
            
            # Ensure the directory exists before writing
            os.makedirs(objdir, exist_ok=True)
            
            # Use zlib.compress to save it in the format Git expects (compressed again)
            with open(objname, "wb") as d:
                object_data = zlib.compress(decompressed_contents)
                d.write(object_data)

    except zlib.error:
        # File is not a valid zlib stream, which is expected for garbage data
        pass
    except Exception as e:
        # Catch all other unexpected errors
        print(f"Unexpected error processing {filename}: {e}")
        

# --- Execution ---
if __name__ == "__main__":
    
    print(f"--- Configuration Check ---")
    print(f"Source Directory (Recovered Files): {srcdir}")
    print(f"Destination Repository (Check Path): {dstdir}")
    print(f"Looking for .git/objects/ at: {git_objects_path}")
    print(f"---------------------------")
    
    # CRITICAL CHECK: Does the .git/objects folder exist?
    if not os.path.isdir(git_objects_path):
        print(f"\nFATAL ERROR: The destination directory ({dstdir}) does not appear to be a valid Git repository.")
        print(f"Please ensure you ran 'git init' inside '{dstdir}' and try again.")
    else:
        print(f"Git repository check passed. Starting reconstruction...")
        
        # Recursively walk through the recovered directories
        for filename in glob.iglob(os.path.join(srcdir, '**/*'), recursive=True):
            check_and_save_git_object(filename)
            
        print("\nReconstruction phase complete. You can now run 'git fsck' in your destination repository.")

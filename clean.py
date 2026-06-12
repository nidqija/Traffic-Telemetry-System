import shutil
from pathlib import Path

def delete_pycache(start_dir="."):
    """
    Recursively finds and deletes all __pycache__ folders 
    starting from the specified directory.
    """
    # Convert the input string to a Path object
    base_dir = Path(start_dir).resolve()
    print(f"Scanning for __pycache__ in: {base_dir}\n")
    
    count = 0
    # rglob searches recursively for the pattern
    for cache_dir in base_dir.rglob("__pycache__"):
        if cache_dir.is_dir():
            try:
                # shutil.rmtree deletes a directory and all its contents
                shutil.rmtree(cache_dir)
                print(f"[-] Deleted: {cache_dir}")
                count += 1
            except Exception as e:
                print(f"[!] Error deleting {cache_dir}: {e}")
                
    print(f"\nCleanup complete. Removed {count} '__pycache__' folder(s).")

if __name__ == "__main__":
    # By default, it cleans the directory the script is run from.
    # You can change "." to a specific path like "C:/Users/Name/Projects" if needed.
    delete_pycache(".")
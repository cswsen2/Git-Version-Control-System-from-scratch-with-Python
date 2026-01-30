import sys
import os
import hashlib
import zlib
import datetime
from repo import Repository

args = sys.argv[1:]
repo = Repository()

if len(args)>0:
    command = args[0]

    if command == "init":
        repo.init()

    elif command == "hash-object":
        file_name = args[1]
        with open(file_name, 'rb') as file:
            data = file.read()
            hexcode = repo.hash_object(data,"blob")
            print("object hashed")
            print(hexcode)

    elif command == "cat-file":
        hexcode = args[1]
        obj_type,content = repo.read_object(hexcode)
        print(content.decode("utf-8", errors="replace"))

    elif command == "write-tree":
        repo.write_tree()

    elif command == "commit-tree":
        tree_hash = args[1]
        commit_message = args[3]

        commit_content = f"tree {tree_hash}\n"

        date_with_time = datetime.datetime.now()
        formatted_date = date_with_time.strftime("%Y-%m-%d %H:%M:%S")

        if os.path.exists("./.mygit/HEAD.txt"):
            with open('./.mygit/HEAD.txt', 'r') as file:
                parent_hash = file.read().strip()
            commit_content += f"parent {parent_hash}\n"

        commit_content += f"author Senadha tosena@gmail.com {formatted_date}\n"
        commit_content += f"committer Senadha tosena@gmail.com {formatted_date}\n"
        commit_content += f"\n{commit_message}"

        hexcode = repo.hash_object(commit_content.encode('utf-8'),"commit")

        with open("./.mygit/HEAD.txt", 'w') as file:
            file.write(hexcode)
        print("Tree commited")
        print(hexcode)

    elif command == "log":
        last_commit_hash = None
        # with open("./.mygit/HEAD.txt",'r') as file:
        #     last_commit_hash = file.read().strip()

        last_commit_hash = repo.get_current_head()

        while True:
                obj_type, data = repo.read_object(last_commit_hash)
                file_content = data.decode("utf-8")
                file_content_list = file_content.split("\n")
                print(f"commit {last_commit_hash}\n")
                parent_hash = None

                for line in file_content_list:
                    if line.startswith("author"):
                        print(line)
                    if line.startswith("parent"):
                        parent_hash = line.split()[1]

                print(f"\n    {file_content_list[-1]}\n")
                print("-" * 30)
                if parent_hash:
                    last_commit_hash = parent_hash
                else:
                    break

    elif command == "checkout":
        commit_hash = args[1]
        _,content_encoded = repo.read_object(commit_hash)
        content = content_encoded.decode("utf-8")

        lines = content.split("\n")
        tree_hash = lines[0].split()[1]
        print(f"Restoring files from tree hash: {tree_hash}")

        _,tree_encoded = repo.read_object(tree_hash)
        tree_content = tree_encoded.decode('utf-8')

        for line in tree_content.split("\n"):
            parts = line.split()
            if len(parts)<4:
                continue

            blob_hash = parts[2]
            oroginal_filename= parts[3]

            _,blob_content = repo.read_object(blob_hash)
            with open(oroginal_filename, "wb") as actual_file:
                actual_file.write(blob_content)

        print(f"Checkout of commit {commit_hash} complete.")
        with open("./.mygit/HEAD.txt", "w") as f:
            f.write(commit_hash)

    elif command=="add":
        file_name = args[1]
        repo.update_index(file_name)
        print("Index updated")

    elif command=="commit":
        tree_hash = repo.write_tree()
        commit_message = args[2]

        commit_content = f"tree {tree_hash}\n"

        date_with_time = datetime.datetime.now()
        formatted_date = date_with_time.strftime("%Y-%m-%d %H:%M:%S")

        if os.path.exists("./.mygit/HEAD.txt"):
            with open('./.mygit/HEAD.txt', 'r') as file:
                parent_hash = file.read().strip()
            commit_content += f"parent {parent_hash}\n"

        commit_content += f"author Senadha tosena@gmail.com {formatted_date}\n"
        commit_content += f"committer Senadha tosena@gmail.com {formatted_date}\n"
        commit_content += f"\n{commit_message}"

        hexcode = repo.hash_object(commit_content.encode('utf-8'), "commit")

        with open("./.mygit/HEAD.txt", 'w') as file:
            file.write(hexcode)
        print("Tree commited")
        print(hexcode)

    else:
        print("Command not found")

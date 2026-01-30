import sys
import os
import hashlib
import zlib
import datetime




class Repository:
    def __init__(self,path="."):
        self.worktree = path
        self.gitdir = os.path.join(path, ".mygit")

    def init(self):
        try:
            os.makedirs(os.path.join(self.gitdir, "objects"), exist_ok=True)
            os.makedirs(os.path.join(self.gitdir, "refs"), exist_ok=True)
            print(f"Initialized git in {os.getcwd()}")
        except FileExistsError:
            print("myGit has already been initialized")

    def hash_object(self,data,obj_type,write=True):
        sha1 = hashlib.sha1()
        header = f"{obj_type} {len(data)}\0".encode("utf-8")
        full_content = header + data
        sha1.update(full_content)
        hexcode = sha1.hexdigest()

        folder_name = hexcode[:2]
        file_name = hexcode[2:]
        path = os.path.join(self.gitdir, "objects", folder_name, file_name)
        compressed_data = zlib.compress(full_content)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as file:
            file.write(compressed_data)
        print("Tree written")

        return hexcode

    def read_object(self,sha):
        folder_name = sha[:2]
        file_name = sha[2:]
        path = os.path.join(self.gitdir,"objects",folder_name,file_name)
        with open(path, "rb") as file:
            compressed_data = file.read()
            decompressed_data = zlib.decompress(compressed_data)
            header,body = decompressed_data.split(b'\x00', maxsplit=1)
            obj_type = header.split()[1].decode('utf-8')
            return obj_type,body

    def update_index(self,file_name):
        index_path = os.path.join(self.gitdir,"index")

        with open(file_name,'rb') as file:
            file_content = file.read()
        sha = self.hash_object(file_content,"blob")

        entries = {}
        if os.path.exists(index_path):
            with open(index_path,'r') as file:
                content = file.read()
                for line in content.split("\n"):
                    if line.strip():
                        parts = line.split(" ",1)
                        if len(parts) == 2:
                            existing_name = parts[1]
                            existing_hash = parts[0]

                            entries[existing_name] = existing_hash

        entries[file_name] = sha

        with open(index_path,"w") as file:
            for name in sorted(entries.keys()):
                file.write(f"{entries[name]} {name}\n")


    def write_tree(self):
        index_path = os.path.join(self.gitdir, "index")

        blob_list = []
        if os.path.exists(index_path):
            with open(index_path,"r") as file:
                content = file.read()
                for line in content.split("\n"):
                    if not line.strip():
                        continue
                    file_hash = line.split(" ",1)[0]
                    file_name = line.split(" ",1)[1]

                    blob_list.append(f"100644 blob {file_hash} {file_name}")

        blob_content = ("\n".join(blob_list)).encode("utf-8")
        sha = self.hash_object(blob_content, "tree")
        print(sha)
        return sha

    def get_current_head(self):
        head_path = os.path.join(self.gitdir,"HEAD.txt")
        with open(head_path,"r") as file:
            content = file.read()
            content_split = content.split()
            if content_split[0] == "ref:":
                master_path = os.path.join(self.gitdir,content_split[1])
                with open(master_path,"r") as f:
                    commit_hash = f.read()
                    return commit_hash
            else:
                return content.strip()







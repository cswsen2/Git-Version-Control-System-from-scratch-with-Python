# Content-Addressable VCS Implementation (Python)

A fully functional, distributed **Version Control System (VCS)** built from scratch in Python.

This project implements the core low-level architecture of Git, including **content-addressable storage**, **DAG (Directed Acyclic Graph)** history traversal, and reference management. It was built to demonstrate a deep understanding of file system internals, hashing algorithms, and data structure serialization.

## 🚀 Overview

Unlike simple file copiers, this system uses a **Merkle Tree-like structure** to store snapshots efficiently. It replicates the internal "plumbing" of Git:

* **Content-Addressable Storage:** Files are deduplicated and stored based on their SHA-1 hash.
* **Object Database:** Custom binary serialization format using Zlib compression.
* **Reference System:** Full support for Branches (`refs/heads`) and HEAD pointer management.
* **Atomic Operations:** Staging area (Index) management and tree construction.

## 🛠 Features

* **`init`**: Initializes a new repository structure (`.mygit/objects`, `.mygit/refs`).
* **`hash-object`**: Computes SHA-1 hashes and compresses data into blobs.
* **`cat-file`**: Reads and decompresses binary objects from the database.
* **`add`**: Updates the **Staging Area (Index)**, tracking file blobs.
* **`write-tree`**: recursively builds **Tree Objects** representing the directory state.
* **`commit`**: Creates **Commit Objects** linking to trees and parent commits (Linked List/DAG).
* **`log`**: Traverses and displays the commit history graph.
* **`branch`**: Creates new pointers (references) to specific commits.
* **`checkout`**:
    * Restores the working directory to a specific state.
    * Handles **Detached HEAD** (checking out a hash).
    * Handles **Attached HEAD** (checking out a branch and updating the pointer).

## 📂 Architecture

The system relies on four fundamental object types stored in `.mygit/objects`:



1.  **Blob:** Stores the raw file content (compressed).
2.  **Tree:** Represents a directory; maps filenames to Blobs or other Trees.
3.  **Commit:** A wrapper object containing the Tree hash, author metadata, and Parent hash.
4.  **Refs:** Text files in `.mygit/refs/heads/` that store pointers to the latest commit of a branch.

## 💻 Installation & Usage

### 1. Setup
Clone this repository to your local machine:
```bash
git clone [https://github.com/yourusername/content-addressable-vcs-python.git](https://github.com/yourusername/content-addressable-vcs-python.git)
cd content-addressable-vcs-python

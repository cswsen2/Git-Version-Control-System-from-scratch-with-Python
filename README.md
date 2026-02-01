# PyGit: Git Internals Implementation

## Overview
A simplified implementation of Git's core object model, built to deeply 
understand version control internals. This project implements Git's 
content-addressable storage, object model, and basic versioning operations.

## What I Learned
- **Content-addressable storage**: How SHA-1 hashing enables deduplication 
  and integrity
- **Merkle trees**: The commit → tree → blob hierarchy
- **Immutable data structures**: Why Git objects never change
- **Symbolic references**: How HEAD and branches work as pointers

## Architecture

[Insert your diagram here]

## Implemented Features
- ✅ Blob, tree, and commit objects
- ✅ Staging area (index)
- ✅ Branch creation and switching
- ✅ Commit history traversal
- ✅ Detached HEAD state

## Comparison to Real Git

### What's the Same
- Object storage format (header + content)
- SHA-1 hashing algorithm
- Directory structure (.mygit/objects, .mygit/refs)
- Branch pointer mechanism

### Simplified Decisions
- Text-based index (Git uses binary format)
- Human-readable timestamps (Git uses Unix timestamps)
- Single-level directory support (Git handles nested directories)
- No pack files or delta compression

### Not Implemented (Yet)
- Distributed features (push/pull)
- Merge and conflict resolution
- Diff algorithms
- Network protocol
- Pack files

## Usage

\`\`\`bash
# Initialize repository
python mygit.py init

# Stage a file
python mygit.py add file.txt

# Commit
python mygit.py commit -m "Initial commit"

# Create branch
python mygit.py branch feature

# View history
python mygit.py log
\`\`\`

## Testing

\`\`\`bash
pytest tests/
\`\`\`

## Future Enhancements
1. Implement merge with conflict detection
2. Add nested directory support
3. Build web UI for visualization
4. Add comprehensive diff functionality

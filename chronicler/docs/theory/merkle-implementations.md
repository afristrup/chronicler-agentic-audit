# Merkle Tree Implementations: Practical Guide

## Overview

This document provides practical implementations of Merkle trees in various programming languages, along with real-world examples and best practices for integration into blockchain systems.

## Python Implementation

### Basic Merkle Tree

```python
import hashlib
from typing import List, Tuple, Optional

class MerkleTree:
    def __init__(self, data: List[bytes]):
        self.data = data
        self.leaves = [self._hash(item) for item in data]
        self.tree = self._build_tree()
        self.root = self.tree[-1][0] if self.tree else None

    def _hash(self, data: bytes) -> bytes:
        """Compute SHA-256 hash of data."""
        return hashlib.sha256(data).digest()

    def _build_tree(self) -> List[List[bytes]]:
        """Build the complete Merkle tree."""
        if not self.leaves:
            return []

        tree = [self.leaves]
        current_level = self.leaves

        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                parent = self._hash(left + right)
                next_level.append(parent)
            tree.append(next_level)
            current_level = next_level

        return tree

    def get_proof(self, index: int) -> List[Tuple[bytes, bool]]:
        """Generate Merkle proof for data at given index."""
        if index >= len(self.leaves):
            raise ValueError("Index out of range")

        proof = []
        current_index = index

        for level in self.tree[:-1]:  # Exclude root level
            if current_index % 2 == 0:  # Left child
                sibling_index = current_index + 1
                is_right = False
            else:  # Right child
                sibling_index = current_index - 1
                is_right = True

            if sibling_index < len(level):
                proof.append((level[sibling_index], is_right))

            current_index //= 2

        return proof

    def verify_proof(self, leaf_hash: bytes, proof: List[Tuple[bytes, bool]], root_hash: bytes) -> bool:
        """Verify a Merkle proof."""
        current_hash = leaf_hash

        for sibling_hash, is_right in proof:
            if is_right:
                current_hash = self._hash(current_hash + sibling_hash)
            else:
                current_hash = self._hash(sibling_hash + current_hash)

        return current_hash == root_hash

# Usage example
data = [b"transaction1", b"transaction2", b"transaction3", b"transaction4"]
tree = MerkleTree(data)
proof = tree.get_proof(1)  # Proof for "transaction2"
is_valid = tree.verify_proof(tree.leaves[1], proof, tree.root)
print(f"Proof valid: {is_valid}")
```

### Sparse Merkle Tree

```python
class SparseMerkleTree:
    def __init__(self, depth: int = 256):
        self.depth = depth
        self.default_hashes = self._compute_default_hashes()
        self.root = self.default_hashes[depth]
        self.leaves = {}

    def _compute_default_hashes(self) -> List[bytes]:
        """Pre-compute default hashes for each level."""
        default_hashes = [b'\x00' * 32]  # Level 0 default

        for i in range(self.depth):
            default_hash = hashlib.sha256(default_hashes[i] + default_hashes[i]).digest()
            default_hashes.append(default_hash)

        return default_hashes

    def _get_path(self, key: int) -> List[bool]:
        """Get the path from root to leaf for a given key."""
        path = []
        for i in range(self.depth):
            path.append(bool(key & (1 << (self.depth - 1 - i))))
        return path

    def update(self, key: int, value: bytes) -> bytes:
        """Update a leaf value and return new root."""
        leaf_hash = hashlib.sha256(value).digest()
        self.leaves[key] = leaf_hash

        path = self._get_path(key)
        current_hash = leaf_hash

        for i, is_right in enumerate(path):
            level = self.depth - 1 - i
            sibling_key = key ^ (1 << i)

            if sibling_key in self.leaves:
                sibling_hash = self.leaves[sibling_key]
            else:
                sibling_hash = self.default_hashes[level]

            if is_right:
                current_hash = hashlib.sha256(sibling_hash + current_hash).digest()
            else:
                current_hash = hashlib.sha256(current_hash + sibling_hash).digest()

        self.root = current_hash
        return self.root

    def get_proof(self, key: int) -> List[Tuple[bytes, bool]]:
        """Generate inclusion proof for a key."""
        if key not in self.leaves:
            raise ValueError("Key not found")

        proof = []
        path = self._get_path(key)

        for i, is_right in enumerate(path):
            level = self.depth - 1 - i
            sibling_key = key ^ (1 << i)

            if sibling_key in self.leaves:
                sibling_hash = self.leaves[sibling_key]
            else:
                sibling_hash = self.default_hashes[level]

            proof.append((sibling_hash, is_right))

        return proof
```

## Solidity Implementation

### Merkle Tree Verification

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MerkleTree {
    bytes32 public root;

    constructor(bytes32 _root) {
        root = _root;
    }

    function verifyProof(
        bytes32 leaf,
        bytes32[] memory proof,
        bool[] memory proofFlags
    ) public view returns (bool) {
        bytes32 computedHash = leaf;

        for (uint256 i = 0; i < proof.length; i++) {
            bytes32 proofElement = proof[i];

            if (proofFlags[i]) {
                // Hash(current computed hash + current element of the proof)
                computedHash = keccak256(abi.encodePacked(computedHash, proofElement));
            } else {
                // Hash(current element of the proof + current computed hash)
                computedHash = keccak256(abi.encodePacked(proofElement, computedHash));
            }
        }

        return computedHash == root;
    }

    function verifyMultipleProofs(
        bytes32[] memory leaves,
        bytes32[][] memory proofs,
        bool[][] memory proofFlags
    ) public view returns (bool[] memory) {
        require(
            leaves.length == proofs.length && leaves.length == proofFlags.length,
            "Array lengths must match"
        );

        bool[] memory results = new bool[](leaves.length);

        for (uint256 i = 0; i < leaves.length; i++) {
            results[i] = verifyProof(leaves[i], proofs[i], proofFlags[i]);
        }

        return results;
    }
}

// Example usage contract
contract MerkleExample {
    MerkleTree public merkleTree;

    constructor(bytes32 _root) {
        merkleTree = new MerkleTree(_root);
    }

    function claimWithProof(
        address recipient,
        uint256 amount,
        bytes32[] memory proof,
        bool[] memory proofFlags
    ) external {
        bytes32 leaf = keccak256(abi.encodePacked(recipient, amount));

        require(
            merkleTree.verifyProof(leaf, proof, proofFlags),
            "Invalid proof"
        );

        // Process the claim
        // ... implementation details
    }
}
```

## JavaScript/TypeScript Implementation

### Merkle Tree for Frontend

```typescript
import { ethers } from 'ethers';

interface MerkleProof {
    proof: string[];
    proofFlags: boolean[];
}

class MerkleTree {
    private leaves: string[];
    private tree: string[][];
    private root: string;

    constructor(leaves: string[]) {
        this.leaves = leaves.map(leaf => this.hash(leaf));
        this.tree = this.buildTree();
        this.root = this.tree[this.tree.length - 1][0];
    }

    private hash(data: string): string {
        return ethers.utils.keccak256(ethers.utils.toUtf8Bytes(data));
    }

    private buildTree(): string[][] {
        if (this.leaves.length === 0) return [];

        const tree = [this.leaves];
        let currentLevel = this.leaves;

        while (currentLevel.length > 1) {
            const nextLevel: string[] = [];

            for (let i = 0; i < currentLevel.length; i += 2) {
                const left = currentLevel[i];
                const right = i + 1 < currentLevel.length ? currentLevel[i + 1] : left;
                const parent = ethers.utils.keccak256(left + right.slice(2));
                nextLevel.push(parent);
            }

            tree.push(nextLevel);
            currentLevel = nextLevel;
        }

        return tree;
    }

    public getProof(index: number): MerkleProof {
        if (index >= this.leaves.length) {
            throw new Error('Index out of range');
        }

        const proof: string[] = [];
        const proofFlags: boolean[] = [];
        let currentIndex = index;

        for (let level = 0; level < this.tree.length - 1; level++) {
            const isRight = currentIndex % 2 === 1;
            const siblingIndex = isRight ? currentIndex - 1 : currentIndex + 1;

            if (siblingIndex < this.tree[level].length) {
                proof.push(this.tree[level][siblingIndex]);
                proofFlags.push(isRight);
            }

            currentIndex = Math.floor(currentIndex / 2);
        }

        return { proof, proofFlags };
    }

    public verifyProof(leaf: string, proof: string[], proofFlags: boolean[], root: string): boolean {
        let computedHash = leaf;

        for (let i = 0; i < proof.length; i++) {
            const proofElement = proof[i];

            if (proofFlags[i]) {
                computedHash = ethers.utils.keccak256(computedHash + proofElement.slice(2));
            } else {
                computedHash = ethers.utils.keccak256(proofElement + computedHash.slice(2));
            }
        }

        return computedHash === root;
    }

    public getRoot(): string {
        return this.root;
    }
}

// Usage example
const data = ['transaction1', 'transaction2', 'transaction3', 'transaction4'];
const tree = new MerkleTree(data);
const proof = tree.getProof(1);
const isValid = tree.verifyProof(tree.leaves[1], proof.proof, proof.proofFlags, tree.getRoot());
console.log('Proof valid:', isValid);
```

## Rust Implementation

### High-Performance Merkle Tree

```rust
use sha2::{Sha256, Digest};
use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct MerkleTree {
    leaves: Vec<Vec<u8>>,
    tree: Vec<Vec<Vec<u8>>>,
    root: Vec<u8>,
}

impl MerkleTree {
    pub fn new(data: Vec<Vec<u8>>) -> Self {
        let leaves: Vec<Vec<u8>> = data.into_iter().map(|item| Self::hash(&item)).collect();
        let tree = Self::build_tree(&leaves);
        let root = tree.last().unwrap().first().unwrap().clone();

        MerkleTree { leaves, tree, root }
    }

    fn hash(data: &[u8]) -> Vec<u8> {
        let mut hasher = Sha256::new();
        hasher.update(data);
        hasher.finalize().to_vec()
    }

    fn build_tree(leaves: &[Vec<u8>]) -> Vec<Vec<Vec<u8>>> {
        if leaves.is_empty() {
            return vec![];
        }

        let mut tree = vec![leaves.to_vec()];
        let mut current_level = leaves.to_vec();

        while current_level.len() > 1 {
            let mut next_level = Vec::new();

            for chunk in current_level.chunks(2) {
                let left = &chunk[0];
                let right = if chunk.len() > 1 { &chunk[1] } else { left };

                let mut combined = Vec::new();
                combined.extend_from_slice(left);
                combined.extend_from_slice(right);

                let parent = Self::hash(&combined);
                next_level.push(parent);
            }

            tree.push(next_level.clone());
            current_level = next_level;
        }

        tree
    }

    pub fn get_proof(&self, index: usize) -> Result<Vec<(Vec<u8>, bool)>, &'static str> {
        if index >= self.leaves.len() {
            return Err("Index out of range");
        }

        let mut proof = Vec::new();
        let mut current_index = index;

        for level in &self.tree[..self.tree.len() - 1] {
            let is_right = current_index % 2 == 1;
            let sibling_index = if is_right { current_index - 1 } else { current_index + 1 };

            if sibling_index < level.len() {
                proof.push((level[sibling_index].clone(), is_right));
            }

            current_index /= 2;
        }

        Ok(proof)
    }

    pub fn verify_proof(&self, leaf_hash: &[u8], proof: &[(Vec<u8>, bool)], root_hash: &[u8]) -> bool {
        let mut current_hash = leaf_hash.to_vec();

        for (sibling_hash, is_right) in proof {
            let mut combined = Vec::new();

            if *is_right {
                combined.extend_from_slice(&current_hash);
                combined.extend_from_slice(sibling_hash);
            } else {
                combined.extend_from_slice(sibling_hash);
                combined.extend_from_slice(&current_hash);
            }

            current_hash = Self::hash(&combined);
        }

        current_hash == root_hash
    }

    pub fn get_root(&self) -> &[u8] {
        &self.root
    }
}

// Example usage
fn main() {
    let data = vec![
        b"transaction1".to_vec(),
        b"transaction2".to_vec(),
        b"transaction3".to_vec(),
        b"transaction4".to_vec(),
    ];

    let tree = MerkleTree::new(data);
    let proof = tree.get_proof(1).unwrap();
    let is_valid = tree.verify_proof(&tree.leaves[1], &proof, tree.get_root());

    println!("Proof valid: {}", is_valid);
}
```

## Integration Patterns

### Blockchain Integration

```python
class BlockchainMerkleTree:
    def __init__(self, contract_address: str, web3_provider):
        self.contract_address = contract_address
        self.web3 = web3_provider
        self.contract = self._load_contract()

    def _load_contract(self):
        # Load the MerkleTree contract ABI and address
        # Implementation depends on your web3 library
        pass

    def verify_on_chain(self, leaf: bytes, proof: List[Tuple[bytes, bool]], root: bytes) -> bool:
        """Verify proof on-chain."""
        # Convert proof to contract format
        proof_bytes = [p[0] for p in proof]
        proof_flags = [p[1] for p in proof]

        return self.contract.functions.verifyProof(
            leaf, proof_bytes, proof_flags
        ).call()

    def batch_verify(self, leaves: List[bytes], proofs: List[List[Tuple[bytes, bool]]], root: bytes) -> List[bool]:
        """Batch verify multiple proofs on-chain."""
        # Implementation for batch verification
        pass
```

### Database Integration

```python
class DatabaseMerkleTree:
    def __init__(self, db_connection):
        self.db = db_connection
        self.create_tables()

    def create_tables(self):
        """Create necessary database tables."""
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS merkle_trees (
                id INTEGER PRIMARY KEY,
                root_hash BLOB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.db.execute("""
            CREATE TABLE IF NOT EXISTS merkle_proofs (
                id INTEGER PRIMARY KEY,
                tree_id INTEGER,
                leaf_index INTEGER,
                proof_data BLOB,
                FOREIGN KEY (tree_id) REFERENCES merkle_trees (id)
            )
        """)

    def store_tree(self, root_hash: bytes) -> int:
        """Store a Merkle tree root and return its ID."""
        cursor = self.db.execute(
            "INSERT INTO merkle_trees (root_hash) VALUES (?)",
            (root_hash,)
        )
        return cursor.lastrowid

    def store_proof(self, tree_id: int, leaf_index: int, proof: List[Tuple[bytes, bool]]):
        """Store a Merkle proof."""
        proof_data = self._serialize_proof(proof)
        self.db.execute(
            "INSERT INTO merkle_proofs (tree_id, leaf_index, proof_data) VALUES (?, ?, ?)",
            (tree_id, leaf_index, proof_data)
        )

    def get_proof(self, tree_id: int, leaf_index: int) -> List[Tuple[bytes, bool]]:
        """Retrieve a stored Merkle proof."""
        cursor = self.db.execute(
            "SELECT proof_data FROM merkle_proofs WHERE tree_id = ? AND leaf_index = ?",
            (tree_id, leaf_index)
        )
        row = cursor.fetchone()
        if row:
            return self._deserialize_proof(row[0])
        return []
```

## Performance Optimization

### Batch Operations

```python
class OptimizedMerkleTree:
    def __init__(self):
        self.cache = {}

    def batch_verify(self, proofs: List[Tuple[bytes, List[Tuple[bytes, bool]], bytes]]) -> List[bool]:
        """Batch verify multiple proofs efficiently."""
        results = []

        for leaf_hash, proof, root_hash in proofs:
            # Use cached intermediate results when possible
            cache_key = self._get_cache_key(proof, root_hash)

            if cache_key in self.cache:
                results.append(self.cache[cache_key] == leaf_hash)
            else:
                is_valid = self.verify_proof(leaf_hash, proof, root_hash)
                self.cache[cache_key] = leaf_hash if is_valid else None
                results.append(is_valid)

        return results

    def _get_cache_key(self, proof: List[Tuple[bytes, bool]], root_hash: bytes) -> str:
        """Generate cache key for proof verification."""
        proof_str = "".join([p[0].hex() + str(p[1]) for p in proof])
        return proof_str + root_hash.hex()
```

## Testing and Validation

### Test Suite

```python
import unittest
import hashlib

class MerkleTreeTests(unittest.TestCase):
    def setUp(self):
        self.test_data = [b"item1", b"item2", b"item3", b"item4"]
        self.tree = MerkleTree(self.test_data)

    def test_tree_construction(self):
        """Test that tree is constructed correctly."""
        self.assertIsNotNone(self.tree.root)
        self.assertEqual(len(self.tree.leaves), len(self.test_data))

    def test_proof_generation(self):
        """Test that proofs are generated correctly."""
        for i in range(len(self.test_data)):
            proof = self.tree.get_proof(i)
            self.assertIsInstance(proof, list)
            self.assertTrue(len(proof) > 0)

    def test_proof_verification(self):
        """Test that proofs verify correctly."""
        for i in range(len(self.test_data)):
            proof = self.tree.get_proof(i)
            is_valid = self.tree.verify_proof(
                self.tree.leaves[i], proof, self.tree.root
            )
            self.assertTrue(is_valid)

    def test_invalid_proof(self):
        """Test that invalid proofs are rejected."""
        proof = self.tree.get_proof(0)
        # Modify the proof to make it invalid
        proof[0] = (b"invalid_hash", proof[0][1])

        is_valid = self.tree.verify_proof(
            self.tree.leaves[0], proof, self.tree.root
        )
        self.assertFalse(is_valid)

    def test_empty_tree(self):
        """Test behavior with empty data."""
        empty_tree = MerkleTree([])
        self.assertEqual(empty_tree.root, None)

    def test_single_item(self):
        """Test tree with single item."""
        single_tree = MerkleTree([b"single_item"])
        self.assertIsNotNone(single_tree.root)
        proof = single_tree.get_proof(0)
        self.assertEqual(len(proof), 0)  # No proof needed for single item

if __name__ == '__main__':
    unittest.main()
```

## Conclusion

This implementation guide provides practical examples of Merkle trees in multiple languages and contexts. The implementations can be adapted and extended based on specific requirements, such as:

- **Performance requirements**: Choose appropriate hash functions and optimization strategies
- **Security requirements**: Use cryptographically secure hash functions and proper key management
- **Integration needs**: Adapt to specific blockchain platforms or database systems
- **Scalability**: Implement batch operations and caching for high-throughput systems

The provided code examples serve as a foundation for building robust Merkle tree implementations in production systems.
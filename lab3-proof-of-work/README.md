# Lab 3: Blockchain Proof of Work

## Objective

This lab teaches students how blockchain mining works using Proof of Work.

## What Students Learn

- What is mining
- What is nonce
- What is difficulty
- Why the hash must start with zeros
- Why mining takes time
- Why changing blockchain data is difficult

## How to Run

```bash
python proof_of_work.py

Explanation

In this lab, each block must find a hash that starts with a number of zeros.

Example:

0000a82f9c...

The program keeps changing the nonce until it finds a valid hash.

This process is called mining.

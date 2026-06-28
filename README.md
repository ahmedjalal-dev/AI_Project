# AI_Project

# Solving Travelling Salesman Problem (TSP) using Hybrid Genetic Algorithms

## AI Research Project — Track C (Research Paper Implementation)

**Course:** Artificial Intelligence
**Institution:** FAST-NU Lahore
**Project Type:** Research Paper Reproduction & Extension
**Year:** 2026

---

## Overview

This project focuses on solving the classic **Travelling Salesman Problem (TSP)** using evolutionary computation and local search optimization techniques.

The project follows **Track C: Research Paper Implementation**, where we selected, implemented, analyzed, and extended a published AI research paper.

The reference paper:

> **"Solving Travelling Salesman Problem (TSP) by Hybrid Genetic Algorithm (HGA)"**
> A.M.H. Al-Ibrahim
> International Journal of Advanced Computer Science and Applications (IJACSA), 2020

The original paper proposed a **Hybrid Genetic Algorithm (HGA)** that combines:

* Genetic Algorithm (GA)
* A custom crossover mechanism
* Neighbour Local Search Algorithm (NLSA)

to efficiently solve large-scale TSP instances.

Our implementation reproduces the paper's approach and introduces an additional hybrid method using **GA + 2-Opt Local Search** for performance comparison.

---

# Problem Statement

The Travelling Salesman Problem (TSP) is a well-known NP-complete optimization problem.

Given a set of cities, the goal is to find the shortest possible route that:

* Visits every city exactly once
* Returns to the starting city
* Minimizes total travelling distance

For large numbers of cities, brute force search becomes computationally impossible, so heuristic and metaheuristic algorithms are used.

---

# Project Objectives

The objectives of this project were:

* Reproduce the Hybrid Genetic Algorithm proposed in the research paper
* Understand the contribution of crossover and local search techniques
* Compare different optimization approaches
* Analyze performance on standard TSPLIB benchmarks
* Extend the paper implementation with a stronger local search strategy

---

# Implemented Approaches

## 1. NLSA Standalone (Baseline)

A pure local search approach.

Process:

1. Generate an initial tour using nearest-neighbour heuristic
2. Apply Neighbour Local Search Algorithm
3. Improve the route using local modifications

This serves as the baseline model.

---

## 2. GA + NLSA (Paper Replication)

Implementation of Al-Ibrahim's Hybrid Genetic Algorithm.

Components:

### Genetic Algorithm

Includes:

* Population initialization
* Fitness evaluation
* Selection
* Mutation
* Evolution across generations

### Proposed Crossover Mechanism

The crossover operator:

* Preserves common edges between parent solutions
* Creates new valid tours
* Explores better routes

### Neighbour Local Search Algorithm

Applied as a local improvement operator inside the genetic algorithm.

This improves convergence and solution quality.

---

## 3. GA + 2-Opt (Our Extension)

We extended the original paper by replacing NLSA with a stronger **2-Opt local search algorithm**.

Improvements:

* Full neighbourhood exploration
* No segment length limitation
* Candidate-list optimization
* Applied more frequently during evolution

The goal was to investigate:

> Does stronger local optimization improve Genetic Algorithm performance?

---

# Dataset

Experiments were performed using standard TSPLIB benchmark datasets.

Included benchmark instances:

* berlin52.tsp
* ch130.tsp
* ch150.tsp
* gil262.tsp
* rat195.tsp
* tsp225.tsp
* a280.tsp
* rat575.tsp
* d1291.tsp

Problem sizes range from:

**52 cities → 1291 cities**

---

# Experimental Comparison

The project compares:

| Algorithm  | Purpose                    |
| ---------- | -------------------------- |
| NLSA       | Baseline local search      |
| GA + NLSA  | Research paper replication |
| GA + 2-Opt | Proposed extension         |

---

# Results Summary

The experiments show:

### GA + NLSA vs NLSA

The hybrid genetic algorithm consistently improved results because:

* GA provides global exploration
* NLSA improves individual solutions locally
* Population diversity helps escape local minima

### GA + 2-Opt vs GA + NLSA

GA + 2-Opt achieved the best results on most benchmarks.

Key observations:

* berlin52 reached the known optimal solution
* tsp225 achieved almost optimal performance
* Overall solution quality improved on 6/9 benchmarks

---

# Replication Results

The reproduced GA + NLSA implementation was compared with the original paper.

Our results matched the reported results with small differences caused by:

* Python vs C++ implementation differences
* Random initialization
* Runtime and generation variations

Most benchmarks showed less than 5% deviation.

---

# Technologies Used

* Python
* Genetic Algorithms
* Evolutionary Computation
* Heuristic Search
* Local Search Optimization
* TSPLIB Dataset

---

# Project Structure

```
AI_Project/
│
├── datasets/
│   ├── a280.tsp
│   ├── berlin52.tsp
│   ├── ch130.tsp
│   └── other TSPLIB files
│
├── algorithms/
│   ├── genetic_algorithm
│   ├── nlsa
│   ├── two_opt
│
├── results/
│   ├── charts
│   ├── comparison_tables
│
├── report/
│   └── Research Report.pdf
│
└── README.md
```

---

# Research Insights

The project demonstrates that:

* Pure local search is limited by its starting solution
* Genetic Algorithms provide global exploration
* Local search improves exploitation
* Hybrid optimization methods perform better than isolated techniques

The main conclusion:

> Combining evolutionary search with strong local optimization produces higher quality solutions for complex optimization problems like TSP.

---

# Authors

FAST-NU Lahore — Artificial Intelligence Project

* Ahmad Jalal
* Farhan Tahir
* Ayan Iftikhar
* Faiq Rizwan

---

# Reference

Al-Ibrahim, A.M.H. (2020).
**Solving Travelling Salesman Problem (TSP) by Hybrid Genetic Algorithm (HGA).**
International Journal of Advanced Computer Science and Applications (IJACSA), Vol. 11, No. 6.

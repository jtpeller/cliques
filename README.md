# Cliques

Compute n-sized Cliques of words!

## Table of Contents

- [Cliques](#cliques)
  - [Table of Contents](#table-of-contents)
  - [Purpose](#purpose)
  - [Features](#features)
  - [Future Plans](#future-plans)

## Purpose

My verse game is a wordle-like game in which you play against bots. I was writing a bot that would utilize the strategy of cliques to structure its guesses to cover as much of the alphabet as possible before making its "final" guess.

Therefore, I needed an n-sized clique calculator.

I originally based mine on [Benjamin Paassen's five_clique](https://gitlab.com/bpaassen/five_clique) script, but that only computes words of length 5. So, I used Paassen's project as an inspiration to create my n-sized Clique calculator. Functionality was added to create a generalized approach.

## Features

Features:

- Clique class, responsible for computing the cliques from a provided word list. Capable of outputting to a CSV file!
- Graph class, responsible for computing the neighbors of words. Also can be output to a CSV!

## Future Plans

Some of the future plans / features include:

- Release this on pip, so it may be used in other projects as a module or as a package.
- Optimize graphs by allowing an existing graph to be read in. Enables a compute-once-use-many scheme.

Completed tasks:

- Fuzzy search, for when a clique does not exist in the list. Enables overlap in a clique

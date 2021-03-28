"""
CSC148, Winter 2021
Assignment 2: Automatic Puzzle Solver
==============================
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Jonathan Calver, Sophia Huynh,
         Maryam Majedi, and Jaisie Sin.

All of the files in this directory are:
Copyright (c) 2021 Diane Horton, Jonathan Calver, Sophia Huynh,
                   Maryam Majedi, and Jaisie Sin.

=== Module Description ===

This module contains the abstract Solver class and its two subclasses, which
find solutions to puzzles, step by step.
"""

from __future__ import annotations

from typing import List, Optional, Set

# You may remove this import if you don't use it in your code.
from adts import Queue
from assignments.a2.sudoku_puzzle import SudokuPuzzle

from puzzle import Puzzle


class Solver:
    """"
    A solver for full-information puzzles. This is an abstract class
    and purely provides the interface for our solve method.
    """

    # You may NOT change the interface to the solve method.
    # Note the optional parameter seen and its type.
    # Your implementations of this method in the two subclasses should use seen
    # to keep track of all puzzle states that you encounter during the
    # solution process.
    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """
        raise NotImplementedError


# TODO (Task 2): implement the solve method in the DfsSolver class.
# Your solve method MUST be a recursive function (i.e. it must make
# at least one recursive call to itself)
# You may NOT change the interface to the solve method.
class DfsSolver(Solver):
    """"
    A solver for full-information puzzles that uses
    a depth first search strategy.
    """

    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """
        if puzzle.fail_fast() or (seen is not None and str(puzzle) in seen):
            return []
        elif puzzle.is_solved():
            return [puzzle]
        else:
            solution = [puzzle]
            if seen is None:
                seen = set()
            seen.add(str(puzzle))
            for ext in puzzle.extensions():
                t = self.solve(ext, seen)
                if t == []:
                    continue
                elif t[-1].is_solved():
                    solution.extend(t)
                    return solution
            return solution


# TODO (Task 2): implement the solve method in the BfsSolver class.
# Hint: You may find a Queue useful here.
class BfsSolver(Solver):
    """"
    A solver for full-information puzzles that uses
    a breadth first search strategy.
    """

    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """
        solution = [puzzle]
        q = Queue()

        if puzzle.is_solved():
            return [puzzle]

        for ext in puzzle.extensions():
            if seen is None or str(ext) not in seen:
                q.enqueue(ext)

        while not q.is_empty():
            obj = q.dequeue()
            if not obj.fail_fast() and (seen is None or str(obj) not in seen):
                solution.append(obj)
                for ext in obj.extensions():
                    if seen is None or str(ext) not in seen:
                        q.enqueue(ext)

        # TODO: Sort through solution list to pull out path

        return solution

        # solution = [puzzle]
        # q = Queue()
        #
        # if puzzle.is_solved():
        #     return []
        #
        # # count = -1
        # for ext in puzzle.extensions():
        #     if seen is None or str(ext) not in seen:
        #         q.enqueue(ext)
        #         # count += 1
        #
        # # for i in range(count + 1):
        # #     solution.append([puzzle])
        #
        # # var = 0
        # while not q.is_empty():
        #     obj = q.dequeue()
        #     # if obj.is_solved():
        #     #     solution.append(obj)
        #     #     # solution[var].append(obj)
        #     #     while not q.is_empty():
        #     #         q.dequeue()
        #     if not obj.fail_fast() and (seen is None or str(obj) not in seen):
        #         solution.append(obj)
        #         # solution[var].append(obj)
        #         # if var == count:
        #         #     var = 0
        #         # else:
        #         #     var += 1
        #         for ext in obj.extensions():
        #             if seen is None or str(ext) not in seen:
        #                 q.enqueue(ext)
        #
        # # for i in range(count):
        # #     if solution[i][-1].is_solved():
        # #         return solution[i]
        # # return []
        # return solution


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={'pyta-reporter': 'ColorReporter',
                                'allowed-io': [],
                                'allowed-import-modules': ['doctest',
                                                           'python_ta',
                                                           'typing',
                                                           '__future__',
                                                           'puzzle',
                                                           'adts'],
                                'disable': ['E1136'],
                                'max-attributes': 15}
                        )

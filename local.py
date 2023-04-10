#!/usr/bin/env python3
class LocalAlignment:
    def __init__(self, seq1, seq2):
        self.seq1 = seq1  # First sequence
        self.seq2 = seq2  # Second sequence
        self.score_matrix = None  # Placeholder for the score matrix
        self.max_score = 0  # Maximum score
        self.score_matrix, self.max_score = self.generate_score_matrix()  # Generate the score matrix and find the maximum score
        self.aligned_seq, self.aligned_ref = self.traceback()  # Trace back to find the aligned sequences

    def generate_score_matrix(self):
        match_score = 2  # Score for a match
        mismatch_score = -1  # Score for a mismatch
        gap_penalty = -2  # Penalty for a gap
        rows = len(self.seq1) + 1  # Number of rows in the score matrix
        cols = len(self.seq2) + 1  # Number of columns in the score matrix
        score_matrix = [[0 for _ in range(cols)] for _ in range(rows)]  # Initialize the score matrix with zeros
        max_score = 0  # Maximum score
        for i in range(1, rows):
            for j in range(1, cols):
                # Calculate the score for a match, mismatch, and gap
                match = score_matrix[i-1][j-1] + (match_score if self.seq1[i-1] == self.seq2[j-1] else mismatch_score)
                delete = score_matrix[i-1][j] + gap_penalty
                insert = score_matrix[i][j-1] + gap_penalty
                # Update the score matrix with the maximum score
                score_matrix[i][j] = max(0, match, delete, insert)
                # Update the maximum score if necessary
                if score_matrix[i][j] > max_score:
                    max_score = score_matrix[i][j]
        return score_matrix, max_score

    def traceback(self):
        aligned_seq = ""  # Aligned sequence
        aligned_ref = ""  # Aligned reference sequence
        i, j = len(self.seq1), len(self.seq2)  # Starting indices for tracing back
        while i > 0 or j > 0:
            current_score = self.score_matrix[i][j]  # Current score in the score matrix
            # Calculate the score for a match, mismatch, and gap
            match_score = self.score_matrix[i-1][j-1] + (2 if self.seq1[i-1] == self.seq2[j-1] else -1)
            delete_score = self.score_matrix[i-1][j] - 2
            insert_score = self.score_matrix[i][j-1] - 2
            # Check which direction to go and update the aligned sequences accordingly
            if i > 0 and j > 0 and current_score == match_score:
                aligned_seq = self.seq1[i-1] + aligned_seq
                aligned_ref = self.seq2[j-1] + aligned_ref
                i -= 1
                j -= 1
            elif i > 0 and current_score == delete_score:
                aligned_seq = self.seq1[i-1] + aligned_seq
                aligned_ref = "-" + aligned_ref
                i -= 1
            elif j > 0 and current_score == insert_score:
                aligned_seq = "-" + aligned_seq
                aligned_ref = self.seq2[j-1] + aligned_ref
                j -= 1
            else:
                break
        return aligned_seq, aligned_ref

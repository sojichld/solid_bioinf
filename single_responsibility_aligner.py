#!/usr/bin/env python3
import sys
from local import LocalAlignment


class DNASequence:
	def __init__(self, target, reference):
		self.target = target  # Target DNA sequence
		self.reference = reference  # Reference DNA sequence
		self.gc_content = self.calculate_gc_content()  # GC content of the target sequence
		self.length = len(self.target)  # Length of the target sequence
		self.base_counts = self.count_bases()  # Counts of each base in the target sequence

	def calculate_gc_content(self):
		gc_count = self.target.count('G') + self.target.count('C')  # Count of G's and C's in the target sequence
		gc_content = gc_count / len(self.target) * 100  # Calculate the GC content as a percentage
		return gc_content

	def count_bases(self):
		base_counts = {}  # Dictionary to store the counts of each base
		for base in self.target:
			if base in base_counts:
				base_counts[base] += 1
			else:
				base_counts[base] = 1
		return base_counts

	def align_sequences(self):
		aligner = LocalAlignment(self.target, self.reference)
		aligned_target, aligned_ref = aligner.aligned_seq, aligner.aligned_ref
		alignment = ""
		seq_len = len(aligned_target)
		for i in range(0, seq_len, 60):
			alignment += f"{aligned_target[i:min(i+60, seq_len)]}\n"
			alignment += f"{''.join(['|' if aligned_target[i+j] == aligned_ref[i+j] else '-' for j in range(min(60, seq_len-i))])}\n"
			alignment += f"{aligned_ref[i:min(i+60, seq_len)]}\n\n"
		return alignment

class Trimmer:
	def __init__(self, three_bases):
		self.three_bases = three_bases	

	def trimm(self, dna_seq):
		if dna_seq[:3] == self.three_bases and dna_seq[-3:] == self.three_bases[::-1]:
			# Remove the first and last 3 bases from the target sequence if they match the input string of 3 bases
			dna_seq = dna_seq[3:-3]
if __name__ == '__main__':
	# Get the target and reference sequences from the command line arguments
	target_seq = sys.argv[1]
	reference_seq = sys.argv[2]
	adapters = sys.argv[3]
	print(f"Target Sequence: {target_seq}")
	print(f"Length: {reference_seq}")
	trimmer = Trimmer(adapters)
	trimmer.trimm(target_seq)
	print(f"Trimmed target sequence: {target_seq}")

	# Create a DNASequence object with the target and reference sequences
	dna_seq = DNASequence(target_seq, reference_seq)

	# Print the properties of the DNASequence object
	print(f"GC content: {dna_seq.gc_content:.2f}%")
	print(f"Length: {dna_seq.length}")
	print(f"Base counts: {dna_seq.base_counts}")
	print(f"Local alignment:\n{dna_seq.align_sequences()}")


/* 
 * Computing Wikipedia's internal PageRanks
 * 
 * Copyright (c) 2014 Nayuki Minase
 * All rights reserved. Contact Nayuki for licensing.
 * http://nayuki.eigenstate.org/page/computing-wikipedias-internal-pageranks
 */

import java.util.Arrays;


final class Pagerank {
	
	// Links in packed run-length format: (target page ID, number of incoming links, source page IDs...), ...
	private int[] links;
	
	private int idLimit;  // Maximum page ID plus 1. This sets the length of various arrays.
	private boolean[] hasIncomingLinks;
	private int[] numOutgoingLinks;
	private int activePages;  // Number of pages with incoming links or outgoing links (ignore disconnected nodes)
	
	public double[] pageranks;
	private double[] newPageranks;  // Temporary, filled and discarded per iteration
	
	
	
	public Pagerank(int[] links) {
		this.links = links;
		
		// Find highest page ID
		int max = 0;
		for (int i = 0; i < links.length; ) {
			int dest = links[i];
			max = Math.max(dest, max);
			int n = links[i + 1];
			for (int j = 0; j < n; j++) {
				int src = links[i + 2 + j];
				max = Math.max(src, max);
			}
			i += n + 2;
		}
		idLimit = max + 1;
		
		// Initialize metadata
		hasIncomingLinks = new boolean[idLimit];
		numOutgoingLinks = new int[idLimit];
		for (int i = 0; i < links.length; ) {
			int dest = links[i];
			hasIncomingLinks[dest] = true;
			int n = links[i + 1];
			for (int j = 0; j < n; j++) {
				int src = links[i + 2 + j];
				numOutgoingLinks[src]++;
			}
			i += n + 2;
		}
		activePages = 0;
		for (int i = 0; i < idLimit; i++) {
			if (numOutgoingLinks[i] > 0 || hasIncomingLinks[i])
				activePages++;
		}
		
		// Initialize PageRanks uniformly for active pages
		pageranks = new double[idLimit];
		double initWeight = 1.0 / activePages;
		for (int i = 0; i < idLimit; i++) {
			if (numOutgoingLinks[i] > 0 || hasIncomingLinks[i]) {
				pageranks[i] = initWeight;
			}
		}
		newPageranks = new double[idLimit];
	}
	
	
	
	public void iterate(double damping) {
		// Pre-divide by number of outgoing links
		for (int i = 0; i < idLimit; i++) {
			if (numOutgoingLinks[i] > 0)
				pageranks[i] /= numOutgoingLinks[i];
		}
		
		// Distribute PageRanks over links
		Arrays.fill(newPageranks, 0);
		for (int i = 0; i < links.length; ) {
			int n = links[i + 1];
			double sum = 0;
			for (int j = 0; j < n; j++) {
				int src = links[i + 2 + j];
				sum += pageranks[src];
			}
			int dest = links[i];
			newPageranks[dest] = sum;
			i += n + 2;
		}
		
		// Calculate global bias due to pages without outgoing links
		double bias = 0;
		for (int i = 0; i < idLimit; i++) {
			if (hasIncomingLinks[i] && numOutgoingLinks[i] == 0)
				bias += pageranks[i];
		}
		bias /= activePages;
		
		// Apply bias and damping to all active pages
		double temp = bias * damping + (1 - damping) / activePages;  // Factor out some arithmetic
		for (int i = 0; i < idLimit; i++) {
			if (numOutgoingLinks[i] > 0 || hasIncomingLinks[i])
				pageranks[i] = newPageranks[i] * damping + temp;
		}
	}
	
}

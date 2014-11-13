/* 
 * Knuth-Morris-Pratt string matcher (JavaScript)
 * 
 * Copyright (c) 2014 Nayuki Minase
 * http://nayuki.eigenstate.org/page/knuth-morris-pratt-string-matching
 * 
 * (MIT License)
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to
 * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 * the Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 * - The above copyright notice and this permission notice shall be included in
 *   all copies or substantial portions of the Software.
 * - The Software is provided "as is", without warranty of any kind, express or
 *   implied, including but not limited to the warranties of merchantability,
 *   fitness for a particular purpose and noninfringement. In no event shall the
 *   authors or copyright holders be liable for any claim, damages or other
 *   liability, whether in an action of contract, tort or otherwise, arising from,
 *   out of or in connection with the Software or the use or other dealings in the
 *   Software.
 */

"use strict";


// Searches for the given pattern string in the given text string using the Knuth-Morris-Pratt string matching algorithm.
// If the pattern is found, this returns the index of the start of the earliest match in 'text'. Otherwise null is returned.
function kmpSearch(pattern, text) {
	if (pattern.length == 0)
		return 0;  // Immediate match
	
	// Compute longest suffix-prefix table
	var lsp = [0];  // Base case
	for (var i = 1; i < pattern.length; i++) {
		// Start by assuming we're extending the previous LSP
		var j = lsp[i - 1];
		while (true) {
			if (pattern.charAt(i) == pattern.charAt(j)) {
				j++;
				break;
			} else if (j > 0)
				j = lsp[j - 1];
			else  // j == 0
				break;
		}
		lsp.push(j);
	}
	
	// Walk through text string
	var j = 0;  // Number of chars matched in pattern
	for (var i = 0; i < text.length; i++) {
		while (true) {
			if (text.charAt(i) == pattern.charAt(j)) {  // Next char matched, increment position
				j++;
				if (j == pattern.length) {
					return i - (j - 1);
				} else
					break;
			} else if (j > 0) {  // Fall back in the pattern
				j = lsp[j - 1];
			} else  // j == 0
				break;
		}
	}
	return null;  // Not found
}

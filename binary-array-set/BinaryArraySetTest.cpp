/* 
 * Binary array set test (C++)
 * 
 * Copyright (c) 2014 Nayuki Minase
 * http://nayuki.eigenstate.org/page/binary-array-set
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

#include <cstdlib>
#include <ctime>
#include <iostream>
#include <set>
#include "BinaryArraySet.hpp"


// Comprehensively tests all the defined methods against std::set
int main(int argc, char *argv[]) {
	try {
		srand(time(NULL));
		std::set<int> set0;
		BinaryArraySet<int> set1;
		size_t size = 0;
		for (int i = 0; i < 100000; i++) {
			int op = rand() % 100;
			
			if (op < 1) {  // Clear
				set1.checkStructure();
				set0.clear();
				set1.clear();
				size = 0;
				
			} else if (op < 70) {  // Insert
				int n = rand() % 100 + 1;
				for (int j = 0; j < n; j++) {
					int val = rand() % 10000;
					if (!set1.contains(val)) {
						set1.insert(val);
						set0.insert(val);
						size++;
					}
				}
				
			} else if (op < 100) {  // Contains
				int n = rand() % 100 + 1;
				for (int j = 0; j < n; j++) {
					int val = rand() % 10000;
					if (set1.contains(val) != (set0.find(val) != set0.end()))
						throw "Contain test mismatch";
				}
				
			} else
				throw "Invalid random operation";
			
			if (set0.size() != size || set1.size() != size)
				throw "Set size mismatch";
		}
		std::cerr << "Test passed" << std::endl;
		return 0;
		
	} catch (const char *msg) {
		std::cerr << msg << std::endl;
		return 1;
	}
}

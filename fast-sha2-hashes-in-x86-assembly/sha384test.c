/* 
 * SHA-384 hash in C and x86 assembly
 * 
 * Copyright (c) 2014 Nayuki Minase
 * All rights reserved. Contact Nayuki for licensing.
 * http://nayuki.eigenstate.org/page/fast-sha2-hashes-in-x86-assembly
 */

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>


/* Function prototypes */

static int self_check(void);
void sha384_hash(const uint8_t *message, uint32_t len, uint64_t hash[6]);

// Link this program with an external C or x86 compression function
extern void sha512_compress(uint64_t state[8], const uint8_t block[128]);


/* Main program */

int main(int argc, char **argv) {
	if (!self_check()) {
		printf("Self-check failed\n");
		return 1;
	}
	printf("Self-check passed\n");
	
	// Benchmark speed
	uint64_t state[8] = {};
	uint64_t block[16] = {};
	const int N = 3000000;
	clock_t start_time = clock();
	int i;
	for (i = 0; i < N; i++)
		sha512_compress(state, (uint8_t *)block);  // Type-punning
	printf("Speed: %.1f MiB/s\n", (double)N * sizeof(block) / (clock() - start_time) * CLOCKS_PER_SEC / 1048576);
	
	return 0;
}


/* Self-check */

struct testcase {
	uint64_t answer[6];
	const uint8_t *message;
};

#define TESTCASE(a,b,c,d,e,f,msg) {{UINT64_C(a),UINT64_C(b),UINT64_C(c),UINT64_C(d),UINT64_C(e),UINT64_C(f)}, (const uint8_t *)msg}

static struct testcase testCases[] = {
	TESTCASE(0x38B060A751AC9638,0x4CD9327EB1B1E36A,0x21FDB71114BE0743,0x4C0CC7BF63F6E1DA,0x274EDEBFE76F65FB,0xD51AD2F14898B95B, ""),
	TESTCASE(0x54A59B9F22B0B808,0x80D8427E548B7C23,0xABD873486E1F035D,0xCE9CD697E8517503,0x3CAA88E6D57BC35E,0xFAE0B5AFD3145F31, "a"),
	TESTCASE(0xCB00753F45A35E8B,0xB5A03D699AC65007,0x272C32AB0EDED163,0x1A8B605A43FF5BED,0x8086072BA1E7CC23,0x58BAECA134C825A7, "abc"),
	TESTCASE(0x473ED35167EC1F5D,0x8E550368A3DB39BE,0x54639F828868E945,0x4C239FC8B52E3C61,0xDBD0D8B4DE1390C2,0x56DCBB5D5FD99CD5, "message digest"),
	TESTCASE(0xFEB67349DF3DB6F5,0x924815D6C3DC133F,0x091809213731FE5C,0x7B5F4999E463479F,0xF2877F5F2936FA63,0xBB43784B12F3EBB4, "abcdefghijklmnopqrstuvwxyz"),
	TESTCASE(0x09330C33F71147E8,0x3D192FC782CD1B47,0x53111B173B3B05D2,0x2FA08086E3B0F712,0xFCC7C71A557E2DB9,0x66C3E9FA91746039, "abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu"),
};

static int self_check(void) {
	int i;
	for (i = 0; i < sizeof(testCases) / sizeof(testCases[i]); i++) {
		struct testcase *tc = &testCases[i];
		uint64_t hash[6];
		sha384_hash(tc->message, strlen((const char *)tc->message), hash);
		if (memcmp(hash, tc->answer, sizeof(tc->answer)) != 0)
			return 0;
	}
	return 1;
}


/* Full message hasher */

void sha384_hash(const uint8_t *message, uint32_t len, uint64_t hash[6]) {
	uint64_t state[8] = {
		UINT64_C(0xCBBB9D5DC1059ED8),
		UINT64_C(0x629A292A367CD507),
		UINT64_C(0x9159015A3070DD17),
		UINT64_C(0x152FECD8F70E5939),
		UINT64_C(0x67332667FFC00B31),
		UINT64_C(0x8EB44A8768581511),
		UINT64_C(0xDB0C2E0D64F98FA7),
		UINT64_C(0x47B5481DBEFA4FA4),
	};
	
	uint32_t i;
	for (i = 0; len - i >= 128; i += 128)
		sha512_compress(state, message + i);
	
	uint8_t block[128];
	uint32_t rem = len - i;
	memcpy(block, message + i, rem);
	
	block[rem] = 0x80;
	rem++;
	if (128 - rem >= 16)
		memset(block + rem, 0, 120 - rem);
	else {
		memset(block + rem, 0, 128 - rem);
		sha512_compress(state, block);
		memset(block, 0, 120);
	}
	
	uint64_t longLen = ((uint64_t)len) << 3;
	for (i = 0; i < 8; i++)
		block[128 - 1 - i] = (uint8_t)(longLen >> (i * 8));
	sha512_compress(state, block);
	
	memcpy(hash, state, 6 * sizeof(uint64_t));
}

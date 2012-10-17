/*
 * Tiny Encryption Algorithm (TEA) in x86 assembly
 * Copyright (c) 2011 Nayuki Minase
 * 
 * http://nayuki.eigenstate.org/page/tiny-encryption-algorithm-in-x86-assembly
 */


/* void tea_encrypt_x86(uint32_t *msg, uint32_t *key); */
.globl tea_encrypt_x86
tea_encrypt_x86:
	/* Enter */
	pushl  %ebp
	movl   %esp, %ebp
	subl   $12, %esp
	
	/* Preserve callee-save registers */
	movl   %ebx, 0(%esp)
	movl   %esi, 4(%esp)
	movl   %edi, 8(%esp)
	
	/* Load address of message and key */
	movl    8(%ebp), %eax  /* Message */
	movl   12(%ebp), %edx  /* Key */
	
	/* Load message words */
	movl   0(%eax), %esi
	movl   4(%eax), %edi
	
	/* Initialize round constant */
	movl   $0x9E3779B9, %ecx  /* 'sum' */
	
.tea_encrypt_top:
	/* Encrypt 0th message word */
	movl   %edi, %ebx
	shll   $4, %ebx
	addl   0(%edx), %ebx
	leal   (%edi,%ecx), %eax
	xorl   %eax, %ebx
	movl   %edi, %eax
	shrl   $5, %eax
	addl   4(%edx), %eax
	xorl   %eax, %ebx
	addl   %ebx, %esi
	
	/* Encrypt 1st message word */
	movl   %esi, %ebx
	shll   $4, %ebx
	addl   8(%edx), %ebx
	leal   (%esi,%ecx), %eax
	xorl   %eax, %ebx
	movl   %esi, %eax
	shrl   $5, %eax
	addl   12(%edx), %eax
	xorl   %eax, %ebx
	addl   %ebx, %edi
	
	/* Increment */
	addl   $0x9E3779B9, %ecx
	cmpl   $0x6526B0D9, %ecx
	jne    .tea_encrypt_top
	
	/* Store message */
	movl   8(%ebp), %eax
	movl   %esi, 0(%eax)
	movl   %edi, 4(%eax)
	
	/* Restore registers */
	movl   0(%esp), %ebx
	movl   4(%esp), %esi
	movl   8(%esp), %edi
	
	/* Exit */
	addl   $12, %esp
	popl   %ebp
	ret

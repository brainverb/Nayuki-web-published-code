public class Problem021
{
	private static int divisorSum(int n)
	{
		// Finds the sum of integers that evenly divide into n excluding n itself
		int root = (int)Math.sqrt(n);

		int sum = 1;
		for (int i = 2; i <= root; i++)
		{
			if (n % i == 0)
			{
				sum += i;		// Add the divisor & its complement
				if (i * i != n)
					sum += n/i;
			}
		}
		return sum;
	}

	private static boolean isAmicable(int n)
	{
		int nSum = divisorSum(n);
		return n != nSum && divisorSum(nSum) == n;
	}

	public static void main(String[] args)
	{
		long begin = System.currentTimeMillis();

		int sum = 0;
		for (int i = 0; i < 10000; i++)
		{
			if (isAmicable(i))
				sum += i;
		}
		System.out.println(sum);

		long end = System.currentTimeMillis();
		System.out.println((end-begin) + "ms");
	}
}

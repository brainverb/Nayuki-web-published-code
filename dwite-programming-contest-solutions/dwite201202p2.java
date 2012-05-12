// DWITE - February 2012 - Problem 2: Unit rectangles
// Solution by Nayuki Minase


public final class dwite201202p2 extends DwiteSolution {
	
	public static void main(String[] args) {
		DwiteRunner.run("DATA2.txt", "OUT2.txt", new dwite201202p2());
	}
	
	
	protected void runOnce() {
		int n = io.readIntLine();
		int count = 0;
		for (int i = 1; i <= n; i++)
			count += countSmallFactors(i);
		io.println(count);
	}
	
	
	// Counts the number of factors <= sqrt(n) by trial division
	private static int countSmallFactors(int n) {
		int count = 0;
		for (int i = 1, end = DwiteAlgorithm.sqrt(n); i <= end; i++) {
			if (n % i == 0)
				count++;
		}
		return count;
	}
	
}

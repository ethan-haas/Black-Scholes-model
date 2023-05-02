<!DOCTYPE html>
<html>
<body>
	<h1>Documentation for Black-Scholes Model Options Data Analysis</h1>
  <h2>Libraries Used</h2>
<ul>
	<li><code>numpy</code> and <code>pandas</code> are used for data analysis and manipulation.</li>
	<li><code>scipy</code> is used for the <code>norm</code> function to calculate the cumulative distribution function of a normal distribution.</li>
	<li><code>datetime</code> is used to work with dates.</li>
	<li><code>wallstreet</code> is used to extract options data.</li>
</ul>

<h2>Functions Defined</h2>
<h3><code>black_scholes(stock_price, strike_price, time_to_expiry, risk_free_rate, volatility, option_type)</code></h3>
<p>This function calculates the Black-Scholes value of an option, given the stock price, strike price, time to expiry, risk-free rate, volatility, and option type. The function uses the cumulative distribution function of a normal distribution to calculate the option value.</p>
<ul>
	<li><code>stock_price</code>: The current stock price of the underlying asset.</li>
	<li><code>strike_price</code>: The strike price of the option.</li>
	<li><code>time_to_expiry</code>: The time to expiry of the option, in years.</li>
	<li><code>risk_free_rate</code>: The risk-free rate, as a decimal.</li>
	<li><code>volatility</code>: The volatility of the underlying asset, as a decimal.</li>
	 <li><code>option_type</code>: The type of option, either "call" or "put".</li>
</ul>

<h3><code>filter_positive_value_diff(options_df)</code></h3>
<p>This function takes a DataFrame of options data and filters out rows where the value difference (bs_value minus Last Price) is less than or equal to zero.</p>
<ul>
	<li><code>options_df</code>: A DataFrame of options data.</li>
</ul>

<h3><code>process_expiration_date(date)</code></h3>
<p>This function extracts call and put options data for a given expiration date, calculates the Black-Scholes value of each option, and returns two DataFrames: one for calls and one for puts.</p>
<ul>
	<li><code>date</code>: The expiration date of the options, as a datetime object.</li>
</ul>

<h2>Variables Used</h2>
<ul>
	<li><code>ticker</code>: This variable represents the stock symbol for which the options data will be extracted and analyzed.</li>
	<li><code>risk_free_rate</code>: This variable represents the current risk-free rate, as a decimal.</li>
	<li><code>stock_price</code>: This variable represents the current stock price of the underlying asset.</li>
	<li><code>all_calls</code>: This variable is a DataFrame containing all call options data.</li>
	<li><code>all_puts</code>: This variable is a DataFrame containing all put options data.</li>
</ul>

<h2>Main Code Flow</h2>
<ol>
	<li>The <code>Stock</code> object from the <code>wallstreet</code> package is used to extract the current stock price of the underlying asset.</li>
<li>The <code>Call</code> object from the <code>wallstreet</code> package is used to extract a list of expiration dates for the options.</li>
<li>The <code>process_expiration_date</code> function is used with each expiration date in a concurrent thread to extract call and put options data and calculate their Black-Scholes values.</li>
<li>The call and put options data are concatenated into <code>all_calls</code> and <code>all_puts</code> DataFrames.</li>
<li>The value difference for each option is calculated and added to the <code>value_diff</code> column of each DataFrame.</li>
<li>The call and put options data are written to separate sheets in an Excel file using the <code>pd.ExcelWriter</code> object.</li>
<li>The <code>filter_positive_value_diff</code> function is used to filter out call and put options where the value difference is less than or equal to zero.</li>
<li>The most undervalued call and put options are found and printed to the console.</li>
<li>A message is printed to the console indicating that the options data has been saved to an Excel file.</li>
</ol>
<h2>Outputs</h2>
<p>The main outputs of this code are:</p>
<ul>
	<li>A printout of the most undervalued call and put options, if any are found.</li>
	<li>An Excel file with two sheets: one for calls and one for puts.</li>
	<li>A message printed to the console indicating that the options data has been saved to the Excel file.</li>
</ul>

<h2>Example Usage</h2>
<p>To use this code with a different stock symbol, simply change the <code>ticker</code> variable at the beginning of the code to the desired symbol.</p>
<pre><code>ticker = "GOOGL"</code></pre>
<p>To run the code, simply execute the code cell in a Jupyter Notebook or similar environment. The outputs will be printed to the console and an Excel file will be generated in the current working directory.</p>

<h2>Possible Improvements</h2>
<ul>
	<li>The code could be optimized for performance by using a multiprocessing approach instead of a multithreading approach.</li>
	<li>The code could be extended to include more sophisticated option pricing models or volatility models.</li>
</ul>
</body>
</html>

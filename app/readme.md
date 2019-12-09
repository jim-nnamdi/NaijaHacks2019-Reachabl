 ## Decagon-GoStocks

![Screenshot](https://github.com/MetroSpinnin/Decagon-GoStocks/blob/master/static/img/snipp.PNG)

 GoStocks is a generic platform which deals with sales and purchase of stocks in its entirety, in GoStocks users can register accounts and can also login into their accounts and can also update their details, users can also look up different stock prices for different companies in real time as per the data gotten from IEX(investors  exchange platform) through an API. coupled with this, users can buy stocks and also sell too.

 ## IEX API Stock price Lookup

 ![Iex Lookup](https://github.com/MetroSpinnin/Decagon-GoStocks/blob/master/static/img/stockbuy.PNG)

 The API ``https://cloud.iexapis.com/v1/stock/market/batch?&types=quote&symbols={syms}&token=REAL_KEY`` was used to get the quote of different stock prices for various companies, actually i limited the amount to eight(8) ie. the total Number of companies which was listed on the Stock Listings. it was specified to Alibaba, Boeing CO, Tesla, Apple, Facebook, Alphabet(Google). This API's data is returned and tabulated as shown above.

## IEX API to Buy Stocks

![Screenshot](https://github.com/MetroSpinnin/Decagon-GoStocks/blob/master/static/img/buystock.PNG)

Firstly, for making the user to purchase a stock, i sent a get request to the Cloud IEX Api to pull the data from the platform and then rendered it via a select element to the use-end for dynamic selection. Here i selected just six companies.

```
'''

Buy Stocks Page for user

'''
@app.route('/buystock')
def buystock():
re = requests.get('https://cloud.iexapis.com/v1/stock/market/batch?&types=quote&symbols=aapl,fb,googl,tsla,ba,baba&token=sk_61cb076ca68543428e7b04ee40f3c574')
data = re.json()
return render_template('buystock.html', quote = data)
```

So in the user end template view, i had to just run a for loop inside the elements to make the users select their choice of company shares and the corresponding Price gotten from the API attributed to a certain company and its related latest price in real time.

```
<form method="post" action="{{url_for('completedstock')}}">
<div class="form-group col-md-6">

<!-- The select form which captures API return data for company -->

<select name="symbol" class="form-control col-md-12">
<option>Select the company</option>
{%for company in quote %}
<option>{{quote[company]['quote'].symbol}}</option>
{%endfor%}
</select>
</div>

'''
Second select element

'''

<div class="form-group col-md-6">

<!-- The select form which captures API return data for company -->

<select name="amount" class="form-control col-md-12">
<option>Select the Price</option>
{%for company in quote %}
<option>{{quote[company]['quote'].symbol}} {{quote[company]['quote'].latestPrice}}</option>
{%endfor%}
</select>
</div>
</form>
```
When the data from the API is returned, i just created a form which passes the data gotten from the API into the select element, the select element carries the forloop which pulls all the data categorically to the form for use, so the data is automatically populated for the end user to choose.

![Stocks bought by user](https://github.com/MetroSpinnin/Decagon-GoStocks/blob/master/static/img/cstocks.PNG)

Basically before the user can buy stocks as per the design, the user needs to have funds in the account and then use it (the already generated funds) to purchase the stock, no dollar to naira equiv calculation yet.

## FundAccount & Balance

![User's Dashboard and funds](https://github.com/MetroSpinnin/Decagon-GoStocks/blob/master/static/img/funding.PNG)

Here in the user dashboard, the user can fund account either using paypal or even a custom miniature form that collects needed data and then returns a dummy amount into the database, the data is then transferred to the database and then thrown to the user's dashboard on return.

For integrating paypal into the application, i created a paypal account and then returned the values needed via the form with return values and needed parameters too, as shown below (paypal account still under approval pending though) even through the sandbox.

```
<form name="topaypal" action="https://www.sandbox.paypal.com/cgi-bin/webscr" method="post" class="wfont">
<input type="hidden" name="cmd" value="_xclick-subscriptions">
<input type="hidden" name="custom" value="{{session['username']}}"/>
<input type="hidden" name="business" value="jimsamuel50@gmail.com">
<input type="hidden" name="item_name" value="subscription button">
<input type="hidden" name="item_number" value="500">
<input type="hidden" name="no_shipping" value="1">
<input type="hidden" name="a3" value="1000.00">
<input type="hidden" name="p3" value="1">
<input type="hidden" name="t3" value="M">
<input type="hidden" name="src" value="1">
<input type="hidden" name="sra" value="1">
<input type="hidden" name="return" value="http://104.236.221.91/success/">
<input type="hidden" name="cancel_return" value="http://104.236.221.91/">
<input type="hidden" name="notify_url" value="http://104.236.221.91/ipn/">
<input type="submit" value="Fund Using PayPal" name="submit" title="PayPal - The safer, easier way to pay online!" class="btn large btn primary" style="margin-top: 3px; color:darkgreen">
</form>
```

## How to use

 If you already have Python installed on your computer system, regardless of the version but at least >= v.2.7.16 you can straightway clone the repo, and run on your system after initiating your virtual environment, the project uses some specs which would be clearly classified in the requirements.txt file
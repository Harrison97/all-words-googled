# all-words-googled
Twitter Bot

See the bot at : https://twitter.com/AllWordsGoogled


This is built with Node.js and Python with Selenium.



How to use for yourself locally(only tested in windows):
    create a config.js in the main folder

config.json
    //config


    module.exports = {
	
	    consumer_key:         'your key',
	    consumer_secret:      'your secret',
	    access_token:         'your access token',
	    access_token_secret:  'your access token secret',
	    timeout_ms:           60*1000,  // optional HTTP request timeout to apply to all requests. 
	}


npm install

pip install -r requirements.txt

node bot.js
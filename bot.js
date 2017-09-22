
console.log("bot.js is starting.");

var Twit = require('twit');
var fs = require('fs');

var config = require('./config.js');
var T = new Twit(config);



// var tweet = {
// 	status: 'testing'
// }
// T.post('statuses/update', tweet, tweeted);
// function tweeted(err, data, response) {
//   // console.log(data)
// }

// var x = 5;
// tweetIt;
// setInterval(tweetIt, 1000*10)
// function tweetIt() {
// 	T.post('statuses/update', {status: 'testing..'}, tweeted);
// 	function tweeted(err, data, response) {
//   		// console.log(x)
// 	}
// 	// x++;
// }
tweetIt();
setInterval(tweetIt, 1000*30)
function tweetIt(){
	var spawnSync = require("child_process").spawnSync;
	var process = spawnSync('python',["scraper.py"]);
	console.log("py scraper.py")
	data = JSON.parse(fs.readFileSync('data.json'))
	var pic = fs.readFileSync(data.filename, { encoding: 'base64' })
	var tweet = data.tweet;
	// first we must post the media to Twitter 
	T.post('media/upload', { media_data: pic }, function (err, data, response) {
	  // now we can assign alt text to the media, for use by screen readers and 
	  // other text-based presentations and interpreters 
	  var mediaIdStr = data.media_id_string
	  var altText = "(alt text.)"
	  var meta_params = { media_id: mediaIdStr, alt_text: { text: altText } }
	 
	  T.post('media/metadata/create', meta_params, function (err, data, response) {
	    if (!err) {
	      // now we can reference the media and post a tweet (media will attach to the tweet) 
	      var params = { status: tweet, media_ids: [mediaIdStr] }
	 
	      T.post('statuses/update', params, function (err, data, response) {
	        // console.log(data)
	      })
	    }
	  })
	})
	console.log("Posted.")
}




// https://www.google.com/search?tbm=isch&q=findSomeImage

console.log("bot.js is ending.");
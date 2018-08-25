const secrets = require('./secrets.json');
const googleTranslate = require('google-translate')(secrets.apiKey);

function translateText(text, fromLanguage, toLanguage) {
	return new Promise((resolve, reject) => {
		googleTranslate.translate(text, fromLanguage, toLanguage, (err, translation) => {
			if (err !== null) {
				reject(err);
			}
			else {
	 			resolve(translation.translatedText);
			}
		});
	});
}

// Example
translateText('I like apples and oranges', 'en', 'es')
	.then((res) => {
		console.log(res);
	})
	.catch((res) => {
		console.log(res);
	});

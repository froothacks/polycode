const googleTranslate = require('google-translate')(process.env.apiKey);

// module.exports = (tokens, dictionary, callback) => {
module.exports = (word = "", fromLanguage, toLanguage, callback) => {
  googleTranslate.translate(word, fromLanguage, toLanguage, (err, translation) => {
    if (err !== null) {
      callback(err, null);
    }
    else {
      console.log(translation.translatedText)
      callback(null, translation.translatedText);
    }
  });
};

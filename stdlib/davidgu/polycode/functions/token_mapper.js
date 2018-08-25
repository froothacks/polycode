const googleTranslate = require('google-translate')(process.env.apiKey);
const lib = require('lib');
const Case = require('case');
module.exports = async (tokens = ["BANANAS_APPLES_ORANGES", "camelCase", "AppleBanana", "david-case", "snakey_boi", "apple", "pineapple"], dictionary = "apple pomme\npineapple ananas", to="ES", from="EN", context) => {
  String.prototype.replaceAll = function(find, replace) {
    return this.split(find).join(replace);
  }
  const dictionaryObj = JSON.parse(`{"${dictionary.replaceAll(" ", "\":\"").replaceAll('\n', '", "')}"}`)
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
  const allPromises = [];
  for (let i = 0; i < tokens.length; i++) {
    allPromises.push(translateText(Case.lower(tokens[i]), from, to));
  }
  const results = await Promise.all(allPromises);
  results.forEach((item, i) => {
    results[i] = Case[Case.of(tokens[i])](item);
  });
  return results;
};

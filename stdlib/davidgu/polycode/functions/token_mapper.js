const googleTranslate = require('google-translate')(process.env.apiKey);
const lib = require('lib');
const Case = require('case');

/**
* @param {string} to
* @param {string} from
* @param {array} tokens
* @param {object} dictionary
* @returns {array}
*/

module.exports = async (to, from, tokens, dictionary, context) => {
  const allPromises = [];

  const toLangIdx = dictionary.languages.indexOf(to);
  const fromLangIdx = dictionary.languages.indexOf(from);

  for (let i = 0; i < tokens.length; i++) {
    let inDict = false;
    dictionary.tokens.forEach(entry => { // as in dictionary entry
      if (entry[fromLangIdx] === tokens[i].value) {
        tokens[i].translated = entry[toLangIdx];
        inDict = true;
      }
    });
    if (!inDict) {
      allPromises.push(translateText(Case.lower(tokens[i].value), from, to));
    }
  }
  const results = await Promise.all(allPromises);
  results.forEach((item, i) => {
    tokens[i].translated = Case[Case.of(tokens[i].value)](item);
  });
  console.log(results)
  return tokens;

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
};

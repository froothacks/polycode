const googleTranslate = require('google-translate')(process.env.apiKey);
const lib = require('lib');
const Case = require('case');

/**
* @param {string} to
* @param {string} from
* @param {array} tokens
* @param {object} map
* @returns {array}
*/
module.exports = async (to, from, tokens, map, context) => {
  const allPromises = [];

  var toLangIdx = 1;
  var fromLangIdx = 0;

  if (map["languages"]) {
    toLangIdx = map["languages"].indexOf(to);
    fromLangIdx = map["languages"].indexOf(from);
  }

  for (let i = 0; i < tokens.length; i++) {
    let inDict = false;
    if (map["tokens"]) {
      map["tokens"].forEach(entry => {
        if (entry[fromLangIdx] === tokens[i].value) {
          tokens[i].translated = entry[toLangIdx];
          inDict = true;
        }
      });
    }
    if (!inDict) {
      allPromises.push(translateText(Case.lower(tokens[i].value), from, to));
    }
  }
  const results = await Promise.all(allPromises);
  results.forEach((item, i) => {
    tokens[i].translated = Case[Case.of(tokens[i].value)](item);
  });
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

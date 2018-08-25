const googleTranslate = require('google-translate')(process.env.apiKey);
const lib = require('lib');
const Case = require('case');

/**
* @param {array} tokens
* @param {string} from
* @param {string} to
* @param {object} map
* @returns {object} 
*/
module.exports = async (tokens, from, to, map) => {
  const allPromises = [];

  var fromLangIdx, toLangIdx;

  if (!map["languages"]) {
    map["languages"] = []
  }

  if (!map["tokens"]) {
    map["tokens"] = []
  }

  fromLangIdx = map["languages"].indexOf(from);
  toLangIdx = map["languages"].indexOf(to);
  if (fromLangIdx === -1) { // from language not found
    fromLangIdx = map["languages"].length;
    map["languages"].push(from);
    map["tokens"].forEach(row => {row.add(null)});
  }
  if (toLangIdx === -1) { // to language not found
    toLangIdx = map["languages"].length;
    map["languages"].push(to);
    map["tokens"].forEach(row => {row.add(null)});
  }

  console.log("map")
  console.log(map)

  for (let i = 0; i < tokens.length; i++) {
    let inDict = false;
    map["tokens"].forEach(row => {
      if (row[toLangIdx] && row[fromLangIdx] === tokens[i].value) {
        tokens[i].translated = row[toLangIdx];
        inDict = true;
      }
    });
    if (!inDict) {
      allPromises.push(translateText(Case.lower(tokens[i].value), from, to));
    }
  }
  const results = await Promise.all(allPromises);
  results.forEach((item, i) => {
    origToken = tokens[i].value;
    tokens[i].translated = Case[Case.of(origToken)](item);
    var found = false;
    for (var i = 0; i < map["tokens"].length; i++) {
      if (map["tokens"][i][fromLangIdx] === origToken) {
        map["tokens"][i][toLangIdx] = tokens[i].translated;
        found = true;
        break;
      }
    }
    if (!found) {
      row = new Array(map["languages"].length).fill(null);
      row[fromLangIdx] = origToken;
      row[toLangIdx] = tokens[i].translated;
      map["tokens"].push(row);
    }
  });
  console.log("tokens", tokens);
  return {"tokens": tokens, "map": map};

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

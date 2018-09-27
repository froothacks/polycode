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
    map["tokens"].forEach(row => {row.push(null)});
  }
  if (toLangIdx === -1) { // to language not found
    toLangIdx = map["languages"].length;
    map["languages"].push(to);
    map["tokens"].forEach(row => {row.push(null)});
  }

  for (let i = 0; i < tokens.length; i++) {
    let inDict = false;
    map["tokens"].forEach(row => {
      if (row[toLangIdx] && row[fromLangIdx] === tokens[i].value) {
        tokens[i].translated = row[toLangIdx];
        inDict = true;
      }
    });
    if (!inDict) {
      var value = tokens[i].value;
      if (!tokens[i].isComment) {
        value = Case.lower(value);
      }
      allPromises.push(translateText(value, i, from, to));
    }
  }
  var results = await Promise.all(allPromises);
  results.forEach(result => {
    token = tokens[result["index"]];
    origValue = result["origValue"]
    var translated = result["translated"];
    if (!token.isComment) {
      translated = Case[Case.of(origValue)](translated).split(" ").join("_");
    }
    token.translated = translated;

    // Update map with new language translation of a token that 
    var found = false;
    for (var j = 0; j < map["tokens"].length; j++) {
      if (map["tokens"][j][fromLangIdx] === origValue) {
        map["tokens"][j][toLangIdx] = translated;
        found = true;
        break;
      }
    }
    if (!found) {
      // Completely new token: push new row
      row = new Array(map["languages"].length).fill(null);
      row[fromLangIdx] = origValue;
      row[toLangIdx] = translated;
      map["tokens"].push(row);
    }
  });
  
  return {"tokens": tokens, "map": map};

  function translateText(value, index, fromLanguage, toLanguage) {
    return new Promise((resolve, reject) => {
      googleTranslate.translate(value, fromLanguage, toLanguage, (err, translation) => {
        if (err !== null) {
          reject(err);
        }
        else {
          resolve({
            "index": index,
            "origValue": value,
            "translated": translation.translatedText
          });
        }
      });
    });
  }
};

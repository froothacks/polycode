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
      allPromises.push(translateToken(tokens[i], i, from, to));
    }
  }
  var results = await Promise.all(allPromises);
  results.forEach(result => {
    var token = result.token;
    tokens[result.index] = token;

    // Update map with new language translation of a token that 
    var found = false;
    for (var j = 0; j < map["tokens"].length; j++) {
      if (map["tokens"][j][fromLangIdx] === token.value) {
        map["tokens"][j][toLangIdx] = token.translated;
        found = true;
        break;
      }
    }
    if (!found) {
      // Completely new token: push new row
      row = new Array(map["languages"].length).fill(null);
      row[fromLangIdx] = token.value;
      row[toLangIdx] = token.translated;
      map["tokens"].push(row);
    }
  });
  
  return {"tokens": tokens, "map": map};

  function translateToken(token, index, fromLanguage, toLanguage) {
    return new Promise((resolve, reject) => {
      if (token.value.length === 1) {
        token.translated = token.value;
        resolve({"index": index, "token": token});
      }
      var text = token.value;
      if (!token.isComment) {
        text = Case.lower(text);
      }
      googleTranslate.translate(text, fromLanguage, toLanguage, (err, translation) => {
        if (err !== null) {
          reject(err);
        }
        else {
          var translated = translation.translatedText;
          if (!token.isComment) {
            translated = Case[Case.of(token.value)](translated).split(" ").join("_");
          }
          token.translated = translated;

          resolve({"index": index, "token": token});
        }
      });
    });
  }
};

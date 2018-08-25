const googleTranslate = require('google-translate')(process.env.apiKey);
const lib = require('lib');

// module.exports = (tokens, dictionary, callback) => {
module.exports = (tokens = ["bananas", "camelCase", "PascalCase", "david-case", "snakey_boi", "apple", "pineapple"], dictionary = "apple pomme\npineapple ananas", to="EN", from="ES", context, callback) => {
  String.prototype.replaceAll = function(find, replace) {
    return this.split(find).join(replace);
  }

  const result = [];
  const dictionaryObj = JSON.parse(`{"${dictionary.replaceAll(" ", "\":\"").replaceAll('\n', '", "')}"}`)

  for (let i = 0; i < tokens.length; i++) {
    let token = tokens[i];

    if (dictionaryObj['token']) {
      result.push(dictionaryObj['token'])
    } else {
      if (checkCase(token) === "cute") {
        console.log("NTH")
        translate(token, function(res) {
          console.log(res)
          result.push(res);
        });
        // lib[`${context.service.identifier}.translate_word`](token, from, to, (err, res) => {
        //   console.log(err, res)
        // })
        // googleTranslate.translate(token, from, to, (err, translation) => {
        //   result.push(translation)
        // });
      } else {
        let words = token.split(/\-|_/);
        for (let j = 0; j < words.length; j++) {
          let word = words[j];
          // x = translateText(word, from, to).then(res => {
          //   // token.replace(word, lib[`${context.service.identifier}.translate_word`](word));
          // }).catch(err => { console.log(err) })
        }
        result.push(token);
      }
    }
  }
  callback(null, result);


  async function translate(word, callback) {
    lib[`${context.service.identifier}.translate_word`](word, from, to, (err, res) => {
      return [err, res]
    })
  }
  function checkCase(token) {
    for (var i = 0; i < token.length; i++) {
      let char = token.charAt(i);
      if (char === char.toUpperCase()) {
        return "camel";
      } else if (char === '_') {
        return "snake";
      } else if (char === "-") {
        return "david"
      } else {
        return "cute";
      }
    }
  }
};

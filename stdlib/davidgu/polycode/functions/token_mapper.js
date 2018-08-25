// module.exports = (tokens, dictionary, callback) => {
module.exports = (tokens = ["bananas", "camelCase", "PascalCase", "david-case", "snakey_boi", "apple", "pineapple"], dictionary = "apple pomme\npineapple ananas", callback) => {
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
        // result.push(lib[`${context.service.identifier}.translate_word`](token))
      } else {
        let words = token.split(/\-|_/);
        for (let j = 0; j < words.length; j++) {
          let word = words[j];
          // token.replace(word, lib[`${context.service.identifier}.translate_word`](word))
        }
        // result.push(token); 
      }
    }
  }
  callback(null, result);



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

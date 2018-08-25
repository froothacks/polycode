const filbert = require("filbert");

/**
* @param {string} doc
* @returns {array} tokens
*/
module.exports = async (doc) => {
  var tokens = [];

  var nextToken = filbert.tokenize(doc);

  var t = nextToken();
  while (t["type"]["type"] !== "eof") {
    if (t["type"]["type"] === "name") {
      tokens.push(Object.assign({}, t));
    }
    t = nextToken();
  }

  return tokens;
};

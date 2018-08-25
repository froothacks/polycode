const filbert = require("filbert");

/**
* @param {string} doc
* @returns {array} tokens
*/
module.exports = (doc, callback) => {
  tokens = [];

  nextToken = filbert.tokenize(doc);

  t = nextToken();
  while (t.type.type !== "eof") {
    if (t.type.type === "name") {
      tokens.push(t);
    }
    t = nextToken();
  }

  callback(null, tokens);
};

const filbert = require("filbert");

/**
* @param {string} doc
* @returns {array} tokens_
*/
module.exports = (doc, callback) => {
  var tokens_ = [];

  var nextToken = filbert.tokenize(doc);

  var t = nextToken();
  while (t["type"]["type"] !== "eof") {
    if (t["type"]["type"] === "name") {
      tokens_.push(Object.assign({}, t));
    }
    t = nextToken();
  }


  callback(null, tokens_);
};

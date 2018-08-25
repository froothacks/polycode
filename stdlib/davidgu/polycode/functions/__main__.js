const lib = require("lib");

/**
* @param {string} doc Plaintext of the document to be translated
* @param {object} config
* @param {object} map
* @returns {any}
*/
module.exports = (doc="", config, map, context, callback) => {
  lib.davidgu.polycode.get_tokens(doc, (err, tokens) => {
    for (var token in tokens) token.translated = "ttt";
    lib.davidgu.polycode.update_docs(doc, tokens, (err, doc) => {
      callback(null, doc);
    });
  });
};

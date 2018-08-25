const lib = require("lib");

/**
* @param {string} doc Plaintext of the document to be translated
* @param {object} config
* @param {object} map
* @returns {any}
*/
module.exports = (doc="", config, map, context, callback) => {
  lib[`${context.service.identifier}.get_tokens`](doc, (err, tokens) => {
    for (var token in tokens) token.translated = "ttt";
    lib[`${context.service.identifier}.update_docs`](doc, tokens, (err, doc) => {
      callback(null, doc);
    });
  });
};

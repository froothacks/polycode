const lib = require("lib");

/**
* @param {string} doc Plaintext of the document to be translated
* @param {object} config
* @param {object} map
* @returns {any}
*/
module.exports = (doc, config={"to": "FR", "from": "EN"}, map={}, context, callback) => {
  console.log(context.service.identifier)
  lib[`${context.service.identifier}.get_tokens`](doc, (err, tokens) => {
    lib[`${context.service.identifier}.token_mapper`](config.to, config.from, tokens, map, (err, tokens) => {
      lib[`${context.service.identifier}.update_doc`](doc, tokens, (err, doc) => {
        callback(err, doc);
      });
    });
  });
};

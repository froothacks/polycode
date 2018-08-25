const lib = require("lib");

/**
* @param {string} doc Plaintext of the document to be translated
* @param {object} config
* @param {object} map
* @returns {any}
*/

const test_config = {
  "to": "FR",
  "from": "EN"
}
module.exports = (doc="testPotato banana", config, map, context, callback) => {
  console.log(context.service.identifier)
  lib[`${context.service.identifier}.get_tokens`](doc, (err, tokens) => {
    lib[`${context.service.identifier}.token_mapper`](test_config.to, test_config.from, tokens, JSON.parse(map), (err, tokens) => {
      lib[`${context.service.identifier}.update_doc`](doc, tokens, (err, doc) => {
        callback(null, doc);
      });
    });
  });
};

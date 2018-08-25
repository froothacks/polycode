const lib = require("lib");

/**
* @param {string} doc Plaintext of the document to be translated
* @param {string} from ISO 639-1 language code for 
* @param {string} to
* @param {object} map
* @returns {any} 
*/
module.exports = async (doc, from="EN", to="FR", map={}, context) => {
  var tokens = await lib[`${context.service.identifier}.get_tokens`](doc);
  var result = await lib[`${context.service.identifier}.token_mapper`](tokens, from, to, map);
  tokens = result[0];
  map = result[1];
  doc = await lib[`${context.service.identifier}.update_doc`](doc, tokens);

  return {"doc": doc, "map": map}
};

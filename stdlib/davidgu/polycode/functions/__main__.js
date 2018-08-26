const lib = require("lib");

/**
* @param {string} doc Plaintext of the document to be translated
* @param {string} from ISO 639-1 language code for 
* @param {string} to
* @param {object} map
* @returns {any} 
*/
module.exports = async (doc, from="EN", to="FR", map={}, scriptlang="python", context) => {
  var tokens = await lib[`${context.service.identifier}.get_tokens`](doc, scriptlang);
  var result = await lib[`${context.service.identifier}.token_mapper`](tokens, from, to, map);
  tokens = result["tokens"];
  map = result["map"];
  doc = await lib[`${context.service.identifier}.update_doc`](doc, tokens);

  return {"doc": doc, "map": map}
};

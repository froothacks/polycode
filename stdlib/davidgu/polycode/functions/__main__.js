const lib = require("lib");

/**
* @param {string} doc   Plaintext of the document to be translated
* @param {string} from  2-letter code of language to translate from
* @param {string} to    2-letter code of language to be translate into
* @param {string} map   JSON-stringified string of map file
* @param {string} ext   File extension of doc
* @returns {object} 
*/
module.exports = async (doc, from="EN", to="FR", map="{}", ext=".py", context) => {
  map = JSON.parse(map);
  var lang = langForExt[ext];
  var tokens = await lib[`${context.service.identifier}.get_tokens`](doc, lang);
  var result = await lib[`${context.service.identifier}.token_mapper`](tokens, from, to, map);
  tokens = result["tokens"];
  map = result["map"];
  doc = await lib[`${context.service.identifier}.update_doc`](doc, tokens);

  return {"doc": doc, "map": map}
};

langForExt = {
  ".py": "python",
  ".js": "javascript",
  ".jsx": "javascript"
}

/**
* @param {string} doc
* @param {object} tokens
* @returns {string} doc
*/
module.exports = (doc, tokens, callback) => {
  offset = 0;

  for (var token in tokens) {
    before = doc.slice(0, t.start + offset);
    after = doc.slice(t.end + offset);

    offset += token.translated.length - (t.end - t.start);

    doc = before + token.translated + after;
  }

  callback(null, doc);
};

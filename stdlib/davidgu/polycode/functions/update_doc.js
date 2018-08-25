/**
* @param {string} doc
* @param {array} tokens
* @returns {string} doc
*/
module.exports = (doc, tokens, callback) => {
  offset = 0;

  tokens.forEach(t => {
    before = doc.slice(0, t.start + offset);
    after = doc.slice(t.end + offset);

    offset += t.translated.length - (t.end - t.start);

    doc = before + t.translated + after;
  });

  callback(null, doc);
};

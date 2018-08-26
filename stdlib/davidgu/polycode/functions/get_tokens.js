const filbert = require("filbert");

/**
* @param {string} doc
* @param {string} lang
* @returns {array} tokens
*/
module.exports = async (doc, lang="python") => {
  if (!(lang in getTokensForLang)) lang = "python";
  return getTokensForLang[lang](doc);
};

getTokensForLang = {
  "python": function(doc) {
    var tokens = [];

    var nextToken = filbert.tokenize(doc);

    var t = nextToken();
    while (t["type"]["type"] !== "eof") {
      if (t["type"]["type"] === "name") {
        tokens.push(Object.assign({}, t));
      }
      t = nextToken();
    }

    // Iterate through looking for comments

    var runningLength = 0;

    doc.split("\n").forEach(line => {
      var hash = line.indexOf("#");
      if (hash !== -1) {

        var start = hash + 1;
        while (line.charAt(start) == " ") start++;

        var text = line.slice(start);
        tokens.push({
          "value": text,
          "start": start + runningLength,
          "end": runningLength + line.length,
          "isComment": true
        });
      }
      runningLength += line.length + 1; // + 1 for newline
    });

    tokens.sort((a, b) => {return a["start"] - b["start"]});

    return tokens;
  },

  "javascript": function(doc) {
    var tokens = [];

    for (let token of acorn.tokenizer(doc)) {
      if (token.type.label === "name") {
        tokens.push({
          start: token.start,
          end: token.end,
          value: token.value,
          type: { type: token.type.label }
        });
      }
    }

    var runningLength = 0;

    doc.split("\n").forEach(line => {
      var hash = line.indexOf("//");
      if (hash !== -1) {

        var start = hash + 2;
        while (line.charAt(start) == " ") start++;

        var text = line.slice(start);
        tokens.push({
          "value": text,
          "start": start + runningLength,
          "end": runningLength + line.length,
          "isComment": true
        });
      }
      runningLength += line.length + 1; // + 1 for newline
    });

    tokens.sort((a, b) => {return a["start"] - b["start"]});
    return tokens;
  }
}

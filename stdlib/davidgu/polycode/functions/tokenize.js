filbert = require("filbert");

function processDoc(doc) {
  nextToken = filbert.tokenize(doc);

  t = nextToken();

  offset = 0;

  while (t.type.type !== "eof") {
    if (t.type.type === "name") {
      newToken = "`" + t.value + "`";

      before = doc.slice(0, t.start + offset);
      after = doc.slice(t.end + offset);

      offset += newToken.length - (t.end - t.start);

      doc = before + newToken + after;
    }

    t = nextToken();
  }

  return doc;
}

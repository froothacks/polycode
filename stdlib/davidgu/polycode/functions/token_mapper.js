const googleTranslate = require('google-translate')(process.env.apiKey);
const lib = require('lib');
const Case = require('case');

/**
* @param {array} tokens
* @param {string} from
* @param {string} to
* @param {object} map
* @returns {object} 
*/
module.exports = async (tokens, from, to, map) => {
  const allPromises = [];

  var fromLangIdx, toLangIdx;

  if (!map["languages"]) {
    map["languages"] = []
  }

  if (!map["tokens"]) {
    map["tokens"] = []
  }

  fromLangIdx = map["languages"].indexOf(from);
  toLangIdx = map["languages"].indexOf(to);
  if (fromLangIdx === -1) { // from language not found
    fromLangIdx = map["languages"].length;
    map["languages"].push(from);
    map["tokens"].forEach(row => {row.push(null)});
  }
  if (toLangIdx === -1) { // to language not found
    toLangIdx = map["languages"].length;
    map["languages"].push(to);
    map["tokens"].forEach(row => {row.push(null)});
  }

  for (let i = 0; i < tokens.length; i++) {
    let inDict = false;
    map["tokens"].forEach(row => {
      if (row[toLangIdx] && row[fromLangIdx] === tokens[i].value) {
        tokens[i].translated = row[toLangIdx];
        inDict = true;
      }
    });
    if (!inDict) {
      var text = tokens[i].value;
      if (!tokens[i]["isComment"]) {
        Case.lower(text);
      }
      allPromises.push(translateText(text, from, to));
    }
  }
  const results = await Promise.all(allPromises);
  results.forEach((item, i) => {
    origToken = tokens[i].value;
    
    var text = item;
    if (!tokens[i]["isComment"]) {
      Case.lower(text);
    }
    tokens[i].translated = Case[Case.of(origToken)](item).split(" ").join("_");
    var found = false;
    for (var i = 0; i < map["tokens"].length; i++) {
      if (map["tokens"][i][fromLangIdx] === origToken) {
        map["tokens"][i][toLangIdx] = tokens[i].translated;
        found = true;
        break;
      }
    }
    if (!found) {
      row = new Array(map["languages"].length).fill(null);
      row[fromLangIdx] = origToken;
      row[toLangIdx] = tokens[i].translated;
      map["tokens"].push(row);
    }
  });
  
  return {"tokens": tokens, "map": map};

  function translateText(text, fromLanguage, toLanguage) {
    return new Promise((resolve, reject) => {
      googleTranslate.translate(text, fromLanguage, toLanguage, (err, translation) => {
        if (err !== null) {
          reject(err);
        }
        else {
          resolve(translation.translatedText);
        }
      });
    });
  }
};
if (typeof TKK !== 'undefined') {
                        window.TKK = TKK;
                        // config.set('TKK', TKK);
                    }
                    /* eslint-enable no-undef */
                }

                /**
                 * Note: If the regex or the eval fail, there is no need to worry. The server will accept
                 * relatively old seeds.
                 */

                resolve();
            }).catch(function (err) {
                var e = new Error();
                e.code = 'BAD_NETWORK';
                e.message = err.message;
                reject(e);
            });
        }
    });
}

function get(text) {
    return updateTKK().then(function () {
        var tk = sM(text);
        tk = tk.replace('&tk=', '');
        return {name: 'tk', value: tk};
    }).catch(function (err) {
        throw err;
    });
}

/**
 *
 * Generated from https://translate.google.com
 *
 * The languages that Google Translate supports (as of 5/15/16) alongside with their ISO 639-1 codes
 * See https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
 */
var langs = {
    'auto': 'Automatic',
    'af': 'Afrikaans',
    'sq': 'Albanian',
    'am': 'Amharic',
    'ar': 'Arabic',
    'hy': 'Armenian',
    'az': 'Azerbaijani',
    'eu': 'Basque',
    'be': 'Belarusian',
    'bn': 'Bengali',
    'bs': 'Bosnian',
    'bg': 'Bulgarian',
    'ca': 'Catalan',
    'ceb': 'Cebuano',
    'ny': 'Chichewa',
    'zh-cn': 'Chinese Simplified',
    'zh-tw': 'Chinese Traditional',
    'co': 'Corsican',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'en': 'English',
    'eo': 'Esperanto',
    'et': 'Estonian',
    'tl': 'Filipino',
    'fi': 'Finnish',
    'fr': 'French',
    'fy': 'Frisian',
    'gl': 'Galician',
    'ka': 'Georgian',
    'de': 'German',
    'el': 'Greek',
    'gu': 'Gujarati',
    'ht': 'Haitian Creole',
    'ha': 'Hausa',
    'haw': 'Hawaiian',
    'iw': 'Hebrew',
    'hi': 'Hindi',
    'hmn': 'Hmong',
    'hu': 'Hungarian',
    'is': 'Icelandic',
    'ig': 'Igbo',
    'id': 'Indonesian',
    'ga': 'Irish',
    'it': 'Italian',
    'ja': 'Japanese',
    'jw': 'Javanese',
    'kn': 'Kannada',
    'kk': 'Kazakh',
    'km': 'Khmer',
    'ko': 'Korean',
    'ku': 'Kurdish (Kurmanji)',
    'ky': 'Kyrgyz',
    'lo': 'Lao',
    'la': 'Latin',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'lb': 'Luxembourgish',
    'mk': 'Macedonian',
    'mg': 'Malagasy',
    'ms': 'Malay',
    'ml': 'Malayalam',
    'mt': 'Maltese',
    'mi': 'Maori',
    'mr': 'Marathi',
    'mn': 'Mongolian',
    'my': 'Myanmar (Burmese)',
    'ne': 'Nepali',
    'no': 'Norwegian',
    'ps': 'Pashto',
    'fa': 'Persian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'ma': 'Punjabi',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sm': 'Samoan',
    'gd': 'Scots Gaelic',
    'sr': 'Serbian',
    'st': 'Sesotho',
    'sn': 'Shona',
    'sd': 'Sindhi',
    'si': 'Sinhala',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'so': 'Somali',
    'es': 'Spanish',
    'su': 'Sundanese',
    'sw': 'Swahili',
    'sv': 'Swedish',
    'tg': 'Tajik',
    'ta': 'Tamil',
    'te': 'Telugu',
    'th': 'Thai',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'uz': 'Uzbek',
    'vi': 'Vietnamese',
    'cy': 'Welsh',
    'xh': 'Xhosa',
    'yi': 'Yiddish',
    'yo': 'Yoruba',
    'zu': 'Zulu'
};

function translate(text, opts) {
    opts = opts || {};

    var e;
    [opts.from, opts.to].forEach(function (lang) {
        if (lang && !isSupported(lang)) {
            e = new Error();
            e.code = 400;
            e.message = 'The language \'' + lang + '\' is not supported';
        }
    });
    if (e) {
        return new Promise(function (resolve, reject) {
            reject(e);
        });
    }

    opts.from = opts.from || 'auto';
    opts.to = opts.to || 'en';

    opts.from = getCode(opts.from);
    opts.to = getCode(opts.to);

    return get(text).then(function (token) {
        var url = 'https://translate.google.com/translate_a/single';
        var data = {
            client: 't',
            sl: opts.from,
            tl: opts.to,
            hl: opts.to,
            dt: ['at', 'bd', 'ex', 'ld', 'md', 'qca', 'rw', 'rm', 'ss', 't'],
            ie: 'UTF-8',
            oe: 'UTF-8',
            otf: 1,
            ssel: 0,
            tsel: 0,
            kc: 7,
            q: text
        };
        data[token.name] = token.value;

        return url + '?' + querystring.stringify(data);
    }).then(function (url) {
        return got(url).then(function (res) {
            var result = {
                text: '',
                from: {
                    language: {
                        didYouMean: false,
                        iso: ''
                    },
                    text: {
                        autoCorrected: false,
                        value: '',
                        didYouMean: false
                    }
                },
                raw: ''
            };

            if (opts.raw) {
                result.raw = res.body;
            }

            var body = safeEval(res.body);
            body[0].forEach(function (obj) {
                if (obj[0]) {
                    result.text += obj[0];
                }
            });

            if (body[2] === body[8][0][0]) {
                result.from.language.iso = body[2];
            } else {
                result.from.language.didYouMean = true;
                result.from.language.iso = body[8][0][0];
            }

            if (body[7] && body[7][0]) {
                var str = body[7][0];

                str = str.replace(/<b><i>/g, '[');
                str = str.replace(/<\/i><\/b>/g, ']');

                result.from.text.value = str;

                if (body[7][5] === true) {
                    result.from.text.autoCorrected = true;
                } else {
                    result.from.text.didYouMean = true;
                }
            }

            return result;
        }).catch(function (err) {
            var e;
            e = new Error();
            if (err.statusCode !== undefined && err.statusCode !== 200) {
                e.code = 'BAD_REQUEST';
            } else {
                e.code = 'BAD_NETWORK';
            }
            throw e;
        });
    });
}

/**
 * Returns the ISO 639-1 code of the desiredLang – if it is supported by Google Translate
 * @param {string} desiredLang – the name or the code of the desired language
 * @returns {string|boolean} The ISO 639-1 code of the language or false if the language is not supported
 */
function getCode(desiredLang) {
    if (!desiredLang) {
        return false;
    }
    desiredLang = desiredLang.toLowerCase();

    if (langs[desiredLang]) {
        return desiredLang;
    }

    var keys = Object.keys(langs).filter(function (key) {
        if (typeof langs[key] !== 'string') {
            return false;
        }

        return langs[key].toLowerCase() === desiredLang;
    });

    return keys[0] || false;
}

/**
 * Returns true if the desiredLang is supported by Google Translate and false otherwise
 * @param desiredLang – the ISO 639-1 code or the name of the desired language
 * @returns {boolean}
 */
function isSupported(desiredLang) {
    return Boolean(getCode(desiredLang));
}

/**
* @param {array} tokens
* @param {string} from
* @param {string} to
* @param {object} map
* @returns {object} 
*/
module.exports = async (tokens, from, to, map) => {
  const allPromises = [];

  var fromLangIdx, toLangIdx;

  if (!map["languages"]) {
    map["languages"] = []
  }

  if (!map["tokens"]) {
    map["tokens"] = []
  }

  fromLangIdx = map["languages"].indexOf(from);
  toLangIdx = map["languages"].indexOf(to);
  if (fromLangIdx === -1) { // from language not found
    fromLangIdx = map["languages"].length;
    map["languages"].push(from);
    map["tokens"].forEach(row => {row.push(null)});
  }
  if (toLangIdx === -1) { // to language not found
    toLangIdx = map["languages"].length;
    map["languages"].push(to);
    map["tokens"].forEach(row => {row.push(null)});
  }

  for (let i = 0; i < tokens.length; i++) {
    let inDict = false;
    map["tokens"].forEach(row => {
      if (row[toLangIdx] && row[fromLangIdx] === tokens[i].value) {
        tokens[i].translated = row[toLangIdx];
        inDict = true;
      }
    });
    if (!inDict) {
      var text = tokens[i].value;
      if (!tokens[i]["isComment"]) {
        Case.lower(text);
      }
      allPromises.push(translateText(text, from, to));
    }
  }
  const results = await Promise.all(allPromises);
  results.forEach((item, i) => {
    origToken = tokens[i].value;
    
    var text = item;
    if (!tokens[i]["isComment"]) {
      Case.lower(text);
    }
    tokens[i].translated = Case[Case.of(origToken)](item.text).split(" ").join("_");
    var found = false;
    for (var i = 0; i < map["tokens"].length; i++) {
      if (map["tokens"][i][fromLangIdx] === origToken) {
        map["tokens"][i][toLangIdx] = tokens[i].translated;
        found = true;
        break;
      }
    }
    if (!found) {
      row = new Array(map["languages"].length).fill(null);
      row[fromLangIdx] = origToken;
      row[toLangIdx] = tokens[i].translated;
      map["tokens"].push(row);
    }
  });
  
  return {"tokens": tokens, "map": map};

  function translateText(text, fromLanguage, toLanguage) {
      return (translate(text, {from: fromLanguage, to: toLanguage}));
  }
};

'use babel';

import { CompositeDisposable } from 'atom'
const { execSync } = require('child_process');

export default {

  subscriptions: null,

  activate() {
    this.subscriptions = new CompositeDisposable()

    this.subscriptions.add(atom.commands.add('atom-workspace', {
      'polycode:translate': () => this.translate(),
      'polycode:untranslate': () => this.untranslate()
    }))
  },

  deactivate() {
    this.subscriptions.dispose()
  },

  translate() {
    console.log(`cd ${atom.project.rootDirectories[0].path}/ && python3 sample.py`)
    execSync(`cd ${atom.project.rootDirectories[0].path}/ && python3 temp.py`);
    atom.notifications.addSuccess('Translated your code!')
  },


  untranslate() {
    console.log("untranslating")
    atom.notifications.addSuccess('Returned files to the original language!')
  }
};

(function() {
  window.onload = function() {
    const sqlTextArea = document.getElementById('query');
    const mime = 'text/x-mariadb';
    CodeMirror.fromTextArea(sqlTextArea, {
      mode: mime,
      indentWithTabs: true,
      smartIndent: true,
      lineNumbers: true,
      matchBrackets : true,
      autofocus: true,
      extraKeys: {"Ctrl-Space": "autocomplete"},
      hintOptions: {}
    });
  };
})();

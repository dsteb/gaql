(function() {

  function initCodeMirror() {
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
  }

  function navigateToPage(page) {
    document.getElementById('page').value = page.toString();
    const form = document.getElementById('query-form');
    form.submit();
  }

  function initPagination() {
    const elements = document.querySelectorAll('.page-link');

    if (elements.length) {

      let active = -1;
      for (let i = 1; i < elements.length - 1; ++i) {
        const el = elements[i];

        if (!el.parentElement.className.includes('active')) {
          el.onclick = function() {
            const page = parseInt(this.innerText);
            navigateToPage(page);
          }
        } else {
          active = i;
        }
      }
      prev = elements[0];
      if (!prev.parentElement.className.includes('disabled')) {
        const prevPage = parseInt(elements[active - 1].innerText);
        prev.onclick = function() { navigateToPage(prevPage); };
      }
      next = elements[elements.length - 1];
      if (!next.parentElement.className.includes('disabled')) {
        const nextPage = parseInt(elements[active + 1].innerText);
        next.onclick = function() { navigateToPage(nextPage); };
      }
    }
  }

  window.onload = function() {
    initCodeMirror();
    initPagination();
  };
})();

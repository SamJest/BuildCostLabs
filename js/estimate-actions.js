(function () {
  function text(node) {
    return node ? node.textContent.trim() : "";
  }

  function byId(id) {
    return document.getElementById(id);
  }

  function activeButtonText(selector) {
    var active = document.querySelector(selector + '.is-active') || document.querySelector(selector + '[aria-selected="true"]');
    return text(active);
  }

  function sanitizeFilename(value) {
    return (value || 'quote-brief')
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '')
      .slice(0, 80) || 'quote-brief';
  }

  function pageLabel() {
    return text(document.querySelector('h1')) || document.title || 'Estimate';
  }

  function storageKey(suffix) {
    return 'buildcostlab:' + window.location.pathname + ':' + suffix;
  }

  function updateStatus(message) {
    var node = byId('estimate-action-status');
    if (node) node.textContent = message;
  }

  function track(action) {
    if (typeof window.gtag === 'function') {
      var pageTypeMeta = document.querySelector('meta[name="page-type"]');
      window.gtag('event', 'estimate_action_click', {
        action_name: action,
        page_type: pageTypeMeta ? pageTypeMeta.content : 'unknown'
      });
    }
  }

  function saveField(id, value) {
    try {
      window.localStorage.setItem(storageKey(id), value || '');
    } catch (error) {}
  }

  function restoreField(id) {
    try {
      return window.localStorage.getItem(storageKey(id)) || '';
    } catch (error) {
      return '';
    }
  }

  function initializeBriefFields() {
    ['quote-brief-title', 'quote-brief-notes'].forEach(function (id) {
      var field = byId(id);
      if (!field) return;
      var stored = restoreField(id);
      if (stored && !field.value) field.value = stored;
      field.addEventListener('input', function () {
        saveField(id, field.value);
      });
    });
  }

  function getFormValues() {
    var rows = [];
    document.querySelectorAll('.calculator-form label').forEach(function (label) {
      var titleNode = label.querySelector('span');
      var input = label.querySelector('input, select, textarea');
      if (!titleNode || !input) return;
      var value = '';
      if (input.tagName === 'SELECT') {
        value = input.options[input.selectedIndex] ? input.options[input.selectedIndex].text : input.value;
      } else if (input.type === 'checkbox') {
        value = input.checked ? 'Yes' : 'No';
      } else {
        value = input.value;
      }
      if (String(value).trim() !== '') {
        rows.push({ label: text(titleNode), value: String(value).trim() });
      }
    });
    var mode = activeButtonText('.mode-toggle');
    var unit = activeButtonText('.unit-toggle');
    var currency = activeButtonText('.currency-pill');
    if (mode) rows.push({ label: 'Mode', value: mode });
    if (unit) rows.push({ label: 'Units', value: unit });
    if (currency) rows.push({ label: 'Currency view', value: currency });
    return rows;
  }

  function getBreakdownRows(selector) {
    return Array.prototype.slice.call(document.querySelectorAll(selector)).map(function (row) {
      var cells = row.querySelectorAll('span, strong');
      if (cells.length < 2) return null;
      var left = text(cells[0]);
      var right = text(cells[cells.length - 1]);
      if (!left && !right) return null;
      return { label: left, value: right };
    }).filter(Boolean);
  }

  function getScenarioRows() {
    return Array.prototype.slice.call(document.querySelectorAll('#estimate-range .scenario-card')).map(function (card) {
      var heading = text(card.querySelector('strong'));
      var body = text(card.querySelector('span'));
      if (!heading && !body) return null;
      return { label: heading || 'Scenario', value: body };
    }).filter(Boolean);
  }

  function getCompareRows() {
    return Array.prototype.slice.call(document.querySelectorAll('#comparison-output .compare-card')).map(function (card) {
      var heading = text(card.querySelector('strong'));
      var body = text(card.querySelector('span'));
      if (!heading && !body) return null;
      return { label: heading || 'Option', value: body };
    }).filter(Boolean);
  }

  function getRealityItems() {
    return Array.prototype.slice.call(document.querySelectorAll('#reality-output li')).map(text).filter(Boolean);
  }

  function getChecklistItems() {
    return Array.prototype.slice.call(document.querySelectorAll('.quote-checklist .checklist li')).map(text).filter(Boolean);
  }

  function getQuoteBriefData() {
    var projectLabelField = byId('quote-brief-title');
    var notesField = byId('quote-brief-notes');
    return {
      pageTitle: pageLabel(),
      pageUrl: window.location.href,
      projectLabel: projectLabelField ? projectLabelField.value.trim() : '',
      notes: notesField ? notesField.value.trim() : '',
      main: text(document.querySelector('.result-main')) || 'Run the calculator to generate a live result.',
      sub: text(document.querySelector('.result-sub')),
      formValues: getFormValues(),
      breakdown: getBreakdownRows('.result-breakdown .break-row'),
      benchmark: getScenarioRows(),
      timeline: getBreakdownRows('#timeline-output .break-row'),
      compare: getCompareRows(),
      reality: getRealityItems(),
      checklist: getChecklistItems()
    };
  }

  function buildTextBrief(data) {
    var lines = [];
    lines.push(data.pageTitle);
    if (data.projectLabel) lines.push('Project label: ' + data.projectLabel);
    lines.push(data.pageUrl);
    lines.push('');
    lines.push('Main result: ' + data.main);
    if (data.sub) lines.push(data.sub);

    if (data.formValues.length) {
      lines.push('');
      lines.push('Inputs used:');
      data.formValues.forEach(function (row) {
        lines.push('- ' + row.label + ': ' + row.value);
      });
    }

    if (data.breakdown.length) {
      lines.push('');
      lines.push('Breakdown:');
      data.breakdown.forEach(function (row) {
        lines.push('- ' + row.label + ': ' + row.value);
      });
    }

    if (data.benchmark.length) {
      lines.push('');
      lines.push('Benchmark view:');
      data.benchmark.forEach(function (row) {
        lines.push('- ' + row.label + ': ' + row.value);
      });
    }

    if (data.timeline.length) {
      lines.push('');
      lines.push('Timeline notes:');
      data.timeline.forEach(function (row) {
        lines.push('- ' + row.label + ': ' + row.value);
      });
    }

    if (data.compare.length) {
      lines.push('');
      lines.push('Option comparison:');
      data.compare.forEach(function (row) {
        lines.push('- ' + row.label + ': ' + row.value);
      });
    }

    if (data.reality.length) {
      lines.push('');
      lines.push('Reality check items:');
      data.reality.forEach(function (item) {
        lines.push('- ' + item);
      });
    }

    if (data.checklist.length) {
      lines.push('');
      lines.push('Quote-ready checklist:');
      data.checklist.forEach(function (item) {
        lines.push('- ' + item);
      });
    }

    if (data.notes) {
      lines.push('');
      lines.push('Your notes:');
      lines.push(data.notes);
    }

    lines.push('');
    lines.push('Built with BuildCostLab. Treat this as a planning brief and compare it against live quotes, product sheets, and supplier terms before buying.');
    return lines.join('\n');
  }

  function csvEscape(value) {
    var stringValue = value == null ? '' : String(value);
    if (/[",\n]/.test(stringValue)) {
      return '"' + stringValue.replace(/"/g, '""') + '"';
    }
    return stringValue;
  }

  function buildWorksheetCsv(data) {
    var rows = [
      ['Section', 'Item', 'BuildCostLab value', 'Quote A', 'Quote B', 'Quote C', 'Notes']
    ];

    rows.push(['Overview', 'Page', data.pageTitle, '', '', '', '']);
    rows.push(['Overview', 'URL', data.pageUrl, '', '', '', '']);
    if (data.projectLabel) rows.push(['Overview', 'Project label', data.projectLabel, '', '', '', '']);
    if (data.notes) rows.push(['Overview', 'Your notes', data.notes, '', '', '', '']);

    data.formValues.forEach(function (row) {
      rows.push(['Input', row.label, row.value, '', '', '', '']);
    });
    data.breakdown.forEach(function (row) {
      rows.push(['Breakdown', row.label, row.value, '', '', '', '']);
    });
    data.benchmark.forEach(function (row) {
      rows.push(['Benchmark', row.label, row.value, '', '', '', '']);
    });
    data.timeline.forEach(function (row) {
      rows.push(['Timeline', row.label, row.value, '', '', '', '']);
    });
    data.compare.forEach(function (row) {
      rows.push(['Option', row.label, row.value, '', '', '', '']);
    });
    data.reality.forEach(function (item) {
      rows.push(['Reality check', item, '', '', '', '', '']);
    });
    data.checklist.forEach(function (item) {
      rows.push(['Checklist', item, '', '', '', '', '']);
    });

    rows.push(['Contractor questions', 'Lead time', '', '', '', '', '']);
    rows.push(['Contractor questions', 'What is excluded?', '', '', '', '', '']);
    rows.push(['Contractor questions', 'Waste and contingency included?', '', '', '', '', '']);
    rows.push(['Contractor questions', 'Delivery / access notes', '', '', '', '', '']);

    return rows.map(function (row) {
      return row.map(csvEscape).join(',');
    }).join('\n');
  }

  function copyText(summary) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(summary);
    }
    var area = document.createElement('textarea');
    area.value = summary;
    area.setAttribute('readonly', 'readonly');
    area.style.position = 'absolute';
    area.style.left = '-9999px';
    document.body.appendChild(area);
    area.select();
    try {
      document.execCommand('copy');
      document.body.removeChild(area);
      return Promise.resolve();
    } catch (error) {
      document.body.removeChild(area);
      return Promise.reject(error);
    }
  }

  function downloadFile(filename, content, mimeType) {
    var blob = new Blob([content], { type: mimeType });
    var url = window.URL.createObjectURL(blob);
    var link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.setTimeout(function () {
      window.URL.revokeObjectURL(url);
    }, 1000);
  }

  function handleAction(action) {
    var data = getQuoteBriefData();
    var textBrief = buildTextBrief(data);
    var baseName = sanitizeFilename(data.projectLabel || data.pageTitle);

    if (action === 'copy') {
      copyText(textBrief).then(function () {
        updateStatus('Quote brief copied. Paste it into email, notes, or a quote request.');
      }).catch(function () {
        updateStatus('Copy failed on this device. Download the brief or print the page instead.');
      });
      track('copy_quote_brief');
      return;
    }

    if (action === 'download-brief') {
      downloadFile(baseName + '-buildcostlab-brief.txt', textBrief, 'text/plain;charset=utf-8');
      updateStatus('Quote brief downloaded as a text file.');
      track('download_quote_brief');
      return;
    }

    if (action === 'download-worksheet') {
      downloadFile(baseName + '-quote-comparison.csv', buildWorksheetCsv(data), 'text/csv;charset=utf-8');
      updateStatus('Comparison worksheet downloaded as a CSV file.');
      track('download_quote_worksheet');
      return;
    }

    if (action === 'print') {
      window.print();
      updateStatus('Print dialog opened. Save as PDF if you want a shareable version of the brief.');
      track('print_quote_brief');
    }
  }

  initializeBriefFields();

  document.querySelectorAll('[data-estimate-action]').forEach(function (button) {
    button.addEventListener('click', function () {
      handleAction(button.getAttribute('data-estimate-action'));
    });
  });
})();

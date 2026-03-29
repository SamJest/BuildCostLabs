(function () {
  function byId(id) {
    return document.getElementById(id);
  }

  const actions = Array.from(document.querySelectorAll('[data-estimate-action]'));
  if (!actions.length) return;

  const pageKey = 'bcl_quote_brief_' + (window.location.pathname || '/');
  const status = byId('quote-status');
  const projectField = byId('quote-project-label');
  const locationField = byId('quote-location');
  const timingField = byId('quote-timing');
  const emailField = byId('quote-email');
  const notesField = byId('quote-notes');

  function setStatus(message) {
    if (status) status.textContent = message;
  }

  function getText(selector) {
    const el = document.querySelector(selector);
    return el ? el.textContent.trim() : '';
  }

  function getBreakdownLines() {
    return Array.from(document.querySelectorAll('#result-breakdown .break-row')).map(function (row) {
      const bits = Array.from(row.children).map(function (node) { return node.textContent.trim(); }).filter(Boolean);
      return bits.join(': ');
    }).filter(Boolean);
  }

  function getEstimateRangeLines() {
    return Array.from(document.querySelectorAll('#estimate-range .scenario-card')).map(function (card) {
      const parts = Array.from(card.querySelectorAll('strong, span')).map(function (node) { return node.textContent.trim(); }).filter(Boolean);
      return parts.join(' — ');
    }).filter(Boolean);
  }

  function buildBrief() {
    const title = getText('h1') || 'BuildCostLab estimate';
    const projectLabel = projectField && projectField.value.trim() ? projectField.value.trim() : 'Not provided';
    const location = locationField && locationField.value.trim() ? locationField.value.trim() : 'Not provided';
    const timing = timingField && timingField.value.trim() ? timingField.value.trim() : 'Not provided';
    const email = emailField && emailField.value.trim() ? emailField.value.trim() : '';
    const notes = notesField && notesField.value.trim() ? notesField.value.trim() : 'None added';
    const resultMain = getText('.result-main');
    const resultSub = getText('.result-sub');
    const drivers = getText('#estimate-drivers');
    const confidence = getText('#confidence-note');
    const breakdown = getBreakdownLines();
    const ranges = getEstimateRangeLines();

    const lines = [
      title,
      '',
      'Project label: ' + projectLabel,
      'Location / postcode area: ' + location,
      'Target timing: ' + timing,
      'Page URL: ' + window.location.href,
      '',
      'Main estimate:',
      resultMain || 'No live estimate yet',
      resultSub || 'Run the calculator to generate the estimate.',
      ''
    ];

    if (breakdown.length) {
      lines.push('Breakdown:');
      breakdown.forEach(function (line) { lines.push('- ' + line); });
      lines.push('');
    }

    if (ranges.length) {
      lines.push('Planning range:');
      ranges.forEach(function (line) { lines.push('- ' + line); });
      lines.push('');
    }

    if (drivers) {
      lines.push('Main cost drivers:');
      lines.push(drivers);
      lines.push('');
    }

    if (confidence) {
      lines.push('Confidence note:');
      lines.push(confidence);
      lines.push('');
    }

    lines.push('Notes / exclusions:');
    lines.push(notes);
    lines.push('');
    lines.push('Quote request checklist:');
    lines.push('- Confirm whether the price includes materials, labour, delivery, waste removal, and finish items.');
    lines.push('- Ask for exclusions, lead time, payment terms, and any assumptions based on access or condition.');
    lines.push('- Price the same scope with each supplier or installer so the quotes are comparable.');

    return {
      title: title,
      email: email,
      text: lines.join('\n')
    };
  }

  function saveFields() {
    const payload = {
      project: projectField ? projectField.value : '',
      location: locationField ? locationField.value : '',
      timing: timingField ? timingField.value : '',
      email: emailField ? emailField.value : '',
      notes: notesField ? notesField.value : ''
    };
    window.localStorage.setItem(pageKey, JSON.stringify(payload));
  }

  function restoreFields() {
    try {
      const raw = window.localStorage.getItem(pageKey);
      if (!raw) return;
      const payload = JSON.parse(raw);
      if (projectField && payload.project) projectField.value = payload.project;
      if (locationField && payload.location) locationField.value = payload.location;
      if (timingField && payload.timing) timingField.value = payload.timing;
      if (emailField && payload.email) emailField.value = payload.email;
      if (notesField && payload.notes) notesField.value = payload.notes;
    } catch (error) {
      // ignore storage parse issues
    }
  }

  function download(filename, content, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 500);
  }

  function makeSafeFilename(value, fallback, ext) {
    const base = (value || fallback || 'buildcostlab-quote-brief').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
    return (base || fallback || 'buildcostlab-quote-brief') + ext;
  }

  function csvContent(brief) {
    const rows = [
      ['Supplier', 'Contact', 'Materials quote', 'Labour quote', 'Extras', 'Total quote', 'Lead time', 'Notes'],
      ['', '', '', '', '', '', '', 'Based on: ' + brief.title]
    ];
    return rows.map(function (row) {
      return row.map(function (cell) {
        const value = String(cell || '');
        return '"' + value.replace(/"/g, '""') + '"';
      }).join(',');
    }).join('\n');
  }

  restoreFields();
  [projectField, locationField, timingField, emailField, notesField].forEach(function (field) {
    if (!field) return;
    field.addEventListener('input', saveFields);
  });

  actions.forEach(function (button) {
    button.addEventListener('click', function () {
      saveFields();
      const brief = buildBrief();
      const action = button.getAttribute('data-estimate-action');
      if (action === 'copy') {
        navigator.clipboard.writeText(brief.text).then(function () {
          setStatus('Quote brief copied. Paste it into your email or message to a builder or supplier.');
        }).catch(function () {
          setStatus('Copy failed in this browser. Use the download action instead.');
        });
        return;
      }
      if (action === 'email') {
        const recipient = brief.email || '';
        const subject = encodeURIComponent(brief.title + ' quote brief');
        const body = encodeURIComponent(brief.text);
        window.location.href = 'mailto:' + recipient + '?subject=' + subject + '&body=' + body;
        setStatus('Your email app should open with the quote brief ready to send.');
        return;
      }
      if (action === 'txt') {
        download(makeSafeFilename(brief.title, 'buildcostlab-quote-brief', '.txt'), brief.text, 'text/plain;charset=utf-8');
        setStatus('Quote brief downloaded as a text file.');
        return;
      }
      if (action === 'csv') {
        download(makeSafeFilename(brief.title, 'buildcostlab-quote-comparison', '.csv'), csvContent(brief), 'text/csv;charset=utf-8');
        setStatus('Comparison sheet downloaded as CSV.');
        return;
      }
      if (action === 'print') {
        window.print();
        setStatus('Use your browser print dialog to save the brief as PDF if needed.');
      }
    });
  });
})();

fetch('data.json').then(r => r.json()).then(data => {
  const occs = data.occupations;
  const stateAvgs = data.state_averages;

  // Treemap
  Plotly.newPlot('treemap', [{
    type: 'treemap',
    labels: occs.map(o => o.Occupation),
    parents: occs.map(() => 'All Occupations'),
    values: occs.map(o => o.Employed || 1000),
    marker: { colors: occs.map(o => o.ai_score) }
  }], {title: 'AI Exposure Treemap (size = jobs • colour = risk 0-10)'});

  // Full colour choropleth + Sydney default
  const map = L.map('map').setView([-33.8688, 151.2093], 6);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

  fetch('https://raw.githubusercontent.com/rowanhogan/australian-states/master/states.geojson')
    .then(r => r.json()).then(geo => {
      L.geoJSON(geo, {
        style: feature => {
          const name = feature.properties.STATE_NAME;
          const score = stateAvgs[name] || 5;
          const color = score < 4 ? '#10b981' : score < 6 ? '#f59e0b' : '#ef4444';
          return { fillColor: color, weight: 2, opacity: 1, color: '#fff', fillOpacity: 0.75 };
        },
        onEachFeature: (feature, layer) => {
          const name = feature.properties.STATE_NAME;
          const score = stateAvgs[name] || 5;
          layer.bindPopup(`<b>${name}</b><br>Weighted AI Exposure: <strong>${score}/10</strong>`);
          if (name === "New South Wales") layer.setStyle({weight: 5, color: '#22c55e'});
        }
      }).addTo(map);
    });

  // Legend
  const legend = L.control({position: 'bottomright'});
  legend.onAdd = () => {
    const div = L.DomUtil.create('div', 'info legend');
    div.innerHTML = `<strong>AI Risk</strong><br>
      <span style="color:#10b981">● Low (0-4)</span><br>
      <span style="color:#f59e0b">● Medium (4-6)</span><br>
      <span style="color:#ef4444">● High (6-10)</span>`;
    return div;
  };
  legend.addTo(map);

  // Career Matcher with NSW priority
  window.matchCareers = function() {
    let term = (document.getElementById('skills').value || "").toLowerCase();
    let results = occs.filter(o => 
      (o.Occupation + (o.Task || "")).toLowerCase().includes(term)
    ).sort((a,b) => (b.ai_score - a.ai_score) + ((a["New South Wales"] || 0) > 0 ? 100 : 0)).slice(0,12);

    let html = '<h3 class="text-2xl mb-4">Your NSW-focused resilient matches:</h3><ul class="space-y-4">';
    results.forEach(r => {
      html += `<li onclick="generatePDF('${r.Occupation}')" class="cursor-pointer bg-zinc-900 p-4 rounded-2xl hover:bg-emerald-900">
        <strong>${r.Occupation}</strong> – AI risk ${r.ai_score}/10 – $${Math.round(r['Median weekly earnings ($)'] || 0)} AUD
      </li>`;
    });
    html += '</ul>';
    document.getElementById('results').innerHTML = html;
  };

  // PDF Report
  window.generatePDF = function(title) {
    const occ = occs.find(o => o.Occupation === title);
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    doc.text(`AI Resilience Report – ${title}`, 20, 20);
    doc.text(`AI Exposure: ${occ.ai_score}/10`, 20, 40);
    doc.text(`Median pay: $${Math.round(occ['Median weekly earnings ($)'] || 0)} AUD`, 20, 50);
    doc.text(`Rationale: ${occ.rationale.substring(0,300)}...`, 20, 65);
    doc.text('Next step: TAFE NSW or your local Jobs and Skills Centre', 20, 90);
    doc.save(`${title.replace(/ /g,'_')}_AI_Report.pdf`);
    alert('✅ PDF downloaded!');
  };

  // Auto-run NSW matcher
  setTimeout(() => { document.getElementById('skills').placeholder = "e.g. electrician or aged care (NSW focus)"; }, 500);
});

function showTab(n) {
  document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
  document.getElementById('tab'+n).classList.remove('hidden');
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-btn')[n].classList.add('active');
}

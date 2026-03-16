fetch('data.json').then(r => r.json()).then(data => {
  let occs = data.occupations;

  function render(filtered) {
    Plotly.newPlot('treemap', [{
      type: 'treemap',
      labels: filtered.map(o => o.Occupation),
      parents: filtered.map(o => o["Major Group"] || ''),
      values: filtered.map(o => Math.max(o.Employed || 1000, 5000)), // min size for visibility
      marker: { 
        colors: filtered.map(o => o.ai_score),
        colorscale: [[0,'#10b981'],[0.4,'#10b981'],[0.4,'#f59e0b'],[0.6,'#f59e0b'],[0.6,'#ef4444'],[1,'#ef4444']]
      },
      textinfo: "label+value",
      hovertemplate: "<b>%{label}</b><br>AI Risk: %{customdata.score}/10 (%{customdata.outlook}%)<br>Jobs: %{value}<br>Pay: $%{customdata.pay} AUD<br>Tasks: %{customdata.task}<extra></extra>",
      customdata: filtered.map(o => ({
        score: o.ai_score,
        outlook: Math.round(o.ai_score * 10),
        pay: Math.round(o["Median weekly earnings ($)"] || 0),
        task: (o.Task || "").substring(0,150) + "..."
      }))
    }], {
      margin: {t:0, l:0, r:0, b:0},
      paper_bgcolor: "#111",
      plot_bgcolor: "#111"
    });
  }

  render(occs);

  // Update sidebar
  document.getElementById('total-jobs').textContent = `Total Jobs: ${occs.reduce((a,o) => a + (o.Employed||0), 0).toLocaleString()}`;
  document.getElementById('avg-risk').textContent = `Average AI Risk: ${(occs.reduce((a,o) => a + o.ai_score, 0)/occs.length).toFixed(1)}/10`;
  document.getElementById('green-jobs').textContent = `Safe Koala Jobs: ${occs.filter(o => o.ai_score <= 3.5).length}`;
  document.getElementById('red-jobs').textContent = `Shark-Bait Jobs: ${occs.filter(o => o.ai_score >= 6).length}`;

  // Filters
  document.getElementById('stateFilter').onchange = e => {
    const val = e.target.value;
    const f = val === "All" ? occs : occs.filter(o => (o[val] || 0) > 0);
    render(f);
  };

  document.getElementById('searchBox').oninput = e => {
    const term = e.target.value.toLowerCase();
    const f = occs.filter(o => o.Occupation.toLowerCase().includes(term));
    render(f);
  };
});
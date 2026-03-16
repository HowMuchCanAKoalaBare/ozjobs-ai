fetch('data.json').then(r => r.json()).then(data => {
  let occs = data.occupations;

  function render(filtered) {
    Plotly.newPlot('treemap', [{
      type: 'treemap',
      labels: filtered.map(o => o.Occupation),
      parents: filtered.map(() => ''),
      values: filtered.map(o => o.Employed || 1000),
      marker: { 
        colors: filtered.map(o => o.ai_score),
        colorscale: [
          [0, '#10b981'], [0.4, '#10b981'],   // lush green koala
          [0.4, '#f59e0b'], [0.6, '#f59e0b'], // she'll be right orange
          [0.6, '#ef4444'], [1, '#ef4444']    // shark-bait red
        ]
      },
      textinfo: "label+value",
      hovertemplate: "<b>%{label}</b><br>AI Risk: %{customdata.score}/10<br>Jobs: %{value}<br>Pay: $%{customdata.pay} AUD/week<br>Tasks: %{customdata.task}<extra></extra>",
      customdata: filtered.map(o => ({
        score: o.ai_score,
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

  // Live filters (exact JoshKale behaviour)
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
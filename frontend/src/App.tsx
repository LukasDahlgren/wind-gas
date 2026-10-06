function App() {
  return (
    <main className="terminal" id="overview">
      <header className="terminal-bar">
        <a className="wordmark" href="#overview">WINDGAS</a>
        <nav aria-label="Main navigation"><a className="selected" href="#overview">Monitor</a><a href="#history">History</a><a href="#method">Method</a></nav>
        <div className="connection"><span /> Unavailable</div>
      </header>

      <div className="terminal-content">
        <div className="market-line"><span>SWEDEN · SE3 · DAY-AHEAD</span><span>AREA · STOCKHOLM / CENTRAL SWEDEN</span><span className="preview">PROTOTYPE · NO LIVE DATA</span></div>

        <div className="dashboard-columns">
          <div className="monitor-panel">

        <section className="metrics" aria-label="Price outlook inputs">
          <div className="metric-row"><span className="metric-name">Day-ahead price</span><strong>— <small>SEK/MWh</small></strong><span className="metric-state">Awaiting data</span></div>
          <div className="metric-row"><span className="metric-name">Wind generation forecast</span><strong>— <small>MW</small></strong><span className="metric-state">Awaiting data</span></div>
          <div className="metric-row"><span className="metric-name">Electricity load forecast</span><strong>— <small>MW</small></strong><span className="metric-state">Awaiting data</span></div>
        </section>

        <section className="signal-block" aria-labelledby="signal-title">
          <div className="signal-label">PRICE OUTLOOK · SE3</div>
          <div className="signal-summary"><h2 id="signal-title">Not assessed</h2><p>Price forecast needs historical and forecast data</p></div>
        </section>

        <section className="history" id="history">
          <div className="section-head"><h2>Recent day-ahead prices</h2><span>SEK/MWh · NO SERIES LOADED</span></div>
          <div className="history-table" role="table" aria-label="Day-ahead price history">
            <div className="history-row history-header" role="row"><span>Delivery</span><span>Price</span><span>Outlook</span></div>
            <div className="history-empty">Price history will appear here when ENTSO-E data access is configured.</div>
          </div>
        </section>
          </div>

          <aside className="recommendation-panel">
        <section className="recommendation" aria-labelledby="recommendation-title">
          <div className="section-head recommendation-head">
            <h2 id="recommendation-title">Buy recommendations</h2>
          </div>
          <div className="recommendation-card">
            <div className="recommendation-main">
              <div className="recommendation-eyebrow">SE3 DAY-AHEAD ELECTRICITY</div>
              <div className="recommendation-call">No signal</div>
              <p>No buy or sell recommendation until price and forecast data are connected and evaluated.</p>
            </div>
            <div className="recommendation-details">
              <div><span>Price target</span><strong>SE3 day-ahead</strong></div>
              <div><span>Confidence</span><strong>Not assessed</strong></div>
              <div><span>Next step</span><strong>Connect ENTSO-E data</strong></div>
            </div>
          </div>
          <p className="recommendation-note">This is a research prototype, not a validated price forecast or trading strategy. Weather is only one driver; demand, hydro conditions, outages, imports, and market prices also matter.</p>
        </section>
          </aside>
        </div>

      </div>
    </main>
  );
}

export default App;

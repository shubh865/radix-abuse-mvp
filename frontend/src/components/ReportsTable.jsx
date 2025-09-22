import { useEffect, useMemo, useState } from "react";
import api from "../api";

const riskOptions = ["ALL", "HIGH", "MEDIUM", "LOW"];

export default function ReportsTable() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState("");

  const [domainFilter, setDomainFilter] = useState("");
  const [riskFilter, setRiskFilter] = useState("ALL");
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");

  const [sortKey, setSortKey] = useState("reported_timestamp");
  const [sortDir, setSortDir] = useState("desc");

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        const { data } = await api.get("/reports");
        setRows(data || []);
      } catch (e) {
        console.error(e);
        setErr("Failed to load reports");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const view = useMemo(() => {
    let out = [...rows];
    if (domainFilter.trim()) {
      const needle = domainFilter.trim().toLowerCase();
      out = out.filter((r) => r.domain_name.toLowerCase().includes(needle));
    }
    if (riskFilter !== "ALL") out = out.filter((r) => r.risk_level === riskFilter);
    if (dateFrom) out = out.filter((r) => Date.parse(r.reported_timestamp) >= Date.parse(dateFrom + "T00:00:00Z"));
    if (dateTo) out = out.filter((r) => Date.parse(r.reported_timestamp) <= Date.parse(dateTo + "T23:59:59Z"));

    out.sort((a, b) => {
      const dir = sortDir === "asc" ? 1 : -1;
      const val = (x) =>
        sortKey === "reported_timestamp"
          ? Date.parse(x.reported_timestamp)
          : sortKey === "domain_name"
          ? x.domain_name.toLowerCase()
          : String(x[sortKey]);
      const va = val(a), vb = val(b);
      return (va < vb ? -1 : va > vb ? 1 : 0) * dir;
    });
    return out;
  }, [rows, domainFilter, riskFilter, dateFrom, dateTo, sortKey, sortDir]);

  function toggleSort(key) {
    if (sortKey === key) setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    else { setSortKey(key); setSortDir("asc"); }
  }

  if (loading) return <p className="muted">Loading reports…</p>;
  if (err) return <p style={{ color: "tomato" }}>{err}</p>;

  return (
    <>
      {/* Filters */}
      <div className="row" style={{ marginBottom: 10 }}>
        <div className="col">
          <input className="input" placeholder="Domain filter (e.g., paypal)" value={domainFilter}
                 onChange={(e) => setDomainFilter(e.target.value)} />
        </div>
        <div className="col">
          <select className="select" value={riskFilter} onChange={(e) => setRiskFilter(e.target.value)}>
            {riskOptions.map((o) => <option key={o} value={o}>{o}</option>)}
          </select>
        </div>
        <div className="col">
          <input type="date" className="date" value={dateFrom} onChange={(e) => setDateFrom(e.target.value)} />
        </div>
        <div className="col">
          <input type="date" className="date" value={dateTo} onChange={(e) => setDateTo(e.target.value)} />
        </div>
        <div style={{ display:"flex", alignItems:"stretch" }}>
          <button className="btn small secondary" onClick={()=>{
            setDomainFilter(""); setRiskFilter("ALL"); setDateFrom(""); setDateTo("");
          }}>Clear filters</button>
        </div>
      </div>

      {/* Table */}
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <Th label="Report ID" />
              <SortTh label="Domain" k="domain_name" on={toggleSort} activeKey={sortKey} dir={sortDir} />
              <SortTh label="Abuse" k="abuse_type" on={toggleSort} activeKey={sortKey} dir={sortDir} />
              <SortTh label="Risk" k="risk_level" on={toggleSort} activeKey={sortKey} dir={sortDir} />
              <SortTh label="Reported At (UTC)" k="reported_timestamp" on={toggleSort} activeKey={sortKey} dir={sortDir} />
            </tr>
          </thead>
          <tbody>
            {view.length === 0 ? (
              <tr><td colSpan="5" className="muted">No reports match your filters.</td></tr>
            ) : view.map((r) => (
              <tr key={r.report_id}>
                <td>{r.report_id}</td>
                <td style={{ fontWeight:700 }}>{r.domain_name}</td>
                <td>{r.abuse_type}</td>
                <td>
                  <span className={`badge ${r.risk_level === "HIGH" ? "high" : r.risk_level === "MEDIUM" ? "med" : "low"}`}>
                    {r.risk_level}
                  </span>
                </td>
                <td>{new Date(r.reported_timestamp).toISOString().replace("T"," ").replace("Z","")}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}

function Th({ label }) { return <th>{label}</th>; }

function SortTh({ label, k, on, activeKey, dir }) {
  const active = activeKey === k;
  return (
    <th>
      <button className="btn small secondary"
        style={{ borderColor: active ? "#3f50ff" : "var(--border)" }}
        onClick={() => on(k)}>
        {label} {active ? (dir === "asc" ? "↑" : "↓") : ""}
      </button>
    </th>
  );
}

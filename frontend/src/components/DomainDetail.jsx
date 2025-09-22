import { useState } from "react";
import api from "../api";

export default function DomainDetail(){
  const [query, setQuery] = useState("");
  const [detail, setDetail] = useState(null);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");

  async function fetchDetail(e){
    e?.preventDefault();
    const dn = query.trim().toLowerCase();
    if(!dn || !dn.includes(".")) return setMsg("Enter a valid domain.");
    try{
      setMsg(""); setLoading(true);
      const { data } = await api.get(`/report/${dn}`);
      setDetail(data);
    }catch(err){
      console.error(err);
      setMsg("Domain not found or error fetching details.");
      setDetail(null);
    }finally{ setLoading(false); }
  }

  return (
    <>
      <form onSubmit={fetchDetail} className="row" style={{ marginBottom: 12 }}>
        <div className="col">
          <input className="input" placeholder="e.g., verify-paypal-online.online"
                 value={query} onChange={(e)=>setQuery(e.target.value)} />
        </div>
        <div style={{ display:"flex", alignItems:"stretch" }}>
          <button className="btn small">Lookup</button>
        </div>
      </form>
      {msg && <p style={{ color:"tomato" }}>{msg}</p>}
      {loading && <p className="muted">Loading…</p>}

      {detail && (
        <div className="detail-grid">
          <div className="card">
            <h3 style={{ marginTop:0 }}>{detail.domain.domain_name}</h3>
            <p className="muted" style={{ marginTop:4 }}>
              Status: <b>{detail.domain.current_status}</b>
            </p>

            <h4>Reports</h4>
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Report ID</th>
                    <th>Abuse</th>
                    <th>Risk</th>
                    <th>Reported At</th>
                  </tr>
                </thead>
                <tbody>
                  {detail.reports.length === 0 ? (
                    <tr><td colSpan="4" className="muted">No reports yet.</td></tr>
                  ) : detail.reports.map(r => (
                    <tr key={r.report_id}>
                      <td>{r.report_id}</td>
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

            <h4 style={{ marginTop:16 }}>Status History</h4>
            {detail.status_history.length === 0 ? (
              <p className="muted">No status updates yet.</p>
            ) : (
              <ul>
                {detail.status_history.map(s => (
                  <li key={s.status_id}>
                    <b>{s.new_status}</b> by {s.reviewer_initials}
                    {s.notes ? ` — ${s.notes}` : ""} on{" "}
                    {new Date(s.created_at).toISOString().replace("T"," ").replace("Z","")}
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div className="card">
            <StatusUpdate domainName={detail.domain.domain_name} onUpdated={fetchDetail} />
          </div>
        </div>
      )}
    </>
  );
}

function StatusUpdate({ domainName, onUpdated }){
  const [newStatus, setNewStatus] = useState("REVIEWED");
  const [initials, setInitials] = useState("SD");
  const [notes, setNotes] = useState("");
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");

  async function submit(e){
    e.preventDefault();
    if(!initials.trim()) return setMsg("Reviewer initials required.");
    try{
      setMsg(""); setLoading(true);
      await api.post(`/domains/${domainName}/status`, {
        new_status: newStatus, reviewer_initials: initials.trim(), notes: notes.trim() || null
      });
      setMsg("Status updated ✅"); onUpdated();
    }catch(err){
      console.error(err); setMsg("Failed to update status.");
    }finally{ setLoading(false); }
  }

  return (
    <form onSubmit={submit}>
      <h3 style={{ marginTop:0 }}>Update Status</h3>
      <p className="muted" style={{ marginTop:0 }}>Domain: <b>{domainName}</b></p>

      <label className="muted">New Status</label>
      <select className="select" value={newStatus} onChange={(e)=>setNewStatus(e.target.value)}>
        <option value="REVIEWED">REVIEWED</option>
        <option value="ESCALATED">ESCALATED</option>
        <option value="SUSPENDED">SUSPENDED</option>
      </select>

      <div className="row" style={{ marginTop:10 }}>
        <div className="col">
          <label className="muted">Reviewer Initials</label>
          <input className="input" value={initials} onChange={(e)=>setInitials(e.target.value)} />
        </div>
      </div>

      <label className="muted" style={{ marginTop:10, display:"block" }}>Notes (optional)</label>
      <input className="input" value={notes} onChange={(e)=>setNotes(e.target.value)} />

      <div style={{ marginTop:12 }}>
        <button className="btn" disabled={loading}>{loading ? "Saving…" : "Save Status"}</button>
      </div>
      {msg && <p style={{ marginTop:8 }}>{msg}</p>}
    </form>
  );
}

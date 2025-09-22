import { useState } from "react";
import api from "../api";

const abuseTypes = ["PHISHING","MALWARE","BOTNET_C2","CSAM","SPAM","OTHER"];

export default function NewReportForm() {
  const [domain, setDomain] = useState("");
  const [source, setSource] = useState("");
  const [abuseType, setAbuseType] = useState("PHISHING");
  const [confidence, setConfidence] = useState(80);
  const [ts, setTs] = useState(new Date().toISOString().slice(0,19));
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");

  const validDomain = (d) => /\./.test(d) && !/\s/.test(d);

  async function onSubmit(e){
    e.preventDefault();
    setMsg("");
    const dn = domain.trim().toLowerCase();
    if(!validDomain(dn)) return setMsg("Enter a valid domain.");
    if(!source.trim()) return setMsg("Reporter source is required.");
    if(confidence<0 || confidence>100) return setMsg("Confidence must be 0–100.");

    try{
      setLoading(true);
      await api.post("/report", {
        domain_name: dn,
        reporter_source: source.trim(),
        abuse_type: abuseType,
        timestamp: ts.endsWith("Z") ? ts : ts + "Z",
        confidence_score: Number(confidence)
      });
      setMsg("Report created ✅");
      setTimeout(()=>window.location.reload(), 500);
    }catch(err){
      console.error(err);
      setMsg("Failed to create report.");
    }finally{ setLoading(false); }
  }

  return (
    <form onSubmit={onSubmit}>
      <div className="row">
        <div className="col">
          <label className="muted">Domain</label>
          <input className="input" placeholder="e.g., verify-paypal-online.online"
                 value={domain} onChange={(e)=>setDomain(e.target.value)} />
        </div>
        <div className="col">
          <label className="muted">Reporter Source</label>
          <input className="input" placeholder="e.g., Netcraft"
                 value={source} onChange={(e)=>setSource(e.target.value)} />
        </div>
      </div>

      <div className="row" style={{ marginTop:10 }}>
        <div className="col">
          <label className="muted">Abuse Type</label>
          <select className="select" value={abuseType} onChange={(e)=>setAbuseType(e.target.value)}>
            {abuseTypes.map(t => <option key={t} value={t}>{t}</option>)}
          </select>
        </div>
        <div className="col">
          <label className="muted">Confidence (0–100)</label>
          <input className="input" type="number" min={0} max={100}
                 value={confidence} onChange={(e)=>setConfidence(e.target.value)} />
        </div>
      </div>

      <div className="row" style={{ marginTop:10 }}>
        <div className="col">
          <label className="muted">Reported Timestamp (UTC)</label>
          <input className="date" type="datetime-local" value={ts} onChange={(e)=>setTs(e.target.value)} />
          <div className="muted" style={{ marginTop:6 }}>Sent as ISO 8601 with <span className="kbd">Z</span>.</div>
        </div>
      </div>

      <div style={{ marginTop:14 }}>
        <button className="btn" disabled={loading}>{loading ? "Submitting…" : "Create Report"}</button>
      </div>

      {msg && <p style={{ marginTop:10 }}>{msg}</p>}
    </form>
  );
}

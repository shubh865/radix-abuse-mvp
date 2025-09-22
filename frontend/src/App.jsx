import ReportsTable from "./components/ReportsTable";
import NewReportForm from "./components/NewReportForm";
import DomainDetail from "./components/DomainDetail";

export default function App() {
  return (
    <div className="app-wrap">
      <div className="header">
        <h1 className="h1">Radix Abuse Dashboard (MVP)</h1>
        <span className="api-chip">API: {import.meta.env.VITE_API_BASE_URL}</span>
      </div>

      <div className="card" style={{ marginBottom: 16 }}>
        <h2 className="section-title">Abuse Reports</h2>
        <ReportsTable />
      </div>

      <div className="card" style={{ marginBottom: 16 }}>
        <h2 className="section-title">Add New Report</h2>
        <NewReportForm />
      </div>

      <div className="card">
        <h2 className="section-title">Domain Detail</h2>
        <DomainDetail />
      </div>
    </div>
  );
}

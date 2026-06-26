import { useEffect, useMemo, useState } from 'react';
import { analyzeIncident, getHealth, getMetrics, getObservability } from './api';
import AgentChat from './components/AgentChat';
import AgentTraceTimeline from './components/AgentTraceTimeline';
import AgentWorkflow from './components/AgentWorkflow';
import IncidentForm from './components/IncidentForm';
import LangSmithPanel from './components/LangSmithPanel';
import MetricsPanel from './components/MetricsPanel';
import MonitoringPanel from './components/MonitoringPanel';
import ObservabilityPanel from './components/ObservabilityPanel';
import ResultDashboard from './components/ResultDashboard';

const getServiceStatus = (health) => health?.status || health?.service_status || 'unknown';
const getEnvironment = (health, observability) => (
  observability?.environment || health?.environment || 'local'
);
const getVersion = (health, observability) => (
  observability?.version || health?.version || 'N/A'
);
const isLangSmithEnabled = (observability, result) => Boolean(
  result?.monitoring?.langsmith?.enabled ??
  observability?.langsmith_enabled ??
  observability?.enabled
);

function App() {
  const [health, setHealth] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [observability, setObservability] = useState(null);
  const [bootstrapLoading, setBootstrapLoading] = useState(true);
  const [bootstrapError, setBootstrapError] = useState(null);
  const [incident, setIncident] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [analysisError, setAnalysisError] = useState(null);

  const workflowStatus = useMemo(() => {
    if (analysisError) return 'error';
    if (analysisLoading) return 'running';
    if (analysisResult) return 'completed';
    return 'pending';
  }, [analysisError, analysisLoading, analysisResult]);

  const refreshMetrics = async () => {
    try {
      const data = await getMetrics();
      setMetrics(data);
    } catch {
      setBootstrapError((current) => current || 'Metrics are unavailable.');
    }
  };

  useEffect(() => {
    let mounted = true;

    const loadBootstrap = async () => {
      setBootstrapLoading(true);
      const [healthResult, metricsResult, observabilityResult] = await Promise.allSettled([
        getHealth(),
        getMetrics(),
        getObservability(),
      ]);

      if (!mounted) return;

      if (healthResult.status === 'fulfilled') setHealth(healthResult.value);
      if (metricsResult.status === 'fulfilled') setMetrics(metricsResult.value);
      if (observabilityResult.status === 'fulfilled') setObservability(observabilityResult.value);

      const failed = [healthResult, metricsResult].some((result) => result.status === 'rejected');
      setBootstrapError(failed ? 'Some backend status data is unavailable.' : null);
      setBootstrapLoading(false);
    };

    loadBootstrap();
    const interval = window.setInterval(refreshMetrics, 10000);

    return () => {
      mounted = false;
      window.clearInterval(interval);
    };
  }, []);

  const handleAnalyze = async (payload) => {
    setIncident(payload);
    setAnalysisResult(null);
    setAnalysisError(null);
    setAnalysisLoading(true);

    try {
      const data = await analyzeIncident(payload);
      setAnalysisResult(data);
      refreshMetrics();
    } catch (err) {
      setAnalysisError(err.message || 'An unexpected error occurred during analysis.');
    } finally {
      setAnalysisLoading(false);
    }
  };

  const hasAnalysisContext = analysisLoading || analysisResult || analysisError;
  const langSmithEnabled = isLangSmithEnabled(observability, analysisResult);

  return (
    <div className="app-shell">
      <header className="app-header">
        <div>
          <span className="eyebrow">AI Agents Control Center</span>
          <h1>Finance Incident Observability</h1>
        </div>
        <div className="status-strip">
          <span className={`status-pill ${getServiceStatus(health) === 'ok' ? 'status-ok' : ''}`}>
            Service: {getServiceStatus(health)}
          </span>
          <span className={`status-pill ${langSmithEnabled ? 'status-ok' : 'status-muted'}`}>
            LangSmith: {langSmithEnabled ? 'enabled' : 'disabled'}
          </span>
          <span className="status-pill">Env: {getEnvironment(health, observability)}</span>
          <span className="status-pill">Version: {getVersion(health, observability)}</span>
        </div>
      </header>

      {bootstrapError && <div className="notice notice-warning">{bootstrapError}</div>}

      <main className="dashboard-layout">
        <div className="main-column">
          <IncidentForm onSubmit={handleAnalyze} isLoading={analysisLoading} />
          {analysisError && <div className="error-message">{analysisError}</div>}

          {hasAnalysisContext && (
            <>
              <AgentWorkflow status={workflowStatus} />
              <AgentTraceTimeline result={analysisResult} status={workflowStatus} />
              {analysisResult && <ResultDashboard result={analysisResult} />}
              {analysisResult && (
                <AgentChat incident={incident} analysisResult={analysisResult} />
              )}
            </>
          )}
        </div>

        <aside className="side-column">
          <MetricsPanel metrics={metrics} loading={bootstrapLoading} error={bootstrapError} />
          {hasAnalysisContext && (
            <>
              <MonitoringPanel result={analysisResult} />
              <ObservabilityPanel observability={observability} result={analysisResult} />
              <LangSmithPanel observability={observability} result={analysisResult} />
            </>
          )}
        </aside>
      </main>
    </div>
  );
}

export default App;

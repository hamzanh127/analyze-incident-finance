import { useEffect, useMemo, useState } from 'react';
import {
  Activity,
  AlertTriangle,
  BarChart3,
  Bot,
  BrainCircuit,
  CheckCircle2,
  ChevronDown,
  Clock3,
  Cloud,
  Container,
  Copy,
  DatabaseZap,
  Gauge,
  GitBranch,
  LayoutDashboard,
  LockKeyhole,
  MessageSquareText,
  MonitorCheck,
  Radio,
  RefreshCw,
  Search,
  Server,
  ShieldAlert,
  ShieldCheck,
  Sparkles,
  TerminalSquare,
  XCircle,
} from 'lucide-react';
import { analyzeIncident, getHealth, getMetrics, getObservability } from './api';
import AgentChat from './components/AgentChat';
import IncidentForm from './components/IncidentForm';

const NAV_ITEMS = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'analysis', label: 'Incident Analysis', icon: Search },
  { id: 'chat', label: 'AI Agent Chat', icon: MessageSquareText },
  { id: 'monitoring', label: 'Monitoring', icon: ShieldAlert },
  { id: 'workflow', label: 'LangGraph', icon: GitBranch },
  { id: 'observability', label: 'Observability', icon: Radio },
];

const PLATFORM_CARDS = [
  { key: 'backend', name: 'Backend', icon: Server, accent: 'blue' },
  { key: 'langgraph', name: 'LangGraph', icon: GitBranch, accent: 'cyan' },
  { key: 'grok', name: 'Grok', icon: BrainCircuit, accent: 'green' },
  { key: 'langsmith', name: 'LangSmith', icon: DatabaseZap, accent: 'cyan' },
  { key: 'monitoring', name: 'Monitoring', icon: MonitorCheck, accent: 'green' },
  { key: 'docker', name: 'Docker', icon: Container, accent: 'blue' },
  { key: 'render', name: 'Render', icon: Cloud, accent: 'orange' },
];

const AGENT_STAGES = [
  {
    id: 'supervisor',
    name: 'Supervisor',
    description: 'Coordinates the finance incident analysis and correlation context.',
    resultKey: 'decision',
  },
  {
    id: 'risk',
    name: 'Risk Agent',
    description: 'Scores financial exposure, amount patterns, country and beneficiary risk.',
    resultKey: 'risk_level',
  },
  {
    id: 'fraud',
    name: 'Fraud Agent',
    description: 'Detects suspicious transfer signals and fraud probability.',
    resultKey: 'fraud_suspicion',
  },
  {
    id: 'compliance',
    name: 'Compliance Agent',
    description: 'Evaluates AML, KYC and escalation requirements.',
    resultKey: 'compliance_status',
  },
  {
    id: 'monitoring',
    name: 'Monitoring Agent',
    description: 'Runs security checks, telemetry and LangSmith trace metadata.',
    resultKey: 'monitoring',
  },
  {
    id: 'report',
    name: 'Final Report',
    description: 'Compiles the final decision, recommendations and analyst-ready summary.',
    resultKey: 'report',
  },
];

const getServiceStatus = (health) => health?.status || health?.service_status || 'unknown';
const getEnvironment = (health, observability) => observability?.environment || health?.environment || 'local';
const getVersion = (health, observability) => observability?.version || health?.version || '1.6.0';
const normalizeBool = (value) => (value ? 'Enabled' : 'Disabled');
const valueOrDash = (value) => (value === undefined || value === null || value === '' ? 'N/A' : String(value));

const getLangSmithEnabled = (observability, result) => Boolean(
  result?.monitoring?.langsmith?.enabled ??
  observability?.langsmith_enabled ??
  observability?.enabled
);

const getAiSafety = (result) => result?.report?.ai_safety || result?.monitoring?.ai_safety || {};
const getStaticChecks = (result) => getAiSafety(result)?.static_checks || {};
const getFinalSecurityDecision = (result) => getAiSafety(result)?.final_decision || {};
const getGrokReview = (result) => getAiSafety(result)?.grok_safety_review || {};
const getExecutionTime = (result) => result?.monitoring?.execution_time_ms || result?.monitoring?.latency_ms || 0;

const getMetricValue = (metrics, keys, fallback = 0) => {
  const keyList = Array.isArray(keys) ? keys : [keys];
  const found = keyList.map((key) => metrics?.[key]).find((value) => value !== undefined && value !== null);
  return found ?? fallback;
};

const deriveDecisionBadge = (decision) => {
  const normalized = String(decision || '').toLowerCase();
  if (['approved', 'accepted', 'allow'].includes(normalized)) return 'success';
  if (['blocked', 'rejected', 'block'].includes(normalized)) return 'danger';
  if (normalized.includes('review')) return 'warning';
  return 'default';
};

const buildIncidentRecord = (incident, result) => ({
  correlation_id: result?.correlation_id || 'N/A',
  decision: result?.decision || 'manual_review',
  risk: result?.risk_level || 'medium',
  fraud: result?.fraud_suspicion ? 'suspicious' : 'clear',
  status: result?.monitoring?.status || result?.report?.final_status || 'completed',
  date: new Date().toLocaleString(),
  amount: incident?.amount,
});

function App() {
  const [activePage, setActivePage] = useState('dashboard');
  const [health, setHealth] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [observability, setObservability] = useState(null);
  const [bootstrapLoading, setBootstrapLoading] = useState(true);
  const [bootstrapError, setBootstrapError] = useState(null);
  const [incident, setIncident] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [analysisError, setAnalysisError] = useState(null);
  const [stageStatuses, setStageStatuses] = useState(() => buildStageStatuses('pending'));
  const [recentIncidents, setRecentIncidents] = useState(() => loadRecentIncidents());

  const serviceStatus = getServiceStatus(health);
  const environment = getEnvironment(health, observability);
  const version = getVersion(health, observability);
  const langSmithEnabled = getLangSmithEnabled(observability, analysisResult);

  const dashboardStats = useMemo(() => buildDashboardStats(metrics, recentIncidents), [metrics, recentIncidents]);

  const refreshOperationalData = async () => {
    const [healthResult, metricsResult, observabilityResult] = await Promise.allSettled([
      getHealth(),
      getMetrics(),
      getObservability(),
    ]);

    if (healthResult.status === 'fulfilled') setHealth(healthResult.value);
    if (metricsResult.status === 'fulfilled') setMetrics(metricsResult.value);
    if (observabilityResult.status === 'fulfilled') setObservability(observabilityResult.value);

    const failed = [healthResult, metricsResult].some((result) => result.status === 'rejected');
    setBootstrapError(failed ? 'Some backend supervision data is unavailable.' : null);
    setBootstrapLoading(false);
  };

  useEffect(() => {
    let mounted = true;
    const load = async () => {
      setBootstrapLoading(true);
      await refreshOperationalData();
      if (!mounted) return;
      setBootstrapLoading(false);
    };

    load();
    const interval = window.setInterval(refreshOperationalData, 10000);

    return () => {
      mounted = false;
      window.clearInterval(interval);
    };
  }, []);

  useEffect(() => {
    window.localStorage.setItem('finance_recent_incidents', JSON.stringify(recentIncidents));
  }, [recentIncidents]);

  const runStageAnimation = (finalResultPromise) => {
    setStageStatuses(buildStageStatuses('pending'));
    AGENT_STAGES.forEach((stage, index) => {
      window.setTimeout(() => {
        setStageStatuses((current) => ({
          ...current,
          [stage.id]: { status: 'running', executionTime: null },
        }));
      }, index * 420);
    });

    finalResultPromise
      .then((result) => {
        AGENT_STAGES.forEach((stage, index) => {
          window.setTimeout(() => {
            setStageStatuses((current) => ({
              ...current,
              [stage.id]: {
                status: 'completed',
                executionTime: estimateStageTime(result, index),
              },
            }));
          }, AGENT_STAGES.length * 420 + index * 180);
        });
      })
      .catch(() => {
        setStageStatuses(buildStageStatuses('failed'));
      });
  };

  const handleAnalyze = async (payload) => {
    setIncident(payload);
    setAnalysisResult(null);
    setAnalysisError(null);
    setAnalysisLoading(true);
    setActivePage('analysis');

    const analysisPromise = analyzeIncident(payload);
    runStageAnimation(analysisPromise);

    try {
      const data = await analysisPromise;
      setAnalysisResult(data);
      setRecentIncidents((current) => [buildIncidentRecord(payload, data), ...current].slice(0, 8));
      refreshOperationalData();
    } catch (err) {
      setAnalysisError(err.message || 'Incident analysis failed.');
      setStageStatuses(buildStageStatuses('failed'));
    } finally {
      setAnalysisLoading(false);
    }
  };

  const pageProps = {
    health,
    metrics,
    observability,
    incident,
    result: analysisResult,
    loading: analysisLoading,
    error: analysisError,
    stageStatuses,
    recentIncidents,
    dashboardStats,
    bootstrapLoading,
    bootstrapError,
    langSmithEnabled,
    onAnalyze: handleAnalyze,
    onRefresh: refreshOperationalData,
  };

  return (
    <div className="supervision-shell">
      <Sidebar activePage={activePage} setActivePage={setActivePage} />
      <div className="workspace">
        <Header
          environment={environment}
          serviceStatus={serviceStatus}
          correlationId={analysisResult?.correlation_id}
          version={version}
        />
        <main className="page-surface">
          {renderPage(activePage, pageProps)}
        </main>
      </div>
    </div>
  );
}

const Sidebar = ({ activePage, setActivePage }) => (
  <aside className="sidebar">
    <div className="brand-block">
      <div className="brand-orbit"><Sparkles size={22} /></div>
      <div>
        <strong>Finance AI Ops</strong>
        <span>Multi-Agent Control</span>
      </div>
    </div>

    <nav className="nav-menu" aria-label="Main navigation">
      {NAV_ITEMS.map((item) => {
        const Icon = item.icon;
        return (
          <button
            type="button"
            className={`nav-item ${activePage === item.id ? 'nav-item-active' : ''}`}
            key={item.id}
            onClick={() => setActivePage(item.id)}
          >
            <Icon size={18} />
            <span>{item.label}</span>
          </button>
        );
      })}
    </nav>

    <div className="sidebar-footer">
      <span>Workflow</span>
      <strong>Supervisor → Report</strong>
    </div>
  </aside>
);

const Header = ({ environment, serviceStatus, correlationId, version }) => (
  <header className="top-header">
    <div>
      <span className="eyebrow">Finance Incident Multi-Agent</span>
      <h1>AI Supervision Platform</h1>
    </div>
    <div className="header-status-grid">
      <StatusChip label="Environment" value={environment} tone="cyan" />
      <StatusChip label="Backend Status" value={serviceStatus} tone={isHealthy(serviceStatus) ? 'green' : 'orange'} />
      <StatusChip label="Correlation ID" value={correlationId || 'No active run'} tone="blue" />
      <StatusChip label="Version" value={version} tone="default" />
    </div>
  </header>
);

const DashboardPage = ({
  health,
  metrics,
  observability,
  result,
  recentIncidents,
  dashboardStats,
  bootstrapLoading,
  bootstrapError,
  langSmithEnabled,
  onRefresh,
}) => (
  <div className="page-grid">
    <PageIntro
      eyebrow="Dashboard"
      title="Finance multi-agent supervision overview"
      description="Global status of the AI platform, incident throughput and latest analysis outcomes."
      action={<button className="icon-button" type="button" onClick={onRefresh} aria-label="Refresh dashboard"><RefreshCw size={18} /></button>}
    />

    {bootstrapError && <div className="notice notice-warning">{bootstrapError}</div>}

    <section className="panel">
      <SectionHeader title="AI Platform Status" subtitle={bootstrapLoading ? 'Loading backend status...' : 'Runtime availability across the finance incident stack.'} />
      <div className="platform-grid">
        {PLATFORM_CARDS.map((card) => (
          <PlatformStatusCard
            key={card.key}
            card={card}
            status={resolvePlatformStatus(card.key, health, observability, langSmithEnabled)}
          />
        ))}
      </div>
    </section>

    <section className="panel">
      <SectionHeader title="Finance Statistics" subtitle="Operational counters collected from /metrics and recent frontend runs." />
      <div className="stats-grid">
        {dashboardStats.map((stat) => (
          <StatCard key={stat.label} {...stat} />
        ))}
      </div>
    </section>

    <section className="panel">
      <SectionHeader title="Recent Incidents" subtitle="Latest analyzed finance incidents with correlation tracking." />
      <RecentIncidentsTable incidents={recentIncidents} result={result} metrics={metrics} />
    </section>
  </div>
);

const IncidentAnalysisPage = ({ result, loading, error, stageStatuses, onAnalyze }) => (
  <div className="analysis-layout">
    <div className="analysis-form-column">
      <PageIntro
        eyebrow="Incident Analysis"
        title="Analyze a finance incident"
        description="Submit a transaction scenario and watch the Supervisor coordinate the finance agents."
      />
      <IncidentForm onSubmit={onAnalyze} isLoading={loading} />
      {error && <div className="notice notice-danger">{error}</div>}
    </div>

    <div className="analysis-timeline-column">
      <section className="panel">
        <SectionHeader
          title={loading ? 'Supervisor started...' : 'Agent Execution'}
          subtitle="Progressive execution from Supervisor to final report."
        />
        <AgentExecutionList statuses={stageStatuses} result={result} />
      </section>
      {result && <AnalysisSummary result={result} />}
    </div>
  </div>
);

const AgentChatPage = ({ incident, result }) => (
  <div className="chat-page">
    <PageIntro
      eyebrow="AI Agent Chat"
      title="Ask the finance assistant"
      description="Independent conversational interface using the latest incident, analysis result and full chat history."
    />
    <AgentChat incident={incident} analysisResult={result} standalone />
  </div>
);

const MonitoringSecurityPage = ({ result, metrics }) => {
  const staticChecks = getStaticChecks(result);
  const grokReview = getGrokReview(result);
  const finalDecision = getFinalSecurityDecision(result);
  const telemetry = getTelemetryItems(result, metrics);

  return (
    <div className="page-grid">
      <PageIntro
        eyebrow="Monitoring & Security Center"
        title="AI safety, telemetry and final security decision"
        description="Security and operational signals produced by the Monitoring Agent."
      />

      <div className="security-grid">
        <SecurityBlock
          title="Static Security Checks"
          icon={LockKeyhole}
          items={[
            ['Toxicity', staticChecks.toxicity?.status || staticChecks.toxicity?.detected],
            ['Prompt Injection', staticChecks.prompt_injection?.detected],
            ['PII', staticChecks.pii?.detected],
            ['Jailbreak', staticChecks.prompt_injection?.jailbreak || staticChecks.jailbreak?.detected],
          ]}
        />
        <SecurityBlock
          title="Grok AI Safety Review"
          icon={BrainCircuit}
          items={[
            ['Overall Risk', grokReview.overall_risk],
            ['Recommended Action', grokReview.recommended_action],
            ['Reason', grokReview.reason || grokReview.rationale],
            ['Confidence', grokReview.confidence],
          ]}
        />
        <SecurityBlock title="Telemetry" icon={Gauge} items={telemetry} />
        <SecurityBlock
          title="Final Security Decision"
          icon={ShieldCheck}
          items={[
            ['Safe', finalDecision.safe ?? getAiSafety(result)?.safe],
            ['Blocked', finalDecision.action === 'block'],
            ['Manual Review', finalDecision.action === 'manual_review'],
            ['Allow', finalDecision.action === 'allow'],
          ]}
        />
      </div>
    </div>
  );
};

const LangGraphWorkflowPage = ({ result, loading, stageStatuses }) => (
  <div className="page-grid">
    <PageIntro
      eyebrow="LangGraph Workflow"
      title="Financial incident graph execution"
      description="A dedicated view of the Supervisor-to-Report workflow observed by the frontend."
    />
    <section className="workflow-canvas">
      {AGENT_STAGES.map((stage, index) => (
        <div className="workflow-stack" key={stage.id}>
          <WorkflowNode stage={stage} status={stageStatuses[stage.id]} result={result} loading={loading} />
          {index < AGENT_STAGES.length - 1 && <ChevronDown className="workflow-chevron" size={26} />}
        </div>
      ))}
    </section>
  </div>
);

const ObservabilityPage = ({ observability, result, metrics, langSmithEnabled }) => {
  const [copied, setCopied] = useState(false);
  const correlationId = result?.correlation_id || '';
  const langsmith = result?.monitoring?.langsmith || {};
  const copyCorrelationId = async () => {
    if (!correlationId) return;
    await navigator.clipboard.writeText(correlationId);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1600);
  };

  return (
    <div className="page-grid">
      <PageIntro
        eyebrow="Observability"
        title="Correlation, metrics, logs and LangSmith"
        description="Trace the run without changing the backend business logic."
      />
      <div className="observability-layout">
        <section className="panel">
          <SectionHeader title="Trace Metadata" subtitle="Current run identifiers and execution context." />
          <div className="detail-grid">
            <DetailItem label="Correlation ID" value={correlationId || 'No active run'} />
            <DetailItem label="Execution Time" value={`${getExecutionTime(result)} ms`} />
            <DetailItem label="Logs" value={normalizeBool(result?.monitoring?.observability?.logs_enabled)} />
            <DetailItem label="Metrics" value={normalizeBool(result?.monitoring?.observability?.metrics_enabled)} />
            <DetailItem label="Run Name" value={langsmith.run_name || 'finance_incident_analysis'} />
            <DetailItem label="Requests" value={getMetricValue(metrics, ['total_requests', 'requests'])} />
          </div>
        </section>

        <section className="panel">
          <SectionHeader title="LangSmith Status" subtitle="External observability project configuration." />
          <div className="detail-grid">
            <DetailItem label="Status" value={langSmithEnabled ? 'Enabled' : 'Disabled'} />
            <DetailItem label="Project" value={langsmith.project || observability?.project || 'finance-incident-multi-agent'} />
            <DetailItem label="Tracing Enabled" value={normalizeBool(observability?.tracing || langSmithEnabled)} />
            <DetailItem label="Application Version" value={observability?.version || '1.6.0'} />
            <DetailItem label="Environment" value={observability?.environment || 'local'} />
            <DetailItem label="Trace Available" value={normalizeBool(langsmith.trace_available)} />
          </div>
          <div className="button-row">
            <a className="btn btn-primary btn-inline" href="https://smith.langchain.com/" target="_blank" rel="noreferrer">
              <DatabaseZap size={17} />
              Open LangSmith
            </a>
            <button className="btn btn-secondary btn-inline" type="button" onClick={copyCorrelationId} disabled={!correlationId}>
              <Copy size={17} />
              {copied ? 'Copied' : 'Copy Correlation ID'}
            </button>
          </div>
        </section>
      </div>
    </div>
  );
};

const PageIntro = ({ eyebrow, title, description, action }) => (
  <div className="page-intro">
    <div>
      <span className="eyebrow">{eyebrow}</span>
      <h2>{title}</h2>
      <p>{description}</p>
    </div>
    {action}
  </div>
);

const SectionHeader = ({ title, subtitle }) => (
  <div className="section-header">
    <div>
      <h3>{title}</h3>
      {subtitle && <p>{subtitle}</p>}
    </div>
  </div>
);

const StatusChip = ({ label, value, tone = 'default' }) => (
  <div className={`status-chip status-chip-${tone}`}>
    <span>{label}</span>
    <strong>{value}</strong>
  </div>
);

const PlatformStatusCard = ({ card, status }) => {
  const Icon = card.icon;
  return (
    <div className={`platform-card platform-${card.accent}`}>
      <div className="platform-icon"><Icon size={22} /></div>
      <div>
        <span>{card.name}</span>
        <strong>{status.label}</strong>
      </div>
      <StatusDot tone={status.tone} />
    </div>
  );
};

const StatCard = ({ label, value, icon: Icon, tone }) => (
  <div className={`stat-card stat-${tone || 'default'}`}>
    <div className="stat-icon">{Icon ? <Icon size={20} /> : <BarChart3 size={20} />}</div>
    <span>{label}</span>
    <strong>{value}</strong>
  </div>
);

const Badge = ({ children, tone = 'default' }) => (
  <span className={`badge badge-${tone}`}>{children}</span>
);

const StatusDot = ({ tone }) => <span className={`status-dot status-dot-${tone}`} />;

const RecentIncidentsTable = ({ incidents, result }) => {
  const rows = incidents.length > 0 ? incidents : result ? [buildIncidentRecord({}, result)] : [];
  if (rows.length === 0) {
    return <div className="empty-state">No incident analyzed yet. Submit an incident to populate this supervision table.</div>;
  }

  return (
    <div className="table-wrap">
      <table className="data-table">
        <thead>
          <tr>
            <th>Correlation ID</th>
            <th>Decision</th>
            <th>Risk</th>
            <th>Fraud</th>
            <th>Status</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((incident) => (
            <tr key={`${incident.correlation_id}-${incident.date}`}>
              <td>{incident.correlation_id}</td>
              <td><Badge tone={deriveDecisionBadge(incident.decision)}>{incident.decision}</Badge></td>
              <td>{incident.risk}</td>
              <td>{incident.fraud}</td>
              <td>{incident.status}</td>
              <td>{incident.date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const AgentExecutionList = ({ statuses, result }) => (
  <div className="execution-list">
    {AGENT_STAGES.map((stage, index) => {
      const state = statuses[stage.id] || { status: 'pending' };
      return (
        <div className={`execution-step execution-${state.status}`} key={stage.id}>
          <div className="step-index">{index + 1}</div>
          <div>
            <h4>{stage.name}</h4>
            <p>{stage.description}</p>
            <strong>{getStageResult(stage, result)}</strong>
          </div>
          <Badge tone={statusToTone(state.status)}>{state.status}</Badge>
        </div>
      );
    })}
  </div>
);

const AnalysisSummary = ({ result }) => (
  <section className="panel">
    <SectionHeader title="Final Analysis Result" subtitle="Decision outputs returned by the multi-agent backend." />
    <div className="summary-grid">
      <DetailItem label="Decision" value={result.decision} tone={deriveDecisionBadge(result.decision)} />
      <DetailItem label="Risk" value={`${result.risk_level} (${result.risk_score})`} />
      <DetailItem label="Fraud" value={`${result.fraud_suspicion ? 'suspicious' : 'clear'} (${result.fraud_score})`} />
      <DetailItem label="Compliance" value={result.compliance_status} />
    </div>
    <div className="recommendation-block">
      <span>Recommendations</span>
      <ul>
        {(result.recommendations || []).map((recommendation) => (
          <li key={recommendation}>{recommendation}</li>
        ))}
      </ul>
    </div>
  </section>
);

const SecurityBlock = ({ title, icon: Icon, items }) => (
  <section className="panel security-block">
    <div className="security-title">
      <Icon size={20} />
      <h3>{title}</h3>
    </div>
    <div className="security-list">
      {items.map(([label, value]) => (
        <div className="security-row" key={label}>
          <span>{label}</span>
          <Badge tone={securityTone(value)}>{formatSecurityValue(value)}</Badge>
        </div>
      ))}
    </div>
  </section>
);

const WorkflowNode = ({ stage, status, result }) => {
  const state = status || { status: 'pending' };
  return (
    <article className={`workflow-node-large workflow-node-${state.status}`}>
      <div className="workflow-node-header">
        <div className="workflow-node-icon"><Bot size={22} /></div>
        <div>
          <h3>{stage.name}</h3>
          <p>{stage.description}</p>
        </div>
        <Badge tone={statusToTone(state.status)}>{state.status}</Badge>
      </div>
      <div className="workflow-node-details">
        <DetailItem label="Execution Time" value={state.executionTime ? `${state.executionTime} ms` : 'Pending'} />
        <DetailItem label="Result" value={getStageResult(stage, result)} />
      </div>
    </article>
  );
};

const DetailItem = ({ label, value, tone }) => (
  <div className={`detail-item ${tone ? `detail-${tone}` : ''}`}>
    <span>{label}</span>
    <strong>{valueOrDash(value)}</strong>
  </div>
);

const renderPage = (activePage, props) => {
  const pages = {
    dashboard: <DashboardPage {...props} />,
    analysis: <IncidentAnalysisPage {...props} />,
    chat: <AgentChatPage {...props} />,
    monitoring: <MonitoringSecurityPage {...props} />,
    workflow: <LangGraphWorkflowPage {...props} />,
    observability: <ObservabilityPage {...props} />,
  };
  return pages[activePage] || pages.dashboard;
};

function buildStageStatuses(status) {
  return AGENT_STAGES.reduce((accumulator, stage) => ({
    ...accumulator,
    [stage.id]: { status, executionTime: null },
  }), {});
}

function estimateStageTime(result, index) {
  const total = Number(getExecutionTime(result)) || 120;
  return Math.max(8, Math.round(total / AGENT_STAGES.length + index * 3));
}

function getStageResult(stage, result) {
  if (!result) return 'Awaiting analysis';
  const values = {
    supervisor: result.decision,
    risk: `${result.risk_level} / ${result.risk_score}`,
    fraud: `${result.fraud_suspicion ? 'suspicious' : 'clear'} / ${result.fraud_score}`,
    compliance: result.compliance_status,
    monitoring: result.monitoring?.status || 'processed',
    report: result.report?.final_status || 'completed',
  };
  return values[stage.id] || valueOrDash(result[stage.resultKey]);
}

function statusToTone(status) {
  if (status === 'completed') return 'success';
  if (status === 'running') return 'warning';
  if (status === 'failed') return 'danger';
  return 'default';
}

function securityTone(value) {
  const normalized = String(value).toLowerCase();
  if (value === false || ['safe', 'allow', 'allowed', 'low', 'none', 'clean'].includes(normalized)) return 'success';
  if (value === true || ['blocked', 'block', 'high', 'unsafe'].includes(normalized)) return 'danger';
  if (['manual_review', 'review', 'medium', 'warning', 'sanitize'].includes(normalized)) return 'warning';
  return 'default';
}

function formatSecurityValue(value) {
  if (value === undefined || value === null || value === '') return 'N/A';
  if (typeof value === 'boolean') return value ? 'Yes' : 'No';
  return String(value);
}

function getTelemetryItems(result, metrics) {
  const staticChecks = getStaticChecks(result);
  return [
    ['Latency', `${getMetricValue(metrics, ['average_latency_ms', 'avg_latency_ms'], getExecutionTime(result))} ms`],
    ['Tokens', staticChecks.tokens?.estimated_tokens],
    ['Estimated Cost', staticChecks.cost?.estimated_cost],
    ['Execution Time', `${getExecutionTime(result)} ms`],
    ['Requests', getMetricValue(metrics, ['total_requests', 'requests'])],
    ['Errors', getMetricValue(metrics, ['total_errors', 'errors'])],
  ];
}

function buildDashboardStats(metrics, recentIncidents) {
  const total = getMetricValue(metrics, ['total_requests', 'requests'], recentIncidents.length);
  const highRisk = getMetricValue(metrics, ['total_high_risk', 'high_risk'], recentIncidents.filter((item) => item.risk === 'high').length);
  const manualReview = getMetricValue(metrics, ['total_manual_review', 'manual_review'], recentIncidents.filter((item) => item.decision?.includes('review')).length);
  const blocked = getMetricValue(metrics, ['total_blocked', 'blocked'], recentIncidents.filter((item) => item.decision === 'blocked').length);
  const approved = getMetricValue(metrics, ['total_approved', 'approved'], recentIncidents.filter((item) => item.decision === 'approved').length);

  return [
    { label: 'Total analyses', value: total, icon: Activity, tone: 'blue' },
    { label: 'High Risk', value: highRisk, icon: AlertTriangle, tone: 'danger' },
    { label: 'Manual Review', value: manualReview, icon: Clock3, tone: 'warning' },
    { label: 'Blocked', value: blocked, icon: XCircle, tone: 'danger' },
    { label: 'Approved', value: approved, icon: CheckCircle2, tone: 'success' },
    { label: 'Average Risk Score', value: getMetricValue(metrics, ['average_risk_score', 'avg_risk_score'], 'N/A'), icon: Gauge, tone: 'cyan' },
    { label: 'Average Fraud Score', value: getMetricValue(metrics, ['average_fraud_score', 'avg_fraud_score'], 'N/A'), icon: ShieldAlert, tone: 'orange' },
    { label: 'Average Latency', value: `${getMetricValue(metrics, ['average_latency_ms', 'avg_latency_ms'], 0)} ms`, icon: TerminalSquare, tone: 'green' },
  ];
}

function resolvePlatformStatus(key, health, observability, langSmithEnabled) {
  const healthy = isHealthy(getServiceStatus(health));
  const statusMap = {
    backend: { label: healthy ? 'online' : 'degraded', tone: healthy ? 'success' : 'warning' },
    langgraph: { label: 'compiled', tone: 'success' },
    grok: { label: 'configured', tone: 'success' },
    langsmith: { label: langSmithEnabled ? 'tracing' : 'disabled', tone: langSmithEnabled ? 'success' : 'default' },
    monitoring: { label: 'active', tone: 'success' },
    docker: { label: 'ready', tone: 'success' },
    render: { label: observability?.environment === 'production' ? 'production' : 'configured', tone: 'warning' },
  };
  return statusMap[key] || { label: 'unknown', tone: 'default' };
}

function isHealthy(status) {
  return ['ok', 'healthy', 'running', 'available'].includes(String(status).toLowerCase());
}

function loadRecentIncidents() {
  try {
    return JSON.parse(window.localStorage.getItem('finance_recent_incidents') || '[]');
  } catch {
    return [];
  }
}

export default App;

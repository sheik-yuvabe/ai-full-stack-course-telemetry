import { useEffect, useMemo, useRef, useState } from "react";
import { useInfiniteQuery, useQuery } from "@tanstack/react-query";
import { AnimatePresence, animate, motion } from "framer-motion";
import { format, isValid, parseISO } from "date-fns";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const dataEndpoint =
  import.meta.env.VITE_BACKEND_API_URL ||
  "https://sheiknoorullah-telemetry-backend.hf.space/api/data";

const pageSize = 8;

function deriveApiBase(endpoint) {
  try {
    const url = new URL(endpoint);
    url.pathname = url.pathname.replace(/\/api\/data\/?$/, "/api");
    return url.toString().replace(/\/$/, "");
  } catch (_error) {
    return endpoint.replace(/\/api\/data\/?$/, "/api");
  }
}

function buildApiUrl(base, path, params = {}) {
  const url = new URL(`${base}${path}`);
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      url.searchParams.set(key, String(value));
    }
  });
  return url.toString();
}

async function fetchJson(url) {
  const response = await fetch(url, {
    headers: {
      Accept: "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  return response.json();
}

function formatDayLabel(value) {
  const parsed = parseDayValue(value);
  return parsed ? format(parsed, "dd MMM yyyy") : "Unknown";
}

function formatTimestamp(value) {
  if (!value) {
    return "Unknown";
  }

  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    return "Unknown";
  }

  return new Intl.DateTimeFormat("en-IN", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(parsed);
}

function parseDayValue(value) {
  if (!value) {
    return null;
  }

  const parsed = parseISO(value);
  return isValid(parsed) ? parsed : null;
}

function getInitials(name) {
  return (name || "Student")
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase())
    .join("");
}

function buildAvatarGradient(seed) {
  const palettes = [
    ["#f7d9a8", "#f28b82"],
    ["#d6e8c8", "#78a97a"],
    ["#d7defd", "#7a8bd0"],
    ["#ffd8c2", "#ee9b73"],
    ["#d8f0ef", "#5ea39a"],
  ];
  const index = (seed || "")
    .split("")
    .reduce((total, char) => total + char.charCodeAt(0), 0) % palettes.length;
  const [start, end] = palettes[index];
  return `linear-gradient(135deg, ${start}, ${end})`;
}

function useDebouncedValue(value, delayMs) {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const timeoutId = window.setTimeout(() => {
      setDebounced(value);
    }, delayMs);

    return () => window.clearTimeout(timeoutId);
  }, [value, delayMs]);

  return debounced;
}

function useThemePreference() {
  const [themeMode, setThemeMode] = useState(() => {
    if (typeof window === "undefined") {
      return "system";
    }
    return window.localStorage.getItem("mentor-theme-mode") || "system";
  });
  const [prefersDark, setPrefersDark] = useState(() => {
    if (typeof window === "undefined") {
      return false;
    }
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  });

  useEffect(() => {
    if (typeof window === "undefined") {
      return undefined;
    }

    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
    const handleChange = (event) => setPrefersDark(event.matches);

    mediaQuery.addEventListener("change", handleChange);
    return () => mediaQuery.removeEventListener("change", handleChange);
  }, []);

  const resolvedTheme =
    themeMode === "system" ? (prefersDark ? "dark" : "light") : themeMode;

  useEffect(() => {
    document.documentElement.dataset.theme = resolvedTheme;
    window.localStorage.setItem("mentor-theme-mode", themeMode);
  }, [resolvedTheme, themeMode]);

  return { themeMode, setThemeMode };
}

function parseStructuredSummary(summary) {
  if (!summary) {
    return [];
  }

  const pattern =
    /(Lesson|Task|Assessment|Gap|Tutor action):\s*([\s\S]*?)(?=(?:Lesson|Task|Assessment|Gap|Tutor action):|$)/gi;
  const items = [];

  for (const match of summary.matchAll(pattern)) {
    items.push({
      label: match[1],
      value: match[2].trim().replace(/\.$/, ""),
    });
  }

  return items;
}

function ThemeSwitcher({ themeMode, onChange }) {
  const options = [
    { label: "Light", value: "light" },
    { label: "Dark", value: "dark" },
    { label: "System", value: "system" },
  ];

  return (
    <div className="theme-switcher" role="group" aria-label="Theme mode">
      {options.map((option) => (
        <button
          key={option.value}
          type="button"
          className={
            themeMode === option.value
              ? "theme-switcher__button theme-switcher__button--active"
              : "theme-switcher__button"
          }
          onClick={() => onChange(option.value)}
        >
          {option.label}
        </button>
      ))}
    </div>
  );
}

function AnimatedNumber({ value, suffix = "" }) {
  const [displayValue, setDisplayValue] = useState(0);
  const previousValueRef = useRef(0);

  useEffect(() => {
    const controls = animate(previousValueRef.current, value, {
      duration: 0.6,
      ease: "easeOut",
      onUpdate(latest) {
        setDisplayValue(latest);
      },
      onComplete() {
        previousValueRef.current = value;
      },
    });

    return () => controls.stop();
  }, [value]);

  return (
    <>
      {Math.round(displayValue)}
      {suffix}
    </>
  );
}

function StatCard({
  label,
  value,
  detail,
  tone = "default",
  animated = false,
  suffix = "",
}) {
  return (
    <article className={`stat-card stat-card--${tone}`}>
      <span>{label}</span>
      <strong>
        {animated ? <AnimatedNumber value={Number(value) || 0} suffix={suffix} /> : value}
      </strong>
      <small>{detail}</small>
    </article>
  );
}

function SummaryPanel({ summary }) {
  return (
    <article className="panel panel--summary">
      <div className="section-heading">
        <p>Summary of the day</p>
        <h2>What the mentor should read first</h2>
      </div>

      <p className="lead">
        {summary?.narrative || "No group summary is available for this day."}
      </p>

      <div className="summary-grid">
        <section className="summary-block">
          <h3>Top blocker patterns</h3>
          <div className="summary-list">
            {(summary?.top_reasons || []).map((item) => (
              <div key={item.reason} className="summary-chip">
                <strong>{item.reason}</strong>
                <span>{item.count} reports</span>
              </div>
            ))}
            {!summary?.top_reasons?.length ? (
              <p className="muted">No blocker patterns detected.</p>
            ) : null}
          </div>
        </section>

        <section className="summary-block">
          <h3>Repeated concepts</h3>
          <div className="summary-list">
            {(summary?.key_concepts || []).map((item) => (
              <div key={item} className="summary-chip summary-chip--concept">
                <strong>{item}</strong>
              </div>
            ))}
            {!summary?.key_concepts?.length ? (
              <p className="muted">No recurring concepts detected.</p>
            ) : null}
          </div>
        </section>
      </div>

      <section className="summary-block">
        <h3>Recommended tutor actions</h3>
        <div className="summary-list">
          {(summary?.recommended_actions || []).map((item) => (
            <div key={item} className="action-row">
              <span>{item}</span>
            </div>
          ))}
          {!summary?.recommended_actions?.length ? (
            <p className="muted">No recommended actions generated.</p>
          ) : null}
        </div>
      </section>
    </article>
  );
}

function SummaryDetails({ summary }) {
  const items = parseStructuredSummary(summary);

  if (items.length === 0) {
    return <p className="lead lead--compact">{summary}</p>;
  }

  return (
    <dl className="definition-list">
      {items.map((item) => (
        <div key={`${item.label}-${item.value}`} className="definition-list__item">
          <dt>{item.label}</dt>
          <dd>{item.value}</dd>
        </div>
      ))}
    </dl>
  );
}

function StudentCard({ report, onOpen }) {
  return (
    <motion.button
      type="button"
      className="student-card"
      onClick={() => onOpen(report.student_id)}
      whileHover={{ y: -4 }}
      whileTap={{ scale: 0.99 }}
      layout
    >
      <div className="student-card__header">
        <div
          className="avatar"
          style={{ backgroundImage: buildAvatarGradient(report.student_id) }}
        >
          <span>{getInitials(report.student_id)}</span>
        </div>

        <div className="student-card__identity">
          <div className="student-card__title-row">
            <strong>{report.student_id}</strong>
            {report.needs_attention ? (
              <span className="attention-badge">Needs attention</span>
            ) : (
              <span className="attention-badge attention-badge--calm">Stable</span>
            )}
          </div>
          <p>{report.latest_summary}</p>
        </div>
      </div>

      <div className="student-card__meta">
        <span>
          <AnimatedNumber value={report.report_count} /> reports
        </span>
        <span>{formatTimestamp(report.latest_timestamp)}</span>
      </div>

      <div className="trigger-strip">
        {report.triggers.slice(0, 3).map((trigger) => (
          <span key={trigger.reason} className="reason-badge">
            {trigger.reason} - {trigger.count}
          </span>
        ))}
      </div>

      <div className="score-row">
        <div className="score-item">
          <span>Progress signal</span>
          <strong>
            <AnimatedNumber value={report.progress_score} suffix="%" />
          </strong>
        </div>
        <div className="progress-track">
          <motion.div
            className="progress-fill"
            initial={{ width: 0 }}
            animate={{ width: `${report.progress_score}%` }}
            transition={{ duration: 0.45, ease: "easeOut" }}
          />
        </div>
      </div>
    </motion.button>
  );
}

function DetailDrawer({ selectedDate, studentId, apiBase, onClose }) {
  const detailQuery = useQuery({
    queryKey: ["student-detail", selectedDate, studentId],
    enabled: Boolean(studentId),
    queryFn: () =>
      fetchJson(
        buildApiUrl(apiBase, "/student-report-detail", {
          report_date: selectedDate,
          student_id: studentId,
        }),
      ),
  });

  const detail = detailQuery.data;

  return (
    <AnimatePresence>
      {studentId ? (
        <>
          <motion.div
            className="drawer-backdrop"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />
          <motion.aside
            className="drawer"
            initial={{ x: "100%" }}
            animate={{ x: 0 }}
            exit={{ x: "100%" }}
            transition={{ type: "spring", stiffness: 280, damping: 30 }}
          >
            <div className="drawer__content">
              <button type="button" className="drawer__close" onClick={onClose}>
                Close
              </button>

              {detailQuery.isLoading ? (
                <div className="drawer__loading">
                  <strong>Loading student report...</strong>
                </div>
              ) : null}

              {detailQuery.isError ? (
                <div className="drawer__loading">
                  <strong>Unable to load student detail.</strong>
                </div>
              ) : null}

              {detail ? (
                <>
                  <div className="drawer__hero">
                    <div
                      className="avatar avatar--large"
                      style={{ backgroundImage: buildAvatarGradient(detail.student_id) }}
                    >
                      <span>{getInitials(detail.student_id)}</span>
                    </div>
                    <div className="drawer__hero-copy">
                      <p className="eyebrow">Student report</p>
                      <h2>{detail.student_id}</h2>
                      <div className="drawer__badges">
                        <span className="reason-badge">{detail.latest_trigger_reason}</span>
                        {detail.needs_attention ? (
                          <span className="attention-badge">Needs attention</span>
                        ) : (
                          <span className="attention-badge attention-badge--calm">
                            Stable
                          </span>
                        )}
                      </div>
                    </div>
                  </div>

                  <div className="drawer__stats">
                    <StatCard
                      label="Reports today"
                      value={detail.report_count}
                      detail="Captured tutor reports"
                      tone="gold"
                      animated
                    />
                    <StatCard
                      label="Attention score"
                      value={detail.attention_score}
                      detail="Higher means more support needed"
                      tone="rose"
                      animated
                      suffix="%"
                    />
                    <StatCard
                      label="Progress signal"
                      value={detail.progress_score}
                      detail="Heuristic signal from the day's reports"
                      tone="sage"
                      animated
                      suffix="%"
                    />
                  </div>

                  <section className="drawer__section">
                    <h3>Latest mentor note</h3>
                    <SummaryDetails summary={detail.latest_summary} />
                  </section>

                  <section className="drawer__section">
                    <h3>All reports for {formatDayLabel(selectedDate)}</h3>
                    <div className="report-stack">
                      {detail.reports.map((report) => (
                        <article key={report.id} className="report-entry">
                          <div className="report-entry__meta">
                            <span className="reason-badge">{report.trigger_reason}</span>
                            <span>{formatTimestamp(report.timestamp)}</span>
                          </div>
                          <SummaryDetails summary={report.ai_reasoning_summary} />
                          <div className="report-entry__context">
                            <span>
                              <strong>File:</strong> {report.file_path || "Unknown"}
                            </span>
                            <span>
                              <strong>Lines:</strong> {report.line_range || "N/A"}
                            </span>
                          </div>
                          <pre className="report-entry__code">
                            <code>{report.excerpt || "# No code snippet provided"}</code>
                          </pre>
                        </article>
                      ))}
                    </div>
                  </section>
                </>
              ) : null}
            </div>
          </motion.aside>
        </>
      ) : null}
    </AnimatePresence>
  );
}

export default function App() {
  const apiBase = useMemo(() => deriveApiBase(dataEndpoint), []);
  const today = useMemo(() => format(new Date(), "yyyy-MM-dd"), []);
  const { themeMode, setThemeMode } = useThemePreference();
  const [selectedDate, setSelectedDate] = useState(today);
  const [studentQuery, setStudentQuery] = useState("");
  const [attentionOnly, setAttentionOnly] = useState(false);
  const [selectedStudentId, setSelectedStudentId] = useState("");
  const debouncedSearch = useDebouncedValue(studentQuery, 260);
  const loadMoreRef = useRef(null);

  const reportDatesQuery = useQuery({
    queryKey: ["report-dates"],
    queryFn: () => fetchJson(buildApiUrl(apiBase, "/report-dates")),
  });

  const summaryQuery = useQuery({
    queryKey: ["group-summary", selectedDate],
    placeholderData: (previousData) => previousData,
    queryFn: () =>
      fetchJson(
        buildApiUrl(apiBase, "/group-summary", {
          report_date: selectedDate,
        }),
      ),
  });

  const reportsQuery = useInfiniteQuery({
    queryKey: ["daily-reports", selectedDate, debouncedSearch, attentionOnly],
    initialPageParam: null,
    placeholderData: (previousData) => previousData,
    queryFn: ({ pageParam }) =>
      fetchJson(
        buildApiUrl(apiBase, "/daily-reports", {
          report_date: selectedDate,
          cursor: pageParam,
          limit: pageSize,
          search: debouncedSearch,
          attention_only: attentionOnly,
        }),
      ),
    getNextPageParam: (lastPage) => lastPage.next_cursor ?? undefined,
  });

  const reportDates = reportDatesQuery.data || [];
  const reportDateSet = useMemo(() => new Set(reportDates), [reportDates]);
  const reportCards = useMemo(
    () => reportsQuery.data?.pages.flatMap((page) => page.items) || [],
    [reportsQuery.data],
  );

  useEffect(() => {
    const node = loadMoreRef.current;
    if (!node || !reportsQuery.hasNextPage || reportsQuery.isFetchingNextPage) {
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0]?.isIntersecting) {
          reportsQuery.fetchNextPage();
        }
      },
      { rootMargin: "280px" },
    );

    observer.observe(node);

    return () => observer.disconnect();
  }, [
    reportsQuery.fetchNextPage,
    reportsQuery.hasNextPage,
    reportsQuery.isFetchingNextPage,
    reportCards.length,
  ]);

  const selectedDateAsDate = parseDayValue(selectedDate) || new Date();
  const highlightedDates = useMemo(
    () => reportDates.map((item) => parseDayValue(item)).filter(Boolean),
    [reportDates],
  );
  const isInitialLoading =
    (summaryQuery.isPending && !summaryQuery.data) ||
    (reportsQuery.isPending && reportCards.length === 0);
  const isRefreshing = summaryQuery.isFetching || reportsQuery.isFetching;

  return (
    <main className="app-shell">
      <section className="hero">
        <div className="hero__header">
          <div>
            <p className="eyebrow">Mentor dashboard</p>
            <h1>Read the day summary, then scan students without losing your place.</h1>
            <p className="hero__copy">
              We moved the working controls closer to the student cards so mentors can
              search, filter, and switch dates while staying in the same review area.
            </p>
          </div>

          <div className="hero__theme">
            <span>Theme</span>
            <ThemeSwitcher themeMode={themeMode} onChange={setThemeMode} />
          </div>
        </div>
      </section>

      <section className="status-strip">
        <div>
          <span>Review mode</span>
          <strong>{formatDayLabel(selectedDate)}</strong>
        </div>
        <div>
          <span>Available report days</span>
          <strong>
            <AnimatedNumber value={reportDates.length} />
          </strong>
        </div>
        <div>
          <span>Reports endpoint</span>
          <strong>{dataEndpoint}</strong>
        </div>
      </section>

      {isInitialLoading || reportDatesQuery.isLoading ? (
        <section className="notice">
          <strong>Preparing the mentor dashboard...</strong>
          <p>Loading summary insights, dates, and report cards.</p>
        </section>
      ) : null}

      {summaryQuery.isError || reportDatesQuery.isError || reportsQuery.isError ? (
        <section className="notice notice--error">
          <strong>Unable to load the mentor dashboard.</strong>
          <p>Try refreshing the page or checking the backend connection.</p>
        </section>
      ) : null}

      {!summaryQuery.isError ? (
        <>
          <section className="stats-grid">
            <StatCard
              label="Selected date"
              value={formatDayLabel(selectedDate)}
              detail={
                reportDateSet.has(selectedDate)
                  ? "Reports exist for this day"
                  : "No reports stored for this date yet"
              }
            />
            <StatCard
              label="Students reported"
              value={summaryQuery.data?.student_count || 0}
              detail="Students with at least one report"
              tone="sage"
              animated
            />
            <StatCard
              label="Needs attention"
              value={summaryQuery.data?.needs_attention_count || 0}
              detail="Students currently flagged for extra support"
              tone="rose"
              animated
            />
            <StatCard
              label="Total reports"
              value={summaryQuery.data?.report_count || 0}
              detail="Tutor-facing reports captured that day"
              tone="gold"
              animated
            />
          </section>

          <section className="review-grid">
            <SummaryPanel summary={summaryQuery.data} />

            <article className="panel panel--cards">
              <div className="section-heading section-heading--inline">
                <div>
                  <p>Student cards</p>
                  <h2>Open a card to read the full report</h2>
                </div>
                <span className="cards-count">
                  <AnimatedNumber value={reportCards.length} /> shown
                  {reportsQuery.data?.pages?.[0]?.total_count
                    ? ` of ${reportsQuery.data.pages[0].total_count}`
                    : ""}
                </span>
              </div>

              <div className="cards-toolbar">
                <label className="field">
                  <span>Review day</span>
                  <DatePicker
                    selected={selectedDateAsDate}
                    onChange={(value) => {
                      const nextDate = value ? format(value, "yyyy-MM-dd") : today;
                      setSelectedDate(nextDate);
                      setSelectedStudentId("");
                    }}
                    dateFormat="dd MMM yyyy"
                    calendarStartDay={1}
                    highlightDates={highlightedDates}
                  />
                </label>

                <label className="field">
                  <span>Find student</span>
                  <input
                    type="search"
                    placeholder="Search by student name"
                    value={studentQuery}
                    onChange={(event) => setStudentQuery(event.target.value)}
                  />
                </label>

                <label className="toggle-field" htmlFor="attention-only">
                  <input
                    id="attention-only"
                    type="checkbox"
                    checked={attentionOnly}
                    onChange={(event) => setAttentionOnly(event.target.checked)}
                  />
                  <span className="toggle-field__switch" aria-hidden="true" />
                  <span>Attention only</span>
                </label>
              </div>

              {isRefreshing ? (
                <div className="cards-updating">
                  <span>Updating results...</span>
                </div>
              ) : null}

              {reportCards.length === 0 && !reportsQuery.isFetching ? (
                <div className="empty-state">
                  <strong>No student reports found for {formatDayLabel(selectedDate)}.</strong>
                  <p>
                    Try another day or remove the attention-only filter to widen the
                    result set.
                  </p>
                </div>
              ) : (
                <motion.div layout className="cards-grid">
                  {reportCards.map((report) => (
                    <StudentCard
                      key={`${report.student_id}-${report.latest_timestamp}`}
                      report={report}
                      onOpen={setSelectedStudentId}
                    />
                  ))}
                </motion.div>
              )}

              <div ref={loadMoreRef} className="load-more">
                {reportsQuery.isFetchingNextPage ? (
                  <span>Loading more reports...</span>
                ) : reportsQuery.hasNextPage ? (
                  <span>Scroll to load more</span>
                ) : reportCards.length > 0 ? (
                  <span>All reports for this date are loaded</span>
                ) : null}
              </div>
            </article>
          </section>
        </>
      ) : null}

      <DetailDrawer
        apiBase={apiBase}
        selectedDate={selectedDate}
        studentId={selectedStudentId}
        onClose={() => setSelectedStudentId("")}
      />
    </main>
  );
}

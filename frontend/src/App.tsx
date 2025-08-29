import { useState } from "react";
import CodeSnippet from "./CodeSnippet";

interface TaskSuggestion {
  id: number;
  title: string;
  file: string;
  description: string;
  estimated_time: number;
}

const API_BASE_URL = "/api"; // via le proxy Nginx

function App() {
  const [repoUrl, setRepoUrl] = useState("");
  const [timeMinutes, setTimeMinutes] = useState<number | "">("");
  const [additionalContext, setAdditionalContext] = useState("");
  const [suggestions, setSuggestions] = useState<TaskSuggestion[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [generatedCode, setGeneratedCode] = useState<string | null>(null);
  const [language, setLanguage] = useState<string>("python");


  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!repoUrl || !timeMinutes) {
      setError("Please fill in at least the repo URL and the time limit fields.");
      return;
    }

    setLoading(true);
    setError(null);
    setSuggestions([]);
    setGeneratedCode(null);

    try {
      const response = await fetch(`${API_BASE_URL}/generate-tasks`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          github_url: repoUrl,
          time_minutes: timeMinutes,
          additional_context: additionalContext,
        }),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data: TaskSuggestion[] = await response.json();
      setSuggestions(data);
    } catch (err: any) {
      setError(err.message || "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  const handleChooseTask = async (taskId: number) => {
    setLoading(true);
    setError(null);
    setGeneratedCode(null);

    try {
      const response = await fetch(`${API_BASE_URL}/generate-code`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ task_id: taskId }),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      setGeneratedCode(data.code || "No code generated");
      setLanguage(data.language || "python");
    } catch (err: any) {
      setError(err.message || "An error occurred");
    } finally {
      setLoading(false);
    }
  };


  return (
    <div style={{ maxWidth: 600, margin: "0 auto", padding: 20 }}>
      <h1>Perlimpinpin</h1>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: 12 }}>
          <label>GitHub Repository URL:</label>
          <input
            type="text"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            style={{ width: "100%", padding: 8 }}
          />
        </div>
        <div style={{ marginBottom: 12 }}>
          <label>Time Available (minutes):</label>
          <input
            type="number"
            value={timeMinutes}
            onChange={(e) => setTimeMinutes(Number(e.target.value))}
            style={{ width: "100%", padding: 8 }}
          />
        </div>
        <div style={{ marginBottom: 12 }}>
          <label>Want to focus on a specific task?</label>
          <input
            type="text"
            value={additionalContext}
            onChange={(e) => setAdditionalContext(e.target.value)}
            style={{ width: "100%", padding: 8 }}
          />
        </div>
        <button type="submit" style={{ padding: "8px 16px" }}>
          Get Suggestions
        </button>
      </form>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {suggestions.length > 0 && (
        <div style={{ marginTop: 20 }}>
          <h2>Task Suggestions</h2>
          <ol>
            {suggestions.map((task, idx) => (
              <li value={task.id} key={idx} style={{ marginBottom: 12 }}>
                <strong>{task.title}</strong> ({task.estimated_time} min)
                <br />
                <em>{task.file}</em>
                <p>{task.description}</p>
                <button
                  onClick={() => handleChooseTask(task.id)}
                  style={{ padding: "6px 12px", marginTop: 8 }}
                >
                  Choose this task
                </button>
              </li>
            ))}
          </ol>
        </div>
      )}

      {generatedCode && (
        <div style={{ marginTop: 20 }}>
          <h2>Generated Code</h2>
          <CodeSnippet code={generatedCode} language={language as any} />
        </div>
      )}
    </div>
  );
}

export default App;
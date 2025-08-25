import { useState } from "react";
import { fetchTasks } from "./api";
import type { TaskSuggestion } from "./api";

function App() {
  const [repoUrl, setRepoUrl] = useState("");
  const [availableTime, setAvailableTime] = useState(30);
  const [tasks, setTasks] = useState<TaskSuggestion[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const result = await fetchTasks(repoUrl, availableTime);
      setTasks(result);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-6">
      <h1 className="text-2xl font-bold mb-4">Task Coach</h1>
      
      <form onSubmit={handleSubmit} className="space-y-3 bg-white p-4 rounded-xl shadow w-full max-w-md">
        <div>
          <label className="block text-sm font-medium mb-1">Lien GitHub :</label>
          <input
            type="text"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            className="w-full p-2 border rounded"
            placeholder="https://github.com/user/repo"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Temps disponible (minutes) :</label>
          <input
            type="number"
            value={availableTime}
            onChange={(e) => setAvailableTime(Number(e.target.value))}
            className="w-full p-2 border rounded"
          />
        </div>

        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
          disabled={loading}
        >
          {loading ? "Chargement..." : "Générer des tâches"}
        </button>
      </form>

      {error && <p className="text-red-500 mt-3">{error}</p>}

      <ul className="mt-6 w-full max-w-md space-y-2">
        {tasks.map((task) => (
          <li key={task.id} className="p-3 bg-white rounded shadow">
            <p className="font-semibold">{task.description}</p>
            <p className="text-sm text-gray-600">⏱ {task.estimated_time}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
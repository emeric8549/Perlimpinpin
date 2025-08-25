export interface TaskSuggestion {
  id: number;
  description: string;
  estimated_time: string;
}

const API_BASE_URL = "http://localhost:8000";

export async function fetchTasks(repoUrl: string, availableTime: number): Promise<TaskSuggestion[]> {
  console.log(repoUrl)
  console.log(JSON.stringify({
      github_url: repoUrl,
      time_minutes: availableTime,
    }),)
  const response = await fetch(`${API_BASE_URL}/generate_tasks`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      github_url: repoUrl,
      time_minutes: availableTime,
    }),
  });

  if (!response.ok) {
    throw new Error(`Erreur API: ${response.statusText}`);
  }

  return response.json();
}
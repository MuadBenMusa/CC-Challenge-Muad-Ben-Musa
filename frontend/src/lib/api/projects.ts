import type { Project, ProjectStatus } from "../types/project";

const apiBaseUrl =
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:18000";


export async function getProjects(
  status?: ProjectStatus
): Promise<Project[]> {
  const url = new URL(`${apiBaseUrl}/projects`);

  if (status) {
    url.searchParams.set("status", status);
  }

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error("Projects could not be loaded.");
  }

  return response.json();
}
import type { DocumentRecord } from "../types/document";

const API_URL = "http://127.0.0.1:8000";

export async function getDocuments(
  signal?: AbortSignal,
): Promise<DocumentRecord[]> {
  const response = await fetch(`${API_URL}/api/documents`, { signal });

  if (!response.ok) {
    throw new Error("Neizdevās ielādēt dokumentus.");
  }

  return response.json();
}
export type Importance = "low" | "medium" | "high" | "critical";

export type DocumentCategory =
  | "public"
  | "internal"
  | "restricted"
  | "confidential";

export interface DocumentRecord {
  id: number;
  external_id: string;
  title: string;
  description: string;
  responsible_unit: string;
  created_at: string;
  url: string;
  file_type: string;
  reading_time_minutes: number;
  importance: Importance;
  category: DocumentCategory;
  active: boolean;
  imported_at: string;
}

export const importanceLabels: Record<Importance, string> = {
  low: "Zems",
  medium: "Vidējs",
  high: "Augsts",
  critical: "Kritisks",
};

export const categoryLabels: Record<DocumentCategory, string> = {
  public: "Publisks",
  internal: "Iekšējs",
  restricted: "Ierobežotas pieejamības",
  confidential: "Konfidenciāls",
};
import { fetchClient } from "./client";
import type { ConvertResponse } from "../types/api";

export async function convertProject(file: File): Promise<ConvertResponse> {
  const formData = new FormData();
  formData.append("file", file);

  return fetchClient<ConvertResponse>("/convert", {
    method: "POST",
    body: formData,
  });
}
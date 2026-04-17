import { fetchClient } from "./client";
import type { ConvertResponse, ExplainResponse } from "../types/api";

export async function explainTranslation(
  translationData: ConvertResponse
): Promise<ExplainResponse> {
  return fetchClient<ExplainResponse>("/explain", {
    method: "POST",
    body: JSON.stringify({ translation_data: translationData }),
  });
}
import client from "./client";

export interface HealthReponse{
  status: string;
}

export async function getHealth(): Promise<HealthResponse> {
  const { data } = await client.get("/health");
  return data;
}

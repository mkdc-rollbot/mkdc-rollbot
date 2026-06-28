import client from "./client";

export interface HealthResponse{
  status: string;
}

export async function getHealth(): Promise<HealthResponse> {
  const { data } = await client.get("/health");
  return data;
}

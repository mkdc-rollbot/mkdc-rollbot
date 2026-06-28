import client from "./client";
import type { Guild } from "../models/guild";

export async function getGuilds(): Promise<Guild[]> {
    const { data } = await client.get("/guilds");
    return data;
}

export async function deleteGuild(id: number): Promise<void> {
    await client.delete(`/guild/${id}`);
}

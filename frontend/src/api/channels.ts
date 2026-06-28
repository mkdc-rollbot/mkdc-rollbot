import client from "./client";
import type { Channel } from "../models/channel";

export async function getChannels(): Promise<Channel[]> {
    const { data } = await client.get("/channels");
    return data;
}

export async function deleteChannel(id: number): Promise<void> {
    await client.delete(`/channel/${id}`);
}

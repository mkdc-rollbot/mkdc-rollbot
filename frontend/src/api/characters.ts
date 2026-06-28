import client from "./client";
import type { Character } from "../models/character";

export async function getCharacters(): Promise<Character[]> {
    const { data } = await client.get("/characters");
    return data;
}

export async function deleteCharacter(id: number): Promise<void> {
  await client.delete(`/character/${id}`);
}

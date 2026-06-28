export interface Character {

    id: number;
    player: number;
    name: string;
    system?: string;
    sheet_data: Record<string, unknown>;
}

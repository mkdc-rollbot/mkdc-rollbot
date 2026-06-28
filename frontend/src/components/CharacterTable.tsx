import { ActionIcon, Group } from "@mantine/core";
import { IconEye, IconTrash } from "@tabler/icons-react";
import { DataTable } from "mantine-datatable";
import type { Character } from "../models/character";

interface Props {
    characters: Character[];

    onView: (character: Character) => void;

    onDelete: (character: Character) => void;
}

export default function CharacterTable({
    characters,
    onView,
    onDelete,
}: Props) {
    return (
        <DataTable
            withTableBorder
            borderRadius="sm"
            striped
            highlightOnHover
            records={characters}
            columns={[
                {
                    accessor: "id",
                    title: "ID",
                },
                {
                    accessor: "name",
                    title: "Name",
                },
                {
                    accessor: "player",
                    title: "Player",
                },
                {
                    accessor: "system",
                    title: "System",
                },
                {
                    accessor: "actions",
                    title: "",
                    render: (character) => (
                        <Group gap="xs">
                            <ActionIcon
                                variant="light"
                                onClick={() => onView(character)}
                            >
                                <IconEye size={18} />
                            </ActionIcon>

                            <ActionIcon
                                color="red"
                                variant="light"
                                onClick={() => onDelete(character)}
                            >
                                <IconTrash size={18} />
                            </ActionIcon>
                        </Group>
                    ),
                },
            ]}
        />
    );
}

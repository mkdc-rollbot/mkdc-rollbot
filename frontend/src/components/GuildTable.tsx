import { ActionIcon, Group } from "@mantine/core";
import { IconTrash } from "@tabler/icons-react";
import { DataTable } from "mantine-datatable";

import type { Guild } from "../models/guild";

interface Props {
    guilds: Guild[];
    onDelete: (guild: Guild) => void;
}

export default function GuildTable({
    guilds,
    onDelete,
}: Props) {

    return (
        <DataTable
            withTableBorder
            striped
            highlightOnHover
            records={guilds}
            columns={[
                {
                    accessor: "id",
                    title: "Guild ID",
                },
                {
                    accessor: "actions",
                    title: "",
                    render: (guild) => (
                        <Group gap="xs">
                            <ActionIcon
                                color="red"
                                variant="light"
                                onClick={() => onDelete(guild)}
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

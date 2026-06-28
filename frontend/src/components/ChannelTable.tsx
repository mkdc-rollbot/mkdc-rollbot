import { ActionIcon, Group } from "@mantine/core";
import { IconTrash } from "@tabler/icons-react";
import { DataTable } from "mantine-datatable";

import type { Channel } from "../models/channel";

interface Props {
    channels: Channel[];
    onDelete: (channel: Channel) => void;
}

export default function ChannelTable({
    channels,
    onDelete,
}: Props) {

    return (
        <DataTable
            withTableBorder
            striped
            highlightOnHover
            records={channels}
            columns={[
                {
                    accessor: "id",
                    title: "Channel",
                },
                {
                    accessor: "guild_id",
                    title: "Guild",
                },
                {
                    accessor: "prefix",
                },
                {
                    accessor: "system",
                },
                {
                    accessor: "actions",
                    render: (channel) => (
                        <Group>
                            <ActionIcon
                                color="red"
                                onClick={() => onDelete(channel)}
                            >
                                <IconTrash size={18}/>
                            </ActionIcon>
                        </Group>
                    ),
                },
            ]}
        />
    );

}

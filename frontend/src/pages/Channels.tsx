import {
    Button,
    Loader,
    Stack,
    Text,
    Title,
    Group,
} from "@mantine/core";

import {
    useMutation,
    useQuery,
    useQueryClient,
} from "@tanstack/react-query";

import {
    getChannels,
    deleteChannel,
} from "../api/channels";

import ChannelTable from "../components/ChannelTable";

import type { Channel } from "../models/channel";

export default function Channels() {

    const queryClient = useQueryClient();

    const mutation = useMutation({
        mutationFn: deleteChannel,
        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: ["channels"],
            });
        },
    });

    const {
        data: channels,
        isLoading,
        error,
        refetch,
    } = useQuery({
        queryKey: ["channels"],
        queryFn: getChannels,
    });

    function handleDelete(channel: Channel) {
        mutation.mutate(channel.id);
    }

    if (isLoading)
        return <Loader />;

    if (error)
        return <Text c="red">Failed to load channels.</Text>;

    return (
        <Stack>

            <Group justify="space-between">

                <Title>
                    Channels
                </Title>

                <Button
                    onClick={() => refetch()}
                >
                    Refresh
                </Button>

            </Group>

            <ChannelTable
                channels={channels ?? []}
                onDelete={handleDelete}
            />

        </Stack>
    );

}

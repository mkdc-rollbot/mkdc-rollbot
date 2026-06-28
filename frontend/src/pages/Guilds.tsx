import {
    Button,
    Group,
    Loader,
    Stack,
    Text,
    Title,
} from "@mantine/core";

import {
    useMutation,
    useQuery,
    useQueryClient,
} from "@tanstack/react-query";

import GuildTable from "../components/GuildTable";

import {
    getGuilds,
    deleteGuild,
} from "../api/guilds";

import type { Guild } from "../models/guild";

export default function Guilds() {

    const queryClient = useQueryClient();

    const deleteMutation = useMutation({
        mutationFn: deleteGuild,

        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: ["guilds"],
            });
        },
    });

    const {
        data: guilds,
        isLoading,
        error,
        refetch,
    } = useQuery({
        queryKey: ["guilds"],
        queryFn: getGuilds,
    });

    function handleDelete(guild: Guild) {
        deleteMutation.mutate(guild.id);
    }

    if (isLoading)
        return <Loader />;

    if (error)
        return (
            <Text c="red">
                Failed to load guilds.
            </Text>
        );

    return (
        <Stack>

            <Group justify="space-between">

                <Title>
                    Guilds
                </Title>

                <Button
                    variant="default"
                    onClick={() => refetch()}
                >
                    Refresh
                </Button>

            </Group>

            <GuildTable
                guilds={guilds ?? []}
                onDelete={handleDelete}
            />

        </Stack>
    );

}

import { Button, Loader, Stack, Text, Title } from "@mantine/core";
import { useQuery, useQueryClient, useMutation } from "@tanstack/react-query";

import CharacterTable from "../components/CharacterTable";
import { getCharacters, deleteCharacter } from "../api/characters";
import type { Character } from "../models/character";



export default function Characters() {
    const queryClient = useQueryClient();

    const deleteMutation = useMutation({
        mutationFn: (id: number) => deleteCharacter(id),

        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: ["characters"],
            });
        },
    });
    const {
        data: characters,
        isLoading,
        error,
        refetch,
    } = useQuery({
        queryKey: ["characters"],
        queryFn: getCharacters,
    });

    function handleView(character: Character) {
        console.log(character);
    }

    function handleDelete(character: Character) {

        if (!confirm("Delete?"))
            return;

        deleteMutation.mutate(character.id);

    }
    if (isLoading) return <Loader />;

    if (error)
        return (
            <Text c="red">
                Failed to load characters.
            </Text>
        );

    return (
        <Stack>

            <Title>
                Characters
            </Title>

            <Button
                w={120}
                onClick={() => refetch()}
            >
                Refresh
            </Button>

            <CharacterTable
                characters={characters ?? []}
                onView={handleView}
                onDelete={handleDelete}
            />

        </Stack>
    );
}

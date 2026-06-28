import { Stack, Button } from "@mantine/core";

interface Props {

    page: string;

    setPage: (page: string) => void;

}

export default function Sidebar({
    setPage,
}: Props) {

    return (

        <Stack p="md">

            <Button onClick={() => setPage("dashboard")}>
                Dashboard
            </Button>

            <Button onClick={() => setPage("characters")}>
                Characters
            </Button>

            <Button onClick={() => setPage("channels")}>
                Channels
            </Button>

            <Button onClick={() => setPage("guilds")}>
                Guilds
            </Button>

        </Stack>

    );

}

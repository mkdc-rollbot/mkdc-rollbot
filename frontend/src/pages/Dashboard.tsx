import { Card, Loader, Text, Title } from "@mantine/core";
import { useQuery } from "@tanstack/react-query";
import { getHealth } from "../api/system";

export default function Dashboard() {

    const { data, isLoading, error } = useQuery({
        queryKey: ["health"],
        queryFn: getHealth,
    });

    return (
      <>
        <Title mb="lg">
          Rollbot Operations Consolle
        </Title>

        <Card shadow="sm" withBorder>

                {isLoading && <Loader />}

                {error && (
                    <Text c="red">
                        API Offline
                    </Text>
                )}

                {data && (
                    <Text>
                        API Status: {data.status}
                    </Text>
                )}

            </Card>
        </>
    );

}

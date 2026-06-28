import { AppShell } from "@mantine/core";
import Sidebar from "../components/Sidebar";
import Dashboard from "../pages/Dashboard";
import { useState } from "react";
import Characters from "../pages/Characters";
import Channels from "../pages/Channels";
import Guilds from "../pages/Guilds";

export default function MainLayout() {

    const [page, setPage] =
        useState("dashboard");

    function render() {

        switch (page) {

            case "characters":
                return <Characters />;

            case "channels":
                return <Channels />;

            case "guilds":
                return <Guilds />;

            default:
                return <Dashboard />;
        }

    }

    return (

        <AppShell
            navbar={{
                width: 250,
                breakpoint: "sm",
            }}
        >

            <AppShell.Navbar>

                <Sidebar
                    page={page}
                    setPage={setPage}
                />

            </AppShell.Navbar>

            <AppShell.Main>

                {render()}

            </AppShell.Main>

        </AppShell>

    );

}

import axios from "axios";

export default axios.create({
    baseURL: "http://localhost:11037",
    headers: {
        "Content-Type": "application/json",
    },
});

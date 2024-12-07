document.addEventListener("DOMContentLoaded", () => {
    const pollForm = document.getElementById("pollForm");
    const resultsList = document.getElementById("results");

    // Handle form submission to vote
    pollForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(pollForm);
        const selectedChoice = formData.get("choice");

        const response = await fetch("/vote", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ choice: selectedChoice }),
        });

        if (response.ok) {
            updateResults();
        }
    });

    // Fetch and update results dynamically
    async function updateResults() {
        const response = await fetch("/results");
        const pollData = await response.json();

        resultsList.innerHTML = "";
        for (const [choice, votes] of Object.entries(pollData.votes)) {
            const listItem = document.createElement("li");
            listItem.textContent = `${choice}: ${votes} votes`;
            resultsList.appendChild(listItem);
        }
    }

    // Update results every 5 seconds
    setInterval(updateResults, 5000);
});

const messagePane = document.querySelector("#messagePane");
if (messagePane) {
  messagePane.scrollTop = messagePane.scrollHeight;
}

const search = document.querySelector("#chatSearch");
const cards = Array.from(document.querySelectorAll(".chat-card"));

if (search) {
  search.addEventListener("input", () => {
    const query = search.value.trim().toLowerCase();
    cards.forEach((card) => {
      card.hidden = !card.dataset.name.includes(query);
    });
  });
}

// Not currently working, not really sure why...

// Define the list of hyperlinks
const links = [
    { text: "Tic-Tac-Toe Project", url: "tic-tac-toe-landing.html" },
    { text: "Deck of Cards Project", url: "deck-of-cards-landing.html" },
    { text: "Home Climbing Wall Project", url: "wall-code-landing.html" },
    { text: "Find My Hat Project", url: "find-my-hat-landing.html" },
    { text: "MTG Chess Clock", url: "mtg-chess-clock-landing.html" }
];

// Get a reference to the "menu" nav element
const menuNav = document.querySelector("#menu");

// Create the "menu" nav element
const nav = document.createElement("nav");

// Create the first ul element with class "links"
const ul1 = document.createElement("ul");
ul1.classList.add("links");

// Iterate through the links and create li element with a elements for the first ul
links.forEach(link => {
    const li = document.createElement("li");
    const a = document.createElement("a");

    // Set the link text and href attribute
    a.textContent = link.text;
    a.href = link.url;

    // Append the anchor element to the list item
    li.appendChild(a);

    // Append the list item to the first unordered list
    ul1.appendChild(li);
});

// Create the second ul element with class "actions stacked"
const ul2 = document.createElement("ul");
ul2.classList.add("actions", "stacked");

// Create a li with a link a element for the "Go Home" link
const li = document.createElement("li");
const a = document.createElement("a");

// Set the link text, href attribute, and class for the "Go Home" link
a.textContent = "Go Home";
a.href = "index.html";
a.classList.add("button", "fit");

// Append the anchor element to the list item
li.appendChild(a);

// Append the list item to the second unordered list
ul2.appendChild(li);

// Append both unordered lists to the "menu" nav element
nav.appendChild(ul1);
nav.appendChild(ul2);

// Append the "menu" nav element to the "menu" nav element in your HTML
menuNav.appendChild(nav);

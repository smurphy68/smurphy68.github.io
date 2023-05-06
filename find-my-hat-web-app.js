// const prompt = require('prompt-sync')({ sigint: true });

let button = document.getElementById("new-game-button");
let gameWindow = document.getElementById("game-console");
let toBeReplaced = document.getElementById("to-be-replaced");

//gameWindow.setAttribute("style", "{min-height:200px;}")

let gameOver = false;
let mouseOver = false;

const wall = '🧱'
const hat = '🎩';
const hole = '🕳️';
const fieldCharacter = '🌿';
const treeCharacter = '🌳'
const pathCharacter = '🪨';
const xCharachter = '❌'
const cowboyHat = '🤠'

// const inputWidth = Number(process.argv[2]);
// const inputHeight = Number(process.argv[3]);
// const inputDifficulty = Number(process.argv[4]);

class Field {
    constructor(width = 19, height = 15, percentage = 0.65) {
        this.array = [];
        for (let i = 0; i <= height; i++) {
            this.array.push(
                new Array(width).fill("").map(e => {
                    return (Math.random() >= percentage) ? e = hole : e = (Math.random() >= 0.5) ? e = fieldCharacter : e = treeCharacter;
                })
            );
        };
        this.array[Math.floor(Math.random() * height)][Math.floor(Math.random() * width)] = hat;
        if (this.array[0][0] != hat) {
            this.array[0][0] = pathCharacter;
            this.playerRow = 0;
            this.playerColumn = 0;
        } else {
            this.array[this.array.length - 1][this.array[0].length - 1] = pathCharacter;
            this.playerRow = this.array.length - 1;
            this.playerColumn = this.array[0].length - 1;
        }
    };

    printArray = () => {
        this.array.forEach(e => {
            console.log(e.join(""));
        })
    };

    returnHTMLString = () => {
        let returnSt = ""
        for (let i = 0; i < this.array.length; i++) {
            returnSt += this.array[i].join("");
            if (i != this.array.length - 1) {
                returnSt += "<br>";
            };
        };
        return "<p>" + returnSt + "</p>";
    };
    makeMove = (input) => {
        if (mouseOver === true && !gameOver) {
            let validMove = true;
            let rows = this.array.length;
            let columns = this.array[0].length
            if (input === "ArrowUp") {
                if (this.playerRow > 0) {
                    this.playerRow -= 1;
                } else {
                    validMove = false;
                }
            } else if (input === "ArrowDown") {
                if (this.playerRow + 1 < rows) {
                    this.playerRow += 1;
                } else {
                    validMove = false;
                }
            } else if (input === "ArrowLeft") {
                if (this.playerColumn > 0) {
                    this.playerColumn -= 1;
                } else {
                    validMove = false;
                }
            } else if (input === "ArrowRight") {
                if (this.playerColumn + 1 < columns) {
                    this.playerColumn += 1;
                } else {
                    validMove = false;
                }
            }

            if (this.array[this.playerRow][this.playerColumn] === hole) {
                button.innerText = "You Lost! Try Again?"
                this.array[this.playerRow][this.playerColumn] = xCharachter;
                gameOver = true;
            } else if (this.array[this.playerRow][this.playerColumn] === hat) {
                gameOver = true;
                button.innerText = "You Won! Try Again?"
                this.array[this.playerRow][this.playerColumn] = cowboyHat;
            } else if (validMove) {
                this.array[this.playerRow][this.playerColumn] = pathCharacter;
            }
            return;
        };
    };
};

gameWindow.addEventListener("mouseenter", () => {
    mouseOver = true;
})
gameWindow.addEventListener("mouseleave", () => {
    mouseOver = false;
})

let Game = new Field()

document.addEventListener("keydown", (e) => {
    if (mouseOver) {
        e.preventDefault()
        Game.makeMove(e.key)
        toBeReplaced.innerHTML = Game.returnHTMLString()
    }
})

function startNewGame() {
    button.innerText = "Click here to play!"
    gameOver = false;
    Game = new Field()
    toBeReplaced.innerHTML = Game.returnHTMLString()
}

startNewGame()

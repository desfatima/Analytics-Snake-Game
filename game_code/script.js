const board = document.querySelector(".play-board");
const scoreElement = document.querySelector(".score");
const highScoreElement = document.querySelector(".high-score");

let gameOver = false;
let foodX, foodY;
let snakeX = 5, snakeY = 5;
let velocityX = 0, velocityY = 0;
let snakeBody = [];
let setIntervalId;
let score = 0;
let movements = [];
let directionChanges = 0;
let lastDirection = "";
let sessionStartTime = new Date();
let failReason = "";

let highScore = localStorage.getItem("high-score") || 0;
highScoreElement.innerText = `High Score: ${highScore}`;

const updateFoodPosition = () => {
    foodX = Math.floor(Math.random() * 30);
    foodY = Math.floor(Math.random() * 30);
};

const handleGameOver = () => {
    clearInterval(setIntervalId);
    gameOver = true;

    // إعداد بيانات الجلسة
    const sessionEndTime = new Date();
    const sessionDuration = sessionEndTime - sessionStartTime;
    const sessionHour = sessionStartTime.getHours();

    const sessionData = {
        duration_ms: sessionDuration,
        startTime: sessionStartTime.toISOString(),
        sessionHour: sessionHour,
        applesEaten: score,
        movements: movements,
        directionChanges: directionChanges,
        failReason: failReason
    };

    const blob = new Blob([JSON.stringify(sessionData, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "Player.json";
    a.click();

    alert("Game Over! Press OK to restart.");
    location.reload();
};

const changeDirection = (e) => {
    let newDirection = "";
    if (e.key === "ArrowUp" && velocityY !== 1) {
        velocityX = 0; velocityY = -1; newDirection = "up";
    } else if (e.key === "ArrowDown" && velocityY !== -1) {
        velocityX = 0; velocityY = 1; newDirection = "down";
    } else if (e.key === "ArrowLeft" && velocityX !== 1) {
        velocityX = -1; velocityY = 0; newDirection = "left";
    } else if (e.key === "ArrowRight" && velocityX !== -1) {
        velocityX = 1; velocityY = 0; newDirection = "right";
    }

    if (newDirection && newDirection !== lastDirection) {
        directionChanges++;
        lastDirection = newDirection;
    }
};

const initGame = () => {
    if (gameOver) return handleGameOver();

    let html = "";
    snakeX += velocityX;
    snakeY += velocityY;

    if (snakeX < 0 || snakeX > 29 || snakeY < 0 || snakeY > 29) {
        failReason = "wall";
        return gameOver = true;
    }

    for (let i = snakeBody.length - 1; i > 0; i--) {
        snakeBody[i] = snakeBody[i - 1];
    }

    snakeBody[0] = [snakeX, snakeY];

    if (snakeX === foodX && snakeY === foodY) {
        updateFoodPosition();
        snakeBody.push([foodX, foodY]);
        score++;
        highScore = score >= highScore ? score : highScore;
        localStorage.setItem("high-score", highScore);
        scoreElement.innerText = `Score: ${score}`;
        highScoreElement.innerText = `High Score: ${highScore}`;
    }

    for (let i = 1; i < snakeBody.length; i++) {
        if (snakeX === snakeBody[i][0] && snakeY === snakeBody[i][1]) {
            failReason = "self";
            return gameOver = true;
        }
    }

    movements.push({
        x: snakeX,
        y: snakeY,
        direction: lastDirection,
        time: new Date().toISOString()
    });

    html += `<div class="food" style="grid-area: ${foodY + 1} / ${foodX + 1}"></div>`;

    for (let i = 0; i < snakeBody.length; i++) {
        html += `<div class="head" style="grid-area: ${snakeBody[i][1] + 1} / ${snakeBody[i][0] + 1}"></div>`;
    }

    board.innerHTML = html;
};

updateFoodPosition();
setIntervalId = setInterval(initGame, 125);
document.addEventListener("keydown", changeDirection);

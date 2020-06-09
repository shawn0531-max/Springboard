const gameContainer = document.getElementById("game");
let card1 = null;
let card2 = null;
let flipped = 0;
let clickable = false;
let turnCount = 0;
let highScore = JSON.parse(localStorage.getItem("bestScore"));
let score = 0;

if (highScore>0){
  let highscoreText = document.querySelector('#highScoreText');
  highScoreText.innerText = highScore;
}

const colors = ["red","blue","green","red","blue","green",];

function shuffle(array) {
  let counter = array.length;
  while (counter > 0) {
    let index = Math.floor(Math.random() * counter);
    counter--;
    let temp = array[counter];
    array[counter] = array[index];
    array[index] = temp;
  }
  return array;
}

let shuffledColors = shuffle(colors);

function makeDivs(colorArray) {
  for (let color of colorArray) {
    const newDiv = document.createElement("div");
    newDiv.classList.add(color);
    newDiv.classList.add('card');
    newDiv.addEventListener("click", cardClick);
    gameContainer.append(newDiv);
  }
}

function cardClick(e) {
  if (clickable){return};
  if (e.target.classList.contains("flipped")){return};

  console.log("you just clicked", e.target);
  
  const turn = document.querySelector('#turnCounter');
  

  let currentCard = e.target;
  currentCard.style.backgroundColor = currentCard.classList[0];
  
  if (card1 === null || card2 === null){
      currentCard.classList.add("flipped");
      turnCount += 0.5;
      let roundTurn = Math.floor(turnCount);
      turn.innerText = roundTurn;
      card1 = card1 || currentCard;
      if(card1 === currentCard){
          card2 = null;
      } else {
          card2 = currentCard;
      }
  }

  if (card1 && card2){
      clickable = true;
      let colorCard1 = card1.style.backgroundColor;
      let colorCard2 = card2.style.backgroundColor;
      if(colorCard1 === colorCard2){
          card1.removeEventListener('click', cardClick);
          card2.removeEventListener('click', cardClick);
          flipped += 2;
          card1 = null;
          card2 = null;
          clickable = false;
          score += 50;
          let scoreText = document.querySelector('#score');
          scoreText.innerText = score;
      } else {
          setTimeout(function(e){
              card1.style.backgroundColor = "";
              card2.style.backgroundColor = "";
              card1.classList.remove("flipped");
              card2.classList.remove("flipped");
              card1 = null;
              card2 = null;
              clickable = false;
              score -= 10;
              let scoreText = document.querySelector('#score');
              scoreText.innerText = score;
          }, 1000);
      }
  }

  let scoreText = document.querySelector('#score');
  scoreText.innerText = score;
   
  if(flipped === colors.length){
      if (score>highScore){
        localStorage.setItem("bestScore",JSON.stringify(score));
      }
      console.log(score);
      let reset = document.querySelector('#resetBtn');
      reset.style.visibility = "visible";
      reset.addEventListener('click',function(e){
      location.reload();
    })
      const header = document.querySelector('#memoryHead');
      startBtn.style.transition = '0s';
      startBtn.style.visibility = "hidden";
      header.style.visibility = "hidden";
      let startDiv = document.querySelector('#startDiv');
      startDiv.style.visibility = "hidden";
      let gameDiv = document.querySelector('#game');
      gameDiv.style.visibility = "hidden";
      let card = document.querySelectorAll('.card');
      for (i=0; i < card.length; i++){
      let cardNum = card[i];
      cardNum.style.visibility = "hidden";
      }
      if (reset.style.visibility === "visible"){
        alert("You Win!")
      }
  };
}

makeDivs(shuffledColors);

const startBtn = document.querySelector('#startBtn');

setInterval(function(e){
  startBtn.classList.toggle('startBtnSmall');
  startBtn.classList.toggle('startBtnBig');
}, 800);

startBtn.addEventListener('click', function(e){
  const header = document.querySelector('#memoryHead');
  startBtn.style.transition = '0s';
  startBtn.style.visibility = "hidden";
  header.classList.replace('memoryHeadStart', 'memoryHeadPlay');
  let startDiv = document.querySelector('#startDiv');
  startDiv.style.visibility = "hidden";
  let gameDiv = document.querySelector('#game');
  gameDiv.style.visibility = "visible";
  let card = document.querySelectorAll('.card');
  for (i=0; i < card.length; i++){
    let cardNum = card[i];
    cardNum.style.visibility = "visible";
  }
  
  let turnLabel = document.querySelector('#turnLabel');
  turnLabel.style.visibility = "visible";
  let turnCounter = document.querySelector('#turnCounter');
  turnCounter.style.visibility = "visible";
  let scoreLabel = document.querySelector('#scoreLabel');
  scoreLabel.style.visibility = "visible";
  let scoreText = document.querySelector('#score');
  scoreText.style.visibility = "visible";
  let highScoreLabel = document.querySelector('#highScoreLabel');
  highScoreLabel.style.visibility = "visible";
  let highscoreText = document.querySelector('#highScoreText');
  highScoreText.style.visibility = "visible";
});

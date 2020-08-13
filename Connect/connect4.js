/** Connect Four
 *
 * Player 1 and 2 alternate turns. On each turn, a piece is dropped down a
 * column until a player gets four-in-a-row (horiz, vert, or diag) or until
 * board fills (tie)
 */

const WIDTH = 7;
const HEIGHT = 6;

let currPlayer = 1; // active player: 1 or 2
let board = []; // array of rows, each row is array of cells  (board[y][x])

/** makeBoard: create in-JS board structure:
 *    board = array of rows, each row is array of cells  (board[y][x])
 */

function makeBoard() {
  // TODO: set "board" to empty HEIGHT x WIDTH matrix array
  for (let y = 0; y < HEIGHT; y++) {
    board.push(Array.from({ length: WIDTH }));
  }
}

/** makeHtmlBoard: make HTML table and row of column tops. */

function makeHtmlBoard() {
  // TODO: get "htmlBoard" variable from the item in HTML w/ID of "board"
  let htmlBoard = document.querySelector('#board');
  // TODO: add comment for this code
  // creating 'insert piece' row of table, setting id of top tr to "column-top", adding click event listener to the row
  let top = document.createElement("tr");
  top.setAttribute("id", "column-top");
  top.addEventListener("click", handleClick);

// adding td's to 'insert piece' row
  for (let x = 0; x < WIDTH; x++) {
    const headCell = document.createElement("td");
    headCell.setAttribute("id", x);
    top.append(headCell);
  }
  // add completed row above actual board
  htmlBoard.append(top);

  // TODO: add comment for this code
  // creating actual game board and assigning unique y-x id to each td element
  for (let y = 0; y < HEIGHT; y++) {
    const row = document.createElement("tr");
    for (var x = 0; x < WIDTH; x++) {
      const cell = document.createElement("td");
      cell.setAttribute("id", `${y}-${x}`);
      row.append(cell); 
    }
    htmlBoard.append(row);
  }
}

/** findSpotForCol: given column x, return top empty y (null if filled) */

function findSpotForCol(x) {
  // TODO: write the real version of this, rather than always returning 0
  for (y = HEIGHT - 1; y >= 0; y--){
    if (!board[y][x]){
      return y;
    }
  }
  return null;
}

/** placeInTable: update DOM to place piece into HTML table of board */

function placeInTable(y, x) {
  // TODO: make a div and insert into correct table cell
  let pieceDiv = document.createElement('div');
  pieceDiv.classList.add('piece', `player${currPlayer}`);
  if (y === 0){pieceDiv.classList.add(`y0`)}
  if (y === 1){pieceDiv.classList.add(`y1`)}
  if (y === 2){pieceDiv.classList.add(`y2`)}
  if (y === 3){pieceDiv.classList.add(`y3`)}
  if (y === 4){pieceDiv.classList.add(`y4`)}
  if (y === 5){pieceDiv.classList.add(`y5`)}
  const piece = document.getElementById(`${y}-${x}`);
  piece.append(pieceDiv);
}

/** endGame: announce game end */

function endGame(msg) {
  // TODO: pop up alert message
  alert(msg);
}

/** handleClick: handle click of column top to play piece */

function handleClick(evt) {
  // get x from ID of clicked cell
  let x = +evt.target.id;

  // get next spot in column (if none, ignore click)
  let y = findSpotForCol(x);
  if (y === null) {
    return;
  }

  // place piece in board and add to HTML table
  // TODO: add line to update in-memory board
  placeInTable(y, x);
  board[y][x] = currPlayer;

  // check for win
  if (checkForWin()) {
    return endGame(`Player ${currPlayer} won!`);
  }

  // check for tie
  // TODO: check if all cells in board are filled; if so call, call endGame
  if (checkTie()) {
    return endGame('Both players are so good that it is a tie!');
  }

  // switch players
  // TODO: switch currPlayer 1 <-> 2
  currPlayer = (currPlayer === 1) ? 2 : 1;
}

/** checkForWin: check board cell-by-cell for "does a win start here?" */

function checkForWin() {
  function _win(cells) {
    // Check four cells to see if they're all color of current player
    //  - cells: list of four (y, x) cells
    //  - returns true if all are legal coordinates & all match currPlayer

    return cells.every(
      ([y, x]) =>
        y >= 0 &&
        y < HEIGHT &&
        x >= 0 &&
        x < WIDTH &&
        board[y][x] === currPlayer
    );
  }

  // TODO: read and understand this code. Add comments to help you.
// looping through spots to see if occupied on board to check for each win case (vertical, horizontal, diagonal L, diagonal R)
  for (let y = 0; y < HEIGHT; y++) {
    for (let x = 0; x < WIDTH; x++) {
      const horiz = [[y, x], [y, x + 1], [y, x + 2], [y, x + 3]];
      const vert = [[y, x], [y + 1, x], [y + 2, x], [y + 3, x]];
      const diagDR = [[y, x], [y + 1, x + 1], [y + 2, x + 2], [y + 3, x + 3]];
      const diagDL = [[y, x], [y + 1, x - 1], [y + 2, x - 2], [y + 3, x - 3]];

      if (_win(horiz) || _win(vert) || _win(diagDR) || _win(diagDL)) {
        return true;
      }
    }
  }
}

function checkTie(){
  // let count = 0;
  // for (let x = 0; x < WIDTH; x++){
  //   let td = document.getElementById(`0-${x}`);
  //   if (td === 1 || td === 2){
  //     count++;
  //   }
  //   return count;
  // }
  // if (count === WIDTH){
  //   return true;
  // }
  if (board.every(row => row.every(cell => cell))) {
    return true;
  }
}


makeBoard();
makeHtmlBoard();
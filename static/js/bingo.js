window.onload = function() {
    var table = document.getElementById("bingoTable");
    var reloadLink = document.getElementById("reloadLink");

    var number=76;
    var used = new Array(76);
    var digit1 = 0;
    var digit2 = 0;

    // Set up click listener for reload link
    reloadLink.addEventListener("click", function(event) {
        event.preventDefault();
        resetBoard(table);
        generateNumbers(table);
    });

    // Generate initial board
    generateNumbers(table);
};

function generateNumbers(table) {
    // Set up variables for tracking generated numbers and used squares
    var numbers = [];
    var usedSquares = {};

    // Generate random numbers and populate board
    for (var i = 1; i <= 75; i++) {
        numbers.push(i);
    }

    for (var row = 0; row < 5; row++) {
        var tr = table.insertRow(row);

        for (var col = 0; col < 5; col++) {
            var td = tr.insertCell(col);

            // Generate random index within remaining numbers
            var index = Math.floor(Math.random() * (numbers.length - 1));

            // Get number from array and remove it
            var number = numbers.splice(index, 1)[0];

            // Set square text and class
            td.innerHTML = number;
            td.className = "square";

            // Store number in used squares object
            usedSquares[number] = true;

            // Add click listener to toggle square class
            td.addEventListener("click", function() {
                if (this.className === "square") {
                    this.className = "square picked";
                } else {
                    this.className = "square";
                }
            });
        }
    }

    // Set "Free" square
    var freeSquare = table.rows[2].cells[2];
    freeSquare.innerHTML = "Free";
    freeSquare.className = "square free";

    // Store used squares in table data attribute
    table.dataset.usedSquares = JSON.stringify(usedSquares);
}

function resetBoard(table) {
    // Remove existing rows from table
    while (table.rows.length > 0) {
        table.deleteRow(0);
    }
}


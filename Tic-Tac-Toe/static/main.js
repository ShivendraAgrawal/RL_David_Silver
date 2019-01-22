/**
 * Created by shivendra on 15/01/19.
 */

$("#start").click(function(e) {
    e.preventDefault();
    console.log("Start clicked");

    $.ajax({
        type: "POST",
        url: "http://0.0.0.0:5000/play_one_round",
        data: {
            button_id: this.id
        },
        success: function(result) {
            console.log(result);
        },
        error: function(result) {
            console.log("Something went wrong");
        }
    });
});

$("button[name=grid]").click(function(e) {
    e.preventDefault();
    var gridText;
    var buttonID = this.id;

    $.ajax({
        type: "POST",
        url: "http://0.0.0.0:5000/play_one_round",
        data: {
           button_id: buttonID
         },
        success: function(result) {
            console.log(result);

            if(result.player === 1){
                gridText = 'X';
                $("#message").html("Player 2's turn");
            }
            else {
                gridText = 'O';
                $("#message").html("Player 1's turn");
            }

            $("#" + buttonID).html(gridText);

            if(result.solved) {
                if (result.player === 1){
                    console.log(result.player + " won!!");
                    $("#message").html("Player " + result.player + " won!!")
                }
                else {
                    $("#message").html("Game draw!!")
                }
            }

        },
        error: function(result) {
            console.log("Something went wrong");
        }
    });
});
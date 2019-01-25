/**
 * Created by shivendra on 15/01/19.
 */

var game_mode;
var start_position;

$("#start").click(function(e) {
    e.preventDefault();
    console.log("Start clicked");

    game_mode = $("input[name='game_mode']:checked").val();
    start_position = $("input[name='start_position']:checked").val();

    if (start_position == "player2" && game_mode == "human_computer"){
        $.ajax({
            type: "GET",
            url: "http://0.0.0.0:5000/random_player_first_round_as_player_1",
            success: function(result) {
                console.log(result);
                $("#" + result.buttonID).html("X");
            },
            error: function(result) {
                console.log("Something went wrong");
            }
        });
    }

    // $.ajax({
    //     type: "POST",
    //     url: "http://0.0.0.0:5000/play_one_round",
    //     data: {
    //         button_id: this.id
    //     },
    //     success: function(result) {
    //         console.log(result);
    //     },
    //     error: function(result) {
    //         console.log("Something went wrong");
    //     }
    // });
});

$("button[name=grid]").click(function(e) {
    e.preventDefault();
    var gridText;
    var buttonID = this.id;
    var computer_buttonID;

    if (game_mode == "human_human") {
        $.ajax({
            type: "POST",
            url: "http://0.0.0.0:5000/play_one_round",
            data: {
                button_id: buttonID
            },
            success: function (result) {
                console.log(result);

                if (result.player === 1) {
                    gridText = 'X';
                    $("#message").html("Player 2's turn");
                }
                else {
                    gridText = 'O';
                    $("#message").html("Player 1's turn");
                }

                $("#" + buttonID).html(gridText);

                if (result.solved) {
                    if (result.player != 0) {
                        console.log(result.player + " won!!");
                        $("#message").html("Player " + result.player + " won!!")
                    }
                    else {
                        $("#message").html("Game draw!!")
                    }
                }

            },
            error: function (result) {
                console.log("Something went wrong");
            }
        });
    }
    else {
        $.ajax({
            type: "POST",
            url: "http://0.0.0.0:5000/random_player",
            data: {
                button_id: buttonID
            },
            success: function (result) {
                console.log(result);
                computer_buttonID = result.buttonID;

                if (result.player === 1) {
                    gridText = 'X';
                    $("#message").html("Player 2's turn");
                    $("#" + buttonID).html(gridText);
                    $("#" + computer_buttonID).html('O');

                }
                else {
                    gridText = 'O';
                    $("#message").html("Player 1's turn");
                    $("#" + buttonID).html(gridText);
                    $("#" + computer_buttonID).html('X');
                }


                if (result.solved) {
                    if (result.player != 0) {
                        console.log(result.player + " won!!");
                        $("#message").html("Player " + result.player + " won!!")
                    }
                    else {
                        $("#message").html("Game draw!!")
                    }
                }

            },
            error: function (result) {
                console.log("Something went wrong");
            }
        });
    }
});
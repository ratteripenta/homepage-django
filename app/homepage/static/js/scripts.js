$(document).ready(function() {
    
    var menu = "closed"
    $("#menu").click(function(){
        if (menu === "closed") {
            $(".navbar-items").addClass("show")
            menu = "opened"            
        } else {
            $(".navbar-items").removeClass("show")
            menu = "closed"
        }
        console.log("Menu clicked, state =",menu)
    })

})
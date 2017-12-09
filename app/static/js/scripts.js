$(document).ready(function() {
    
    var menu = "closed"
    $("#menu").click(function(){
        if (menu === "closed") {
            $(".navbar-items").css("transform", "translate(0, 0)")
            $(".navbar-items").css("display","flex")
            menu = "opened"            
        } else {
            $(".navbar-items").css("transform", "translate(100%, 0)")
            $(".navbar-items").css("display","none")
            menu = "closed"
        }
        console.log("Menu clicked, state =",menu)
    })

})
// function danger()
// {
//     document.querySelectorAll(".btn").addEventListener("click",function()
// {
//     var audio = new Audio("images/tom-7.mp3");
//     audio.play();
// });
// }
document.querySelector(".img1").classList.add("imgf");
var random1=Math.floor(Math.random()*6)+1;

var randomImg1="/static/images/dice" + random1 + ".png";
document.addEventListener("keypress",function(event)
{
    // buttonAnimation();
    nice(event.key);
});
var flag=1;
function nice(key)
{
    switch(key)
    {
        case "1":
            change1();
            flag=0
            break;
        case "2":
            if(flag==0){
                change2();
            }
            break;
        default:
            alert(key + " is PrESSED!!!");
            alert("Enter 1 for player1 :::: Enter 2 for player2!!!!!");
            break;
    }
}

function change1()
{
    flag = 0;
    document.querySelectorAll("img")[0].setAttribute("src",randomImg1);
    
    
    document.querySelector("#dis").removeAttribute("disabled");
    document.querySelector(".img2").classList.add("imgf");
    document.querySelector(".img1").classList.remove("imgf");
    
}


var random2=Math.floor(Math.random()*6)+1;

var randomImg2="/static/images/dice" + random2 + ".png";
function change2()
{
    document.querySelectorAll("img")[1].setAttribute("src",randomImg2);
    result();
}
var r;
var x;
var y;
function result()
{
    var email = document.querySelector(".gpt").textContent;
    var data = JSON.parse(email);
    var a = 0;
    if(random1>random2){
        a = 4;
        x=document.querySelector(".img1").classList.add("imgf");
        r=document.querySelector("h1").textContent="Player1 Wins!!!";
        y=document.querySelector(".img2").classList.remove("imgf");
        

    }
    else if(random2>random1)
    {
        a = 5;
        r=document.querySelector("h1").textContent="Player2 Wins!!!";
    }
    else{
        a = 6;
        r=document.querySelector("h1").textContent="DRAW!!!";
        y=document.querySelector(".img2").remove("imgf");
        x=document.querySelector(".img1").remove("imgf");
    }
    var transfer = {
    "id": a,
    "email": data
    }
      fetch('/update', {
      method: 'POST',
      body: JSON.stringify(transfer),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
      console.log(data); // handle the data returned by flask
    })


    setTimeout(()=> {
        window.location.reload(true);
    },2500)
    
    // document.querySelector(".result").style.backgroundColor="pink";

}

// function buttonAnimation()
// {
//     document.querySelectorAll("btn")[0].classList.add("pressed");
// }
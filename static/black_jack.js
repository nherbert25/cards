//test

//let q = new Date();
//alert("Today's date is " + q);

//let e = new Date();
//document.body.innerHTML = "<h1>Today's date is " + d + "</h1>"

// https://www.youtube.com/watch?v=4K33w-0-p2c   good video on xml http requests
// https://www.youtube.com/watch?v=23hrM4saaMk    rebuilding the last video with the fetch api instead (it's more modern)
//    look up async/await. I *think* they're built on top of promises. They're a wrapper that makes the code more readable, yet under the hood they're still promises.
// from my 1 second google, you still write your promise, then your other function will be defined as an async function by adding it as a keyword
// in the definition, aka: "async function myFunction() { ...my code ..  await myPromise() ... my code ..  }"

var dealer_sum = 0;
var your_sum = 0;

var dealer_ace_count = 0;
var your_ace_count = 0;


var hidden;
var deck;


var can_hit = true;  //allows the player to draw while your_sum <= 21




//
//
//let response = await fetch('static/testing.json');
//
//if (response.ok) { // if HTTP-status is 200-299
//  // get the response body (the method explained below)
//  let json = await response.json();
//} else {
//  alert("HTTP-Error: " + response.status);
//}



//
//
//
/////////////////////////////////////////////////////////////////////////////
//window.onload = function() {
//    build_deck();
//}
//
//function build_deck{
//    let values = ["A", "2", "3", "4"];
//    let types = ["C", "D", "H", "S"];
//    deck = [];
//
//    for (let i = 0; i < types.length; i++) {
//        let j = Math.floor(Math.random())
//
//}

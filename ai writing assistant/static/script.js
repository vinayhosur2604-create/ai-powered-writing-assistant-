const textArea = document.getElementById("inputText");

if(textArea){

textArea.addEventListener("input",()=>{

let text=textArea.value;

let words=text.trim().split(/\s+/).filter(word=>word.length>0).length;

let chars=text.length;

let reading=Math.ceil(words/200);

document.getElementById("words").innerText=
"Words: "+words;

document.getElementById("chars").innerText=
"Characters: "+chars;

document.getElementById("read").innerText=
"Reading Time: "+reading+" min";

});

}

function toggleMode(){

document.body.classList.toggle("dark");

}
async function checkGrammar(){

let text =
document.getElementById("inputText").value;

let response = await fetch("/check",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
text:text
})

});

let data = await response.json();

document.getElementById("output").innerText =
data.result;

}
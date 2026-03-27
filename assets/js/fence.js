
(function(){
let currency="GBP";
const map={GBP:"£",USD:"$",EUR:"€"};

document.querySelectorAll(".currency-pill").forEach(b=>{
b.onclick=()=>{currency=b.dataset.currency;document.querySelectorAll(".currency-pill").forEach(x=>x.classList.remove("is-active"));b.classList.add("is-active");};
});

function m(v){return map[currency]+v.toFixed(2);}

document.getElementById("fence-form").addEventListener("submit",e=>{
e.preventDefault();

let length=+document.getElementById("length").value||0;
let panel=+document.getElementById("panel").value||1;
let waste=+document.getElementById("waste").value/100||0;
let panels=Math.ceil((length/panel)*(1+waste));
let posts=panels+1;

let panelCost=panels*(+document.getElementById("panel-price").value||0);
let postCost=posts*(+document.getElementById("post-price").value||0);

let concVol=posts*(+document.getElementById("concrete").value||0);
let concCost=concVol*(+document.getElementById("concrete-price").value||0);

let total=panelCost+postCost+concCost;

document.querySelector(".result-main").innerText=panels+" panels";
document.querySelector(".result-sub").innerText="Includes posts + concrete";

document.getElementById("result-breakdown").innerHTML=`
<div>Panels: ${panels}</div>
<div>Posts: ${posts}</div>
<div>Concrete: ${concVol.toFixed(2)} m³</div>
<div>Panel cost: ${m(panelCost)}</div>
<div>Post cost: ${m(postCost)}</div>
<div>Concrete cost: ${m(concCost)}</div>
<div><strong>Total: ${m(total)}</strong></div>
`;
});
})();

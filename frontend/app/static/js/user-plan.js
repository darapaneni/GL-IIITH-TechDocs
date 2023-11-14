const toggler = document.querySelector(".plan-switch");
const PremiumPrice = document.getElementById("Price");

toggler.addEventListener("change", () => {
	if (toggler.checked) {
		PremiumPrice.innerHTML = `<span class="rupee">&#8377</span><span class="amount">1999 /</span><span class="type">yr</span>`;
	} else {
		PremiumPrice.innerHTML = `<span class="rupee">&#8377</span><span class="amount">199 /</span><span class="type">mo</span>`;
	}
});

// const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
// const tooltipList = [...tooltipTriggerList].map(tooltipTriggerE1 => new bootstrap.Tooltip(tooltipTriggerE1))

window.onload = function(){
	localStorage.setItem("Plan-Price", "₹199");
	localStorage.setItem("Plan-type", "Premium Monthly Subscription");
  };

toggler.addEventListener("change", () => {
	if (toggler.checked) {
		localStorage.setItem("Plan-Price", "₹1999");
		localStorage.setItem("Plan-type", "Premium Yearly Subscription");
	} else {
		localStorage.setItem("Plan-Price", "₹199");
		localStorage.setItem("Plan-type", "Premium Monthly Subscription");
	}
});



/*



document.querySelector("#compare-button-text").addEventListener("click",function(){
    document.querySelector(".mfPricingComparison").classList.add("active");
});

document.querySelector("#compare-button-text-1").addEventListener("click",function(){
    document.querySelector(".mfPricingComparison").classList.remove("active");
});
*/

window.onload = function(){
	document.getElementById("ComparePlans").style.display='none';
  };

let btn = document.querySelector("#compare-button");
let div = document.querySelector("#ComparePlans");
const btntext = document.getElementById("compare-button-text");

btn.addEventListener("click", () =>{
	if(div.style.display === "none"){
		div.style.display = "block";
		btntext.innerHTML = "Hide Compare Plans";
		// `Hide Compare Plans`
	}else {
		div.style.display = "none";
		btntext.innerHTML = "Show Compare Plans";
	}
});

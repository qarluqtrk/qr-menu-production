/*========================
 Manifest js
 ==========================*/
// window.onload = () => {
//   "use strict";
//   if ("serviceWorker" in navigator) {
//     navigator.serviceWorker.register("sw.js");
//   }
// };


document.addEventListener('DOMContentLoaded', function () {
    // Get all elements with class "price"
    var priceElements = document.getElementsByClassName('price-number');

    // Loop through each element and reformat the price
    for (var i = 0; i < priceElements.length; i++) {
        var price = parseFloat(priceElements[i].textContent.replace(/\s/g, ' ')); // Remove existing spaces
        priceElements[i].textContent = formatPrice(price);
    }

    // Function to format the price with thousands separator
    function formatPrice(price) {
        return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');// Use browser's built-in toLocaleString for formatting
    }
});

/*======================
Get cookies
 */

function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Check if the cookie starts with the provided name
        if (cookie.startsWith(name + '=')) {
            // Return the value of the cookie
            return cookie.substring(name.length + 1);
        }
    }
    // Return null if the cookie is not found
    return null;
}

/*=====================
    wishlist added start
==========================*/
const divs = document.querySelectorAll(".like-btn");
divs.forEach((el) =>
    el.addEventListener("click", (event) => {
        event.target.parentNode.classList.toggle("animate");
        event.target.parentNode.classList.toggle("active");
        event.target.parentNode.classList.toggle("inactive");
    })
);

/*====================
 Ratio js
=======================*/
window.addEventListener("load", () => {
    const bgImg = document.querySelectorAll(".bg-img");
    for (i = 0; i < bgImg.length; i++) {
        let bgImgEl = bgImg[i];

        if (bgImgEl.classList.contains("bg-top")) {
            bgImgEl.parentNode.classList.add("b-top");
        } else if (bgImgEl.classList.contains("bg-bottom")) {
            bgImgEl.parentNode.classList.add("b-bottom");
        } else if (bgImgEl.classList.contains("bg-center")) {
            bgImgEl.parentNode.classList.add("b-center");
        } else if (bgImgEl.classList.contains("bg-left")) {
            bgImgEl.parentNode.classList.add("b-left");
        } else if (bgImgEl.classList.contains("bg-right")) {
            bgImgEl.parentNode.classList.add("b-right");
        }

        if (bgImgEl.classList.contains("blur-up")) {
            bgImgEl.parentNode.classList.add("blur-up", "lazyload");
        }

        if (bgImgEl.classList.contains("bg_size_content")) {
            bgImgEl.parentNode.classList.add("b_size_content");
        }

        bgImgEl.parentNode.classList.add("bg-size");
        const bgSrc = bgImgEl.src;
        bgImgEl.style.display = "none";
        bgImgEl.parentNode.setAttribute(
            "style",
            `
      background-image: url(${bgSrc});
      background-size:cover;
      background-position: center;
      background-repeat: no-repeat;
      display: block;
      `
        );
    }
});

/*====================
 Range js
=======================*/
const rangeInputs = document.querySelectorAll('input[type="range"]');
const numberInput = document.querySelector('input[type="number"]');

function handleInputChange(e) {
    let target = e.target;
    if (e.target.type !== "range") {
        target = document.getElementById("range");
    }
    const min = target.min;
    const max = target.max;
    const val = target.value;

    target.style.backgroundSize = ((val - min) * 100) / (max - min) + "%100%";
}

rangeInputs.forEach((input) => {
    input.addEventListener("input", handleInputChange);
});


/*====================
  RTL js
======================*/
const dirSwitch = document.querySelector("#dir-switch");
const htmlDom = document.querySelector("html");
const rtlLink = document.querySelector("#rtl-link");
const initialCheck = localStorage.getItem("dir");
if (dirSwitch) {
    if (initialCheck === "rtl") dirSwitch.checked = true;
}
dirSwitch?.addEventListener("change", (e) => {
    const checkbox = e.target;
    console.log(checkbox.checked);
    if (checkbox.checked) {
        htmlDom.setAttribute("dir", "rtl");
        rtlLink.href = "/static/assets/css/vendors/bootstrap.rtl.min.css";
        localStorage.setItem("rtlcss", "/static/assets/css/vendors/bootstrap.rtl.min.css");
        localStorage.setItem("dir", "rtl");
    }

    if (!checkbox.checked) {
        htmlDom.setAttribute("dir", "ltr");
        rtlLink.href = "/static/assets/css/vendors/bootstrap.min.css";
        localStorage.setItem("rtlcss", "/static/assets/css/vendors/bootstrap.min.css");
        localStorage.setItem("dir", "ltr");
    }
});
// Rtl
htmlDom.setAttribute("dir", localStorage.getItem("dir") ? localStorage.getItem("dir") : "ltr");
rtlLink.href = localStorage.getItem("rtlcss") ? localStorage.getItem("rtlcss") : "/static/assets/css/vendors/bootstrap.min.css";

/*====================
  Dark js
======================*/
const darkSwitch = document.querySelector("#dark-switch");
const bodyDom = document.querySelector("body");
const initialDarkCheck = localStorage.getItem("layout_version");
if (darkSwitch) {
    if (initialDarkCheck === "dark") darkSwitch.checked = true;
}
darkSwitch?.addEventListener("change", (e) => {
    const checkbox = e.target;
    if (checkbox.checked) {
        bodyDom.classList.add("dark");
        localStorage.setItem("layout_version", "dark");
    }

    if (!checkbox.checked) {
        bodyDom.classList.remove("dark");
        localStorage.removeItem("layout_version");
    }
});

if (localStorage.getItem("layout_version") == "dark") {
    bodyDom.classList.add("dark");
}

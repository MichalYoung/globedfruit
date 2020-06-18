// vtranslate: 
//   Demonstration of modifying element visibility 
//   by handling key clicks in javascript. 
// 
function toggle_translation(event) {
    console.log("Click noted");
    // The 'this' object is set automatically in event handlers
    this.classList.toggle("translated");
    var sib = this.nextElementSibling;
    // The very next element should be the english translation,
    // but we'll search for it just in case. 
    while (sib) {
        console.log("Checking " + sib);
        css_classes = sib.classList;
        if (css_classes.contains("en")) {
            css_classes.toggle("hide");
            console.log("Toggled!");
            return;
        }
        sib = sib.nextElementSibling;
    }
    alert("Didn't find translation");
    return;
}


document.addEventListener("DOMContentLoaded", function() {  
    let es_elements = document.querySelectorAll(".es");
    for (let i=0; i < es_elements.length; ++i) {
	es_elements[i].addEventListener('click', toggle_translation);
    }
});

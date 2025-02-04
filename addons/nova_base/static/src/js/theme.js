$(document).ready(function(){

    console.log("=============================NOVA BASE ============================");
});

// var MyClass = instance.web.Class.extend({
//     say_hello: function() {
//         console.log("hello");
//     },
// });
$('span.contact_up').replaceWith($('span.contact_up').text().replaceAll(',',',</span><span>'))

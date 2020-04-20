$('.collapse').on('shown.bs.collapse', function (e) {
   console.log("Opened")
});

$('.collapse').on('hidden.bs.collapse', function (e) {
   console.log("Closed")
});
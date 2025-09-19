document.addEventListener('DOMContentLoaded',()=>{
    var selectItems = document.querySelectorAll('select');
    if(selectItems.length>0){
        M.FormSelect.init(selectItems);
    }

    var dateEl = document.getElementById('id_start_date');
    if(dateEl) {
            M.Datepicker.init(dateEl, {
            format: 'yyyy-mm-dd',
            autoClose: true
  })};

  var dateE2 = document.getElementById('id_end_date');
  if(dateE2)M.Datepicker.init(dateE2, {
    format: 'yyyy-mm-dd',
    autoClose: true
  });
 
});
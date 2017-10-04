tinymce.init({
  selector: 'textarea',
  height: 300,
  menubar: false,
  plugins: [
    'advlist autolink lists link image charmap print preview anchor textcolor',
    'searchreplace visualblocks code fullscreen',
    'insertdatetime media table contextmenu paste code help'
  ],
  toolbar: 'insert | undo redo |  styleselect | bold italic backcolor  | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | help',
  file_browser_callback: function(field_name, url, type, win) {
    win.document.getElementById(field_name).value = 'my browser value';
  }
  // content_css: [
  //   '//fonts.googleapis.com/css?family=Lato:300,300i,400,400i',
  //   '//www.tinymce.com/css/codepen.min.css']
});
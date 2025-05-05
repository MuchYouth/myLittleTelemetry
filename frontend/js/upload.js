document.addEventListener("DOMContentLoaded", function () {
  var fileInput = document.getElementById("ymlFileInput");
  var form = document.getElementById("uploadForm");

  fileInput.addEventListener("change", function () {
    if (fileInput.files.length) {
      form.submit();
    }
  });
});

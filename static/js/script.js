const modal = document.querySelector(".drag_drop_modal_bg");
const open_modal_button = document.querySelector("#document_button1");
const modal_cross = document.querySelector(".close_button");
const html_body = document.querySelector("body");

const file_container = document.querySelector(".files_container");
modal_cross.addEventListener("click", () => {
  modal.style.display = "none";
  file_container.innerHTML = "";
});

open_modal_button.addEventListener("click", () => {
  modal.style.display = "flex";
  console.log(modal);
});

const upload_button = document.querySelector(".upload_button");
const receive_button = document.querySelector(".receive_button");
const upload_document2 = document.querySelector("#document_button2");

upload_document2.addEventListener("click", () => {
  modal.style.display = "flex";
});
const html_width = html_body.getBoundingClientRect().width;
if (html_width < 800) {
  window.addEventListener("scroll", () => {
    let y_scroll = window.pageYOffset;
    if (y_scroll >= 600) {
      receive_button.style.zIndex = "1";
      receive_button.style.opacity = "1";

      upload_button.style.zIndex = "-1";
      upload_button.style.opacity = "0";

      upload_document2.style.animation = `slideFromLeft 1s ease forwards`;
    } else {
      upload_button.style.zIndex = "1";
      upload_button.style.opacity = "1";

      receive_button.style.zIndex = "-1";
      receive_button.style.opacity = "0";

      upload_document2.style.animation = `none`;
    }
  });
}

let fixed_height = 750;

const body_width = document.querySelector("body").getBoundingClientRect().width;

if (body_width < 400) {
  fixed_height = 555;
  upload_button.textContent = "";
  receive_button.textContent = "";
  upload_button.innerHTML = `<img src="../static/images/upload_up_arrow.png" class ="up_arrow" alt="">`; //here
  receive_button.innerHTML = `<img src="../static/images/receive_down_arrow.png" class ="down_arrow" alt="">`; //here
  upload_document2.textContent = "";
  upload_document2.classList.remove("send_doc");
  upload_document2.classList.add("bg_transparent");
  upload_document2.innerHTML = `<img src="../static/images/upload_file.png" class="upload_file">`; //here
}

document.addEventListener("DOMContentLoaded", function () {
  var summernote1 = document.getElementById("summernote1");
  var summernote2 = document.getElementById("summernote2");

  if (summernote1) {
    $(summernote1).summernote({
      placeholder: "UPLOAD...",
      minHeight: fixed_height,
      maxHeight: fixed_height,
    });
  }

  if (summernote2) {
    $(summernote2).summernote({
      placeholder: "RECEIVE...",
      minHeight: fixed_height,
      maxHeight: fixed_height,
    });
  }
});

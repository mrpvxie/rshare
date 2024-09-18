const drop_here = document.querySelector(".drop_here");
const uploading_list = document.querySelector(".uploading_list");
const list_container = document.querySelector(".files_container");
const file_selector = document.querySelector(".browser_text");
const file_selector_input = document.querySelector("#browser_button");

file_selector.onclick = () => file_selector_input.click();

file_selector_input.onchange = () => {
  [...file_selector_input.files].forEach((file) => {
    if (check_file_validation(file.type)) {
      console.log(file);
      upload_file(file);
    }
  });
};

check_file_validation = (file_type) => {
  const file_format = file_type.split("/")[0];
  if (
    file_format == "image" ||
    file_format == "video" ||
    file_type == "application/pdf"
  ) {
    return true;
  }
};

drop_here.ondragover = (event) => event.preventDefault();

//here
drop_here.ondrop = (event) => {
  event.preventDefault();
  console.log([...event.dataTransfer.items]);
  if (event.dataTransfer.items) {
    [...event.dataTransfer.items].forEach((currentItem) => {
      if (currentItem.kind === "file") {
        const current_file = currentItem.getAsFile();
        if (check_file_validation(current_file.type)) {
          upload_file(current_file);
        }
      } else {
        [...event.dataTransfer.files].forEach((currentItem) => {
          if (check_file_validation(currentItem)) {
            upload_file(currentItem);
          }
        });
      }
    });
  }
};

let uploading_file_counter = 0;

upload_file = (file) => {
  uploading_file_counter++;
  uploading_list.style.display = "flex";
  let li_element = document.createElement("li");
  li_element.classList.add("file_info");
  li_element.classList.add("uploading");
  li_element.innerHTML += `
                        <div class="icon_container">
                            <img
                                src="${select_icon(file)}"
                                class="file_icon">
                        </div>
                        <div class="colmun">
                            <div class="file_name">
                                <div class="name">${file.name}</div>
                                <span>0%</span>
                            </div>
                            
                            <div class="file_size">${(
                              file.size /
                              (1024 * 1024)
                            ).toFixed(2)} MB</div>
                        </div>
                        <div class="right_cross">
                            <div class="right_emoji">✅</div>
                            <div class="cross_emoji">❌</div>
                        </div>
`;
  list_container.prepend(li_element);
  let http = new XMLHttpRequest();
  let data = new FormData();
  console.log(li_element);
  data.append("file", file);
  http.onload = () => {
    li_element.classList.add("uploaded");
    li_element.classList.remove("uploading");
  };
  http.upload.onprogress = (event) => {
    let percentage = (event.loaded / event.total) * 100;
    li_element.querySelector("span").innerHTML = Math.round(percentage) + "%";
  };

  http.open("POST", "/upload_file", true);
  http.send(data);
  li_element.querySelector(".cross_emoji").onclick = () => http.abort();
  http.onabort = () => li_element.remove();
};

select_icon = (file) => {
  const splitType =
    file.type.split("/")[0] == "application"
      ? "application"
      : file.type.split("/")[0];
  return "../static/images/" + splitType + ".png";
};

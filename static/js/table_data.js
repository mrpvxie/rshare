let content_data = [];

let count = 0;
let id = document.querySelectorAll(".table_id");
let content = document.querySelectorAll(".table_content");
let time = document.querySelectorAll(".table_time");

id.forEach(() => {
  content_data.push({
    id: id[count].textContent.trim(),
    content: content[count].textContent.trim(),
    time: time[count].textContent.trim(),
  });
  count++;
});

console.log(content_data);

function insert_data(data_array) {
  const table_row_data = document.querySelector(".table_body");
  const row_data = data_array
    .map((currentItem) => {
      return `
            <tr >
                  <div id="modal_no_{{ $${currentItem.id} }}" class="modal" style="display:none">
                      <div class="modal-content">
                          <span class="close">&times;</span>
                          <p>Are you sure you want to delete this item?</p>
                          <div class="modal-buttons">
                              <a href="{{url_for('delete_content', content_id= cont.id)}}" >
                                  <button class="btn-yes">Yes</button>
                              </a>
                              <button class="btn-no">No</button>
                          </div>
                      </div>
                  </div>
                <td data-label="id" class = "table_id"><span class ="content_text">{{ $${currentItem.id} }}</span></td>

                <td data-label="content" class="content_column table_content">
                    
                  <a href = "{{ url_for('full_content',content_id = cont.id) }}"><br><span class ="content_text">$${currentItem.content}</span></a>
                  
                </td>
                <td data-label="time" class="table_time" ><span class ="content_text">{{ $${currentItem.time} }}</span></td>

                <td id="deleteBtn{{ $${currentItem.id} }}" class= "table_delete">
                    <button class="btn_trash delete_button" data-label="modal_no_{{ $${currentItem.id} }}">
                        <i class="fa fa-trash"></i>
                    </button>
                </td>
            </tr>`;
    })
    .join(" ");
  table_row_data.innerHTML = row_data;
}

const search_input = document.querySelector(".search_input");

search_input.addEventListener("input", function () {
  const searchValue = search_input.value.toLowerCase().trim();
  if (searchValue === "") {
    insert_data(content_data);
    console.log("Showing all data");
  } else {
    const filtered_products = content_data.filter(function (currentItem) {
      return currentItem.content.toLowerCase().includes(searchValue);
    });
    if (filtered_products.length === 0) {
      insert_data([]);
      console.log("No results found");
    } else {
      insert_data(filtered_products);
    }

    console.log(filtered_products);
  }
});

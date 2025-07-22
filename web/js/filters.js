//FONCTION LIEES A PYTHON
eel.get_gmr();

eel.expose(display_gmr);
function display_gmr(li_GMR) {
  const div = document.getElementById("gmr_option");
  for (const element of li_GMR) {
    const p = document.createElement("p");
    p.className = "gmr";
    p.innerHTML = element;
    p.addEventListener("click", () => {
      update_search_bar_text("gmr_search_bar", p.innerHTML, gmr);
    });
    div.appendChild(p);
  }
  document.getElementById("container_indication").classList.add("hidden");
}

eel.expose(go_to);
function go_to(url) {
  window.location.replace(url);
}

const gmr = document.getElementsByClassName("gmr");

const update_selection_list_items = (list_gmr, input) => {
  input = input.toLowerCase();
  for (const element of list_gmr) {
    if (element.innerHTML.toLowerCase().includes(input)) {
      element.classList.remove("hidden");
    } else {
      element.classList.add("hidden");
    }
  }
};

const update_search_bar_text = (search_bar, val, list_gmr) => {
  document.getElementById(search_bar).value = val;
  update_selection_list_items(list_gmr, val);
};

document
  .getElementById("gmr_search_bar")
  .addEventListener("keyup", function () {
    const input = document.getElementById("gmr_search_bar").value;
    update_selection_list_items(gmr, input);
  });

document.getElementById("getfilters").onclick = () => {
  const form_data = {
    gmr: document.getElementById("gmr_search_bar").value,
    date_start: document.getElementById("date_start").value,
    date_end: document.getElementById("date_end").value,
  };

  if (form_data.date_start > form_data["date_end"]) {
    alert("Date de départ après date de fin");
    return;
  }

  const gmr_texts = [...gmr].map(element => element.innerHTML);

  if (!gmr_texts.includes(form_data.gmr)) {
    alert("Nom de GMR non reconnu");
    return;
  }

  document.getElementById("container_indication_end").classList.remove("hidden");
  eel.get_filters(form_data.gmr, form_data.date_start, form_data.date_end);
};

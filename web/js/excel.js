//FONCTIONS LIEES AU SCRIPT PYTHON
eel.expose(step);
function step(message) {
  document.getElementById("indication").innerHTML = message;
  document.getElementById("container_indication").classList.remove("hidden");
}

eel.expose(go_back);
function go_back(url) {
  window.location.replace(url);
}

eel.expose(add_og_to_selection);
function add_og_to_selection(li_og) {
  li_og.sort();
  console.log(li_og)
  const ul = document.getElementById("list_og");
  for (const element of li_og) {
    const div = document.createElement("div");
    const label = document.createElement("label");
    label.for = element;
    label.innerHTML = element;
    label.style.display = "flex";
    label.style.flexDirection = "row";
    const opt = document.createElement("input");
    opt.id = element;
    opt.type = "checkbox";
    opt.className = "og";
    opt.name = "og";
    opt.value = element;
    opt.onclick = () => {
      checkInteraction("og");
    };
    div.style.display = "flex";
    div.style.flexDirection = "row";
    div.style.alignItems = "center";
    div.appendChild(opt);
    div.appendChild(label);
    ul.appendChild(div);
  }
}

eel.expose(add_ni_to_selection);
function add_ni_to_selection(li_ni) {
  li_ni.sort()
  console.log(li_ni)
  const ul = document.getElementById("list_ni");
  for (const element of li_ni) {
    const div = document.createElement("div");
    const label = document.createElement("label");
    label.for = element;
    label.innerHTML = element;
    label.style.display = "flex";
    label.style.flexDirection = "row";
    const opt = document.createElement("input");
    opt.id = element;
    opt.type = "checkbox";
    opt.className = "ni";
    opt.name = "ni";
    opt.value = element;
    opt.onclick = () => {
      checkInteraction("ni");
    };
    div.style.display = "flex";
    div.style.flexDirection = "row";
    div.style.alignItems = "center";
    div.appendChild(opt);
    div.appendChild(label);
    ul.appendChild(div);
  }
}

eel.get_og();
eel.get_ni();

const ogList = document.getElementsByClassName("og");
const niList = document.getElementsByClassName("ni");

const checkAllCheckbox = (className) => {
  for (const element of className) {
    element.checked = true;
  }
};

const uncheckAllCheckbox = (className) => {
  for (const element of className) {
    element.checked = false;
  }
};

const checkInteraction = (type) => {
  checkedBoxes = document.querySelectorAll(
    `input[name=${type}]:checked`
  ).length;
  boxes = document.getElementsByClassName(type).length;
  selector = document.getElementById(`select_all_${type}`);
  selector.checked = checkedBoxes == boxes;
};

const update_selection_list_item = (li_items, input) => {
  input = input.toLowerCase();
  for (const liItem of li_items) {
    if (liItem.value.toLowerCase().includes(input)) {
      liItem.parentElement.classList.remove("hidden");
    } else {
      liItem.parentElement.classList.add("hidden");
    }
  }
};

document.getElementById("select_all_og").onclick = () => {
  selectAllInteraction("og", ogList);
};

document.getElementById("select_all_ni").onclick = () => {
  selectAllInteraction("ni", niList);
};

const selectAllInteraction = (classname, listType) => {
  if (document.getElementById(`select_all_${classname}`).checked == true) {
    checkAllCheckbox(listType);
  } else {
    uncheckAllCheckbox(listType);
  }
};

document.getElementById("radio_og").addEventListener("change", () => {
  if (!document.getElementById("radio_og").checked) {
    return;
  }
  document.getElementById("container_list_og").classList.remove("hidden");
  document.getElementById("container_list_ni").classList.add("hidden");
  document.getElementById("search_bar_ni").value = "";
  uncheckAllCheckbox(niList);
  document.getElementById("select_all_ni").checked = false;
  update_selection_list_item(niList, "");
});

document.getElementById("radio_ni").addEventListener("change", function () {
  if (!document.getElementById("radio_ni").checked) {
    return;
  }
  document.getElementById("container_list_ni").classList.remove("hidden");
  document.getElementById("container_list_og").classList.add("hidden");
  document.getElementById("search_bar_og").value = "";
  uncheckAllCheckbox(ogList);
  document.getElementById("select_all_og").checked = false;
  update_selection_list_item(ogList, "");
});

document.getElementById("search_bar_og").addEventListener("keyup", function () {
  const input = document.getElementById("search_bar_og").value;
  update_selection_list_item(ogList, input);
});

document.getElementById("search_bar_ni").addEventListener("keyup", function () {
  const input = document.getElementById("search_bar_ni").value;
  update_selection_list_item(niList, input);
});

document.getElementById("go_back").addEventListener("click", function () {
  eel.go_back();
});

document.getElementById("generate_excel").onclick = () => {
  checkedBoxesog = document.querySelectorAll("input[name=og]:checked");
  checkedBoxesni = document.querySelectorAll("input[name=ni]:checked");
  if (checkedBoxesog.length > checkedBoxesni.length) {
    for (const element of checkedBoxesog) {
      eel.generate_excel(element.value);
    }
  } else {
    for (const element of checkedBoxesni) {
      eel.generate_excel(element.value);
    }
  }
};

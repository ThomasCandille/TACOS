window.resizeTo(500, 300)

//CREATION DES FONCTIONS UTILISEES DANS PYTHON
eel.expose(go_to)
function go_to(url){window.location.replace(url)}

eel.expose(display_error)
function display_error(response_tuple){
  alert(`Error ${response_tuple[0]} - ${response_tuple[1]}`)
}
//FONCTION SUBMIT DU FORM
document.getElementById('getdata').onclick = () => {
  const form_data = {
    'nni': document.getElementById("nni").value,
    'mdp': document.getElementById("password").value
  };
eel.get_data(form_data['nni'], form_data['mdp'])
};
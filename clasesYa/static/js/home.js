diaSeleccionado = 1;

function seleccionarDia(event){
    var diaSeleccionado = event.target.innerHTML;
    console.log(diaSeleccionado);

    var parentElement = document.getElementById('allReservas');
    var children = parentElement.children;
    for (var i = 0; i < children.length; i++) {
        var child = children[i];
        if (child.id === diaSeleccionado) {
            child.style.display = 'block';
        } else {
            child.style.display = 'none';
        }
    }

};
<script>
document.addEventListener("DOMContentLoaded", function () {
  var botonConfirmar = document.getElementById("confirmarCambios");
  var formulario = document.querySelector("form");
  botonConfirmar.addEventListener("click", function (event) {
    event.preventDefault();

    var confirmacion= confirm("Estas seguro de guardar estos cambios?")
    if (confirmacion){
      formulario.submit();
    }
  });
});
</script>
const successMessage = document.getElementById('success');

document.getElementById('barcode').addEventListener('keydown', function(e) {
  if (e.key === 'Enter') {

    e.preventDefault()
        var form = $("#addForm")[0]
        if (!form.checkValidity())
            form.reportValidity()
        else {
            $("#create_button").prop("disabled", true)
            axios({
                method: 'post',
                headers: {
                    'Content-Type': 'application/json'
                },
                url: '/attendances/crud',
                data: new FormData(form)
            }).then(function (response) {
                document.getElementById('barcode').value = ''
                successMessage.textContent = response.data;
                successMessage.style.color = 'limegreen';
                successMessage.style.display = 'block';
                setTimeout(() => {
                    successMessage.style.display = 'none';
                }, 3000);

            }).catch(function (error) {
                document.getElementById('barcode').value = ''
                successMessage.textContent = `❌ No hay ningun miembro con este código de barras`;
                successMessage.style.color = 'red';
                successMessage.style.display = 'block';
                setTimeout(() => {
                    successMessage.style.display = 'none';
                }, 3000);
            });
        }
    }
});
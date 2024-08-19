
document.getElementById('toggleBtn').addEventListener('click', function() {
    const sidebar = document.getElementById('side-nav-bar');
    sidebar.classList.toggle('show');
});

$('#id_focus').change(function() {
    if ($(this).val() === '' || $(this).val() === null) {
        $('#id_instance').empty();
        console.log('empty');
        return;
    }
    grade = $('#id_grade').val();
    fetch(`/exam/get-focus-instances/?focus=${$(this).val()}&grade=${grade}`)
    .then(response => response.json()
        .then(data => {
            $('#id_id').empty();
            for (const opttion of data.options) {
                $('#id_id').append(`<option value="${opttion.id}">${opttion.name}</option>`);
            }
            $('#id_id').prop('disabled', false);
        })
    );
});

$('#focus_filter').change(function() {
    if ($(this).val() === '' || $(this).val() === null) {
        $('#id_instance').empty();
        console.log('empty');
        return;
    }
    grade = $('#id_grade').val();
    fetch(`/exam/get-focus-instances/?focus=${$(this).val()}&grade=${grade}`)
    .then(response => response.json()
        .then(data => {
            $('#filter_id').empty();
            $('#filter_id').append('<option value="">---------</option>');
            for (const opttion of data.options) {
                console.log(opttion);
                $('#filter_id').append(`<option value="${opttion.id}">${opttion.name}</option>`);
            }
            $('#filter_id').prop('disabled', false);
        })
    );
});


document.querySelector('.dropdown-btn').addEventListener('click', function() {
    const dropdownContainer = this.nextElementSibling;
    dropdownContainer.classList.toggle('show');
});


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

$('#bookmarkIcon').click(async function() {
    let isBookmarked;
    if (bookmarkIcon.classList.contains('fas')) {
        isBookmarked = true;
        bookmarkIcon.classList.remove('fas');
        bookmarkIcon.classList.add('far');
        
    } else {
        isBookmarked = false;
        bookmarkIcon.classList.remove('far');
        bookmarkIcon.classList.add('fas');
    }

    const lesson_id = $('#lesson_id').val();
    const csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    console.log(lesson_id, isBookmarked, csrftoken);
    fetch(`/subject/lesson/${lesson_id}/tag/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(
            {
                is_bookmarked: !isBookmarked,
            }
        )
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            // Revert the icon class if the request failed
            if (isBookmarked) {
                bookmarkIcon.classList.remove('far');
                bookmarkIcon.classList.add('fas');
            } else {
                bookmarkIcon.classList.remove('fas');
                bookmarkIcon.classList.add('far');
            }
        }
    });
});


document.querySelector('.dropdown-btn').addEventListener('click', function() {
    const dropdownContainer = this.nextElementSibling;
    dropdownContainer.classList.toggle('show');
});


document.addEventListener('DOMContentLoaded', function() {
    let toggleButtons = document.querySelectorAll('[data-toggle="collapse"]');

    toggleButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            let targetId = button.getAttribute('data-target');
            let targetElement = document.querySelector(targetId);

            if (targetElement) {
                if (targetElement.classList.contains('show')) {
                    targetElement.classList.remove('show');
                } else {
                    targetElement.classList.add('show');
                }
            }
        });
    });
});
